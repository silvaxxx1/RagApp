from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import (
    pgVectorIndexTypeEnums,
    pgVectorDistanceMethodEnums,
    pgVectorTableSchemeEnums,
    DistanceMethodEnums,
)

import logging
from typing import List
from models.db_schemes import RetrievedDocument
from sqlalchemy.sql import text as sql_text
import json


class PGVectorProvider(VectorDBInterface):
    def __init__(self,
                 db_client,
                 default_vector_size: int = 786,
                 distance_method: str = "cosine",
                 index_threshold: int = 0.5,
                 min_index_record_count: int = 100):

        self.db_client = db_client
        self.default_vector_size = default_vector_size

        self.index_threshold = index_threshold 

        if distance_method == DistanceMethodEnums.COSINE.value:
            distance_method = pgVectorDistanceMethodEnums.COSINE.value
        elif distance_method == DistanceMethodEnums.DOT.value:
            distance_method = pgVectorDistanceMethodEnums.DOT.value

        self.pgvector_table_prefix = pgVectorTableSchemeEnums._PREFIX.value 
        self.distance_method = distance_method

        self.logger = logging.getLogger("uvicorn")
        self.default_index_name = lambda collection_name: f"{collection_name}_vector_idx"

    # ------------------------------------------
    # Connection Management
    # ------------------------------------------
    async def connect(self):
        async with self.db_client() as session:
            async with session.begin():
                await session.execute(sql_text("CREATE EXTENSION IF NOT EXISTS vector"))
            await session.commit()

    async def disconnect(self):
        pass

    # ------------------------------------------
    # Collection Management
    # ------------------------------------------
    async def is_collection_exist(self, collection_name: str) -> bool:
        record = None
        async with self.db_client() as session:
            async with session.begin():
                query = sql_text(
                    f'SELECT * FROM pg_tables WHERE tablename = :collection_name' )
    
                result = await session.execute(query, {'collection_name': collection_name})
                record = result.scalars().one_or_none()

        return record 

    async def list_all_collection(self) -> List:
        records = []
        async with self.db_client() as session:
            async with session.begin():
                query = sql_text(
                    f"SELECT tablename FROM pg_tables WHERE tablename LIKE :prefix"
                )
                result = await session.execute(query, {'prefix': self.pgvector_table_prefix})
                records = result.scalars().all()

        return records

    async def get_collection_info(self, collection_name: str) -> dict:
        async with self.db_client() as session:
            async with session.begin():
                table_info_sql = sql_text(f"""
                    SELECT schemaname, tablename, tableowner, tablespace, hasindexes 
                    FROM pg_tables 
                    WHERE tablename = :collection_nam
                """)

                count_sql = sql_text(f"SELECT COUNT(*) FROM {collection_name}")

                table_info = await session.execute(table_info_sql, {'collection_name': collection_name})
                record_count = await session.execute(count_sql)

                table_data = table_info.fetchone()
                if not table_data:
                    return None

                return {
                    "table_info": {
                        "schemaname": table_data[0],
                        "tablename": table_data[1],
                        "tableowner": table_data[2],
                        "tablespace": table_data[3],
                        "hasindexes": table_data[4],
                    },
                    "record_count": record_count.scalar_one(),
                    }

    async def delete_collection(self, collection_name: str):
        async with self.db_client() as session:
            async with session.begin():
                self.logger.info(f"Deleting collection {collection_name}")
                delete_sql = sql_text(f"DROP TABLE IF EXISTS {collection_name}")
                await session.execute(delete_sql)
                await session.commit()
        return True

    async def create_collection(self,
                                collection_name: str,
                                embedding_size: int,
                                do_reset: bool = False):

        if do_reset:
            _ = await self.delete_collection(collection_name=collection_name)

        is_exist = await self.is_collection_exist(collection_name=collection_name)

        if not is_exist:
            async with self.db_client() as session:
                async with session.begin():
                    self.logger.info(f"Creating collection {collection_name}")
                    create_table_sql = sql_text(f"""
                        CREATE TABLE {collection_name} (
                            {pgVectorTableSchemeEnums.ID.value} bigserial PRIMARY KEY,
                            {pgVectorTableSchemeEnums.TEXT.value} text,
                            {pgVectorTableSchemeEnums.VECTOR.value} vector({embedding_size}),
                            {pgVectorTableSchemeEnums.METADATA.value} jsonb DEFAULT '{{}}',
                            {pgVectorTableSchemeEnums.CHUNK_ID.value} integer,
                            FOREIGN KEY ({pgVectorTableSchemeEnums.CHUNK_ID.value}) REFERENCES chunks(chunk_id)
                        )
                    """)
                    await session.execute(create_table_sql)
                    await session.commit()
            return True

        return False

    # ------------------------------------------
    # Index Management
    # ------------------------------------------
    async def is_index_exist(self, collection_name: str) -> bool:
        index_name = self.default_index_name(collection_name)
        async with self.db_client() as session:
            async with session.begin():
                check_sql = sql_text(f"""
                    SELECT 1
                    FROM pg_indexes
                    WHERE tablename = '{collection_name}'
                      AND indexname = '{index_name}'
                """)
                result = await session.execute(check_sql)
                return bool(result.scalars_one_or_none())

    async def create_index_vector(self,
                                  collection_name: str,
                                  index_type=pgVectorIndexTypeEnums.HNSW.value):

        is_index = await self.is_index_exist(collection_name)
        if is_index:
            return False

        async with self.db_client() as session:
            async with session.begin():
                count_sql = sql_text(f"SELECT COUNT(*) FROM {collection_name}")
                record_count = (await session.execute(count_sql)).scalar()

                if record_count < self.min_index_record_count:
                    self.logger.warning(
                        f"Not enough records to create index ({record_count} < {self.min_index_record_count})"
                    )
                    return False

                self.logger.info(f"Creating index for collection {collection_name}")
                index_name = self.default_index_name(collection_name)

                create_index_sql = sql_text(
                    f"CREATE INDEX {index_name} ON {collection_name} "
                    f"USING {index_type} ({pgVectorTableSchemeEnums.VECTOR.value} {self.distance_method})"
                )
                await session.execute(create_index_sql)
                await session.commit()

                self.logger.info(f"Index created for collection {collection_name}")
                return True

    async def reset_vector_index(self, collection_name: str,
                                 index_type: str = pgVectorIndexTypeEnums.HNSW.value) -> bool:
        index_name = self.default_index_name(collection_name)
        async with self.db_client() as session:
            async with session.begin():
                drop_sql = sql_text(f"DROP INDEX IF EXISTS {index_name}")
                await session.execute(drop_sql)

        return await self.create_index_vector(collection_name, index_type=index_type)

    # ------------------------------------------
    # Data Insert
    # ------------------------------------------
    async def insert_one(self,
                         collection_name: str,
                         text: str,
                         vector: list,
                         metadata: dict = None,
                         record_id: str = None):

        if not await self.is_collection_exist(collection_name):
            self.logger.warning(f"Cannot insert into non-existing collection {collection_name}")
            return False

        if record_id is None:
            self.logger.warning(f"Cannot insert record without chunk_id into {collection_name}")
            return False

        vector_str = "[" + ",".join(str(v) for v in vector) + "]"
        metadata_json = json.dumps(metadata, ensure_ascii=False) if metadata is not None else '{}'
        async with self.db_client() as session:
            async with session.begin():
                insert_sql = sql_text(f"""
                    INSERT INTO {collection_name}
                    ({pgVectorTableSchemeEnums.TEXT.value},
                     {pgVectorTableSchemeEnums.VECTOR.value},
                     {pgVectorTableSchemeEnums.METADATA.value},
                     {pgVectorTableSchemeEnums.CHUNK_ID.value})
                    VALUES (:text, :vector, :metadata, :chunk_id)
                """)
                await session.execute(insert_sql, {
                    'text': text,
                    'vector': vector_str,
                    'metadata': metadata_json,
                    'chunk_id': record_id
                })
                await session.commit()

        return True

    async def insert_many(self,
                            collection_name: str,
                            texts: List,
                            vectors: list,
                            metadata: list = None,
                            record_ids: list = None,
                            batch_size: int = 50):

            if not await self.is_collection_exist(collection_name):
                self.logger.warning(f"Cannot insert into non-existing collection {collection_name}")
                return False

            if len(vectors) != len(record_ids):
                self.logger.warning("Vectors and record_ids length mismatch")
                return False

            if metadata is None or len(metadata) == 0:
                metadata = [{}] * len(texts)

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
                            metadata_json = json.dumps(_metadata, ensure_ascii=False) if _metadata is not None else "{}"
                            values.append({
                                "text": _text,
                                "vector": "[" + ",".join(str(v) for v in _vector) + "]",
                                "metadata": metadata_json,
                                "chunk_id": _chunk_id
                            })

                        batch_insert_sql = sql_text(f"""
                            INSERT INTO {collection_name}
                            ({pgVectorTableSchemeEnums.TEXT.value},
                            {pgVectorTableSchemeEnums.VECTOR.value},
                            {pgVectorTableSchemeEnums.METADATA.value},
                            {pgVectorTableSchemeEnums.CHUNK_ID.value})
                            VALUES (:text, :vector, :metadata, :chunk_id)
                        """)
                        await session.execute(batch_insert_sql, values)
                    
            self.create_index_vector(collection_name = collection_name)

            return True

    # ------------------------------------------
    # Search
    # ------------------------------------------
    async def search_by_vector(self, collection_name: str, vector: list, limit: int):
        if not await self.is_collection_exist(collection_name):
            self.logger.warning(f"Cannot search by vector in non-existing collection {collection_name}")
            return None

        vector_str = "[" + ",".join(str(v) for v in vector) + "]"

        async with self.db_client() as session:
            async with session.begin():
                search_sql = sql_text(f"""
                    SELECT {pgVectorTableSchemeEnums.TEXT.value} AS text,
                           1 - ({pgVectorTableSchemeEnums.VECTOR.value} <=> :vector) AS score
                    FROM {collection_name}
                    ORDER BY score DESC
                    LIMIT {limit}
                """)

                results = await session.execute(search_sql, {'vector': vector_str})
                records = results.fetchall()

                return [
                    RetrievedDocument(text=record.text, score=record.score)
                    for record in records
                ]
