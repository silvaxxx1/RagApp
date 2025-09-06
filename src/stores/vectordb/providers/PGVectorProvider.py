from ..VectorDBInterface import VectorDBInterface 
from ..VectorDBEnums import (
    pgVectorDistanceMethodEnums,
    pgVectorIndexTypeEnums,
    pgVectorTableSchemeEnums,
    DistanceMethodEnum
) 

import logging 
from typing import List 
from models.db_schemes import RetrievedDocument 

from sqlalchemy.sql import text as sql_text 
import json 


class PGVectorProvider(VectorDBInterface): 
    def __init__(self, 
                 db_client,
                 default_vector_size : int = 786,
                 distance_method : str = None,
                 index_threshold : int = 0.5): 
        
        self.db_client = db_client 
        self.default_vector_size = default_vector_size 
        self.distance_method = distance_method 

        self.index_threshold = index_threshold

        self.pgvector_table_prefix = pgVectorTableSchemeEnums.PGVECTOR_TABLE_PREFIX.value

        self.logger = logging.getLogger("uvicorn")
        self.default_index_name = lambda collection_name: f"{collection_name}_vector_idx"

        # Equivalent to 
        # def default_index_name(self, collection_name):
        #     return f"{collection_name}_vector_idx"

    async def connect(self):
        async with self.db_client() as session: 
            async with session.begin(): 
                await session.execute(
                    sql_text(
                        "CREATE EXTENSION IF NOT EXISTS vector"
                    )
                )        
            await session.commit() 


    async def disconnect(self):
        pass

    
    async def is_collection_exist(self, 
                        collection_name : str)->bool:
        record = None
        async with self.db_client() as session:
            async with session.begin():
                list_table = await session.exSizingAlgoecute(
                    sql_text(
                    "SELECT EXISTS (SELECT *  FROM pg_tables WHERE tablename = :collection_name"),
                    )
                result = await session.execute(
                    list_table,
                    {"collection_name": collection_name}
                )
                record = result.scalars().one_or_none() 

        return record 
    
    async def list_all_collection(self)->List:
        records = []
        async with self.db_client() as session: 
            async with session.begin():
                list_table = await session.execute(
                    sql_text(
                       "SELECT * FROM pg_tables WHERE tablename LIKE :prefix"
                    )
                )
                result = await session.execute(
                    list_table,
                    {"prefix": self.pgvector_table_prefix}
                )
                records = result.scalars().all()  

        return records
      
    async def get_collection_info(self, 
                        collection_name : str)->dict:
        
        async with self.db_client() as session:
            async with session.begin():
                list_table_info = await session.execute(
                    sql_text('''
                        SELECT shemaname,tablename, tableowner, tablespace, hasindexes
                        FROM pg_tables
                        WHERE tablename = :collection_name 
                ''')
                )

                count_sql = sql_text(f' SELECT COUNT(*) FROM {collection_name}')

                table_info = await session.execute(
                    list_table_info,
                    {"collection_name": collection_name}
                )
                record_count = await session.execute(count_sql, {"collection_name": collection_name})
                
                table_data = table_info.fetchone()
                if not  table_data: 
                    return None

        return {
            "table_info": dict(table_data),
            "record_count": record_count
            }

    async def delete_collection(self, 
                        collection_name : str):
        async with self.db_client() as session:
            async with session.begin():
                logging.info(f"Deleting collection {collection_name}")
                delete_table =  sql_text(
                        f"DROP TABLE IF EXISTS {collection_name}"
                    ) 
                await session.execute(delete_table, {"collection_name": collection_name})
                await session.commit()

        return True 
    
    async def create_collection(self, 
                        collection_name : str,
                        embedding_size : int,
                        do_reset : bool = False): 
        
        if do_reset: 
            _ = self.delete_collection(collection_name = collection_name)

        is_coolection_exist = await self.is_collection_exist(collection_name = collection_name)
        
        if not is_coolection_exist: 
            async with self.db_client() as session:
                async with session.begin():
                    logging.info(f"Creating collection {collection_name}")
                    create_table = sql_text(
                        f'CREATE TABLE {collection_name} ('
                            f'{pgVectorTableSchemeEnums.ID.value} bigserial PRIMARY KEY,'
                            f'{pgVectorTableSchemeEnums.TEXT.value} text, '
                            f'{pgVectorTableSchemeEnums.VECTOR.value} vector({embedding_size}), '
                            f'{pgVectorTableSchemeEnums.METADATA.value} jsonb DEFAULT \'{{}}\', '
                            f'{pgVectorTableSchemeEnums.CHUNK_ID.value} integer, '
                            f'FOREIGN KEY ({pgVectorTableSchemeEnums.CHUNK_ID.value}) REFERENCES chunks(chunk_id)'
                        ')'
                    )

                    await session.execute(create_table, {"collection_name": collection_name})
                    await session.commit() 

            return True

        return False
    

    async def is_index_exist(self, 
                        collection_name : str,
                         )->bool:
        index_name = self.default_index_name(collection_name = collection_name)
        async with self.db_client() as session:
            async with session.begin():
                check_sql = sql_text('''
                        SELECT 1 
                        FROM pg_indexes
                        WHERE tablename = :collection_name
                        AND indexname = :index_name     
                    ''')
                
                result = await session.execute(
                    check_sql,
                    {"collection_name": collection_name},
                    {"index_name": index_name}
                )

                return bool(result.scalars().one_or_none())

    async def create_index_vector(self,
                                collection_name : str,
                                index_type = pgVectorIndexTypeEnums.HNSW.value):
        
        is_index_exist = await self.is_index_exist(collection_name = collection_name)
        if not is_index_exist: 
            return False

        async with self.db_client() as session:
            async with session.begin():
                count_sql = sql_text(f' SELECT COUNT(*) FROM {collection_name}')
                result = await session.execute(count_sql, {"collection_name": collection_name})
                record_count = result.scalar_one() 

                if record_count < self.min_index_record_count:
                    return False
                
                self.logger.info(f"Creating index for collection {collection_name}")
                index_name = self.default_index_name(collection_name = collection_name)
                create_index_sql = sql_text(f'CREATE INDEX {index_name} ON {collection_name}'
                                             f'USING {index_type}'
                                             f'({pgVectorTableSchemeEnums.VECTOR.value} {self.distance_method})'
                                             )

                await session.execute(create_index_sql)
                self.logger.info(f"End : Index created for collection {collection_name}")
                await session.commit()
                return True 
    

    async def reset_vector_index(self, collection_name: str, 
                                       index_type: str = pgVectorIndexTypeEnums.HNSW.value) -> bool:
        
        index_name = self.default_index_name(collection_name)
        async with self.db_client() as session:
            async with session.begin():
                drop_sql = sql_text(f'DROP INDEX IF EXISTS {index_name}')
                await session.execute(drop_sql)
        
        return await self.create_vector_index(collection_name=collection_name, index_type=index_type)


    async def insert_one(self, 
                    collection_name : str,
                    text : str,
                    vector : list,
                    metadata : dict = None,
                    record_id : str = None): 
        
        is_collection_exist = await self.is_collection_exist(collection_name = collection_name)
        if not is_collection_exist: 
            self.logger.warning(f"cannot insert into non existing Collection {collection_name}")
        
            return False 

        if not record_id:
            self.logger.warning(f"cannot insert record without chunk_id: {collection_name}")
        async with self.db_client() as session: 
            async with session.begin():
                insert_sql = sql_text(f'INSERT INTO {collection_name} '
                                      f'({pgVectorTableSchemeEnums.TEXT.value}, {pgVectorTableSchemeEnums.VECTOR.value}, {pgVectorTableSchemeEnums.METADATA.value}, {pgVectorTableSchemeEnums.CHUNK_ID.value}) '
                                      'VALUES (:text, :vector, :metadata, :chunk_id)'
                                      )

                await session.execute(insert_sql, {
                    'text': text,
                    'vector': "[" + ",".join([ str(v) for v in vector ]) + "]",
                    'metadata': metadata,
                    'chunk_id': record_id
                })
                await session.commit()
                
        return True        

    async def insert_many(self, 
                    collection_name : str,
                    texts : List,
                    vectors : list,
                    metadata : list = None,
                    record_ids : list = None,
                    batch_size : int = 50):

        is_collection = await self.is_collection_exist(collection_name = collection_name)
        if not is_collection: 
            self.logger.warning(f"cannot insert records into non existing Collection {collection_name}")
        
            return False 
        
        if len(vectors) != len(record_ids):
            self.logger.warning(f"cannot insert records into non existing Collection {collection_name}")
            return False
        
        if  not len(metadata) == 0:
            metadata = [None] * len(texts) 


        async with self.db_client() as session:
            async with session.begin():

                for i in range(0, len(texts), batch_size):
                    batch_end = i + batch_size

                    batch_texts = texts[i:batch_end]
                    batch_vectors = vectors[i:batch_end]
                    batch_metadata = metadata[i:batch_end]
                    batch_record_ids = record_ids[i:batch_end]

                    values = []

                    for _text, _vector, _metadata, _chunk_id in zip(batch_texts, batch_vectors, batch_metadata, batch_record_ids):
                        values.append({
                            _text,
                            "[" + ",".join([ str(v) for v in _vector ]) + "]",
                            _metadata,
                            _chunk_id
                        })

                    batch_insert_sql = sql_text(f'INSERT INTO {collection_name} '
                                    f'({pgVectorTableSchemeEnums.TEXT.value}, '
                                    f'{pgVectorTableSchemeEnums.VECTOR.value}, '
                                    f'{pgVectorTableSchemeEnums.METADATA.value}, '
                                    f'{pgVectorTableSchemeEnums.CHUNK_ID.value}) '
                                    f'VALUES (:text, :vector, :metadata, :chunk_id)')
                    
                    await session.execute(batch_insert_sql, values)

                await session.commit()  

        return True 
    
    async def search_by_vector(self, collection_name, vector, limit):

        is_collection = await self.is_collection_exist(collection_name = collection_name)
        if not is_collection: 
            self.logger.warning(f"cannot search by vector into non existing Collection {collection_name}")
        
            return None 
        
        vector = "[" + ",".join([ str(v) for v in vector ]) + "]"
        async with self.db_client() as session:
            async with session.begin():
                 search_sql = sql_text(f'SELECT {pgVectorTableSchemeEnums.TEXT.value} as text,  1 - ({pgVectorTableSchemeEnums.VECTOR.value} <=> :vector) as score'
                                      f' FROM {collection_name}'
                                      ' ORDER BY score DESC '
                                      f'LIMIT {limit}'
                                      )

                 results = await session.execute(search_sql, {'vector': vector})
                 records = results.fetchall() 

                 return [
                     RetrievedDocument(**{
                          "text" : record.text,
                          "score": record.score,
                            })
                     for record in records
                 ] 
            
        
        
                                                

            

        

        

    
                   


        
