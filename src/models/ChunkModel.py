from .BaseDataModel import BaseDataModel 
from .db_schemes import DataChunk 
from helpers.config import get_settings
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy.future import select
from sqlalchemy import delete , func

class ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        self.app_settings = get_settings()
        self.db_client = db_client 

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client=db_client) 
        return instance

    async def create_chunk(self, chunk: DataChunk):
        async with self.db_client() as session:
            session.add(chunk)
            await session.commit()
            await session.refresh(chunk)
            return chunk
    
    async def get_chunk(self, chunk_id: str):
        async with self.db_client() as session:
            result = await session.execute(select(DataChunk).where(DataChunk.chunk_id == chunk_id))
            chunk = result.scalars().one_or_none()
            return chunk
    
    async def insert_many_chunks(self, chunks: list, batch_size: int = 100):
        async with self.db_client() as session:
            try:
                for i in range(0, len(chunks), batch_size):
                    batch = chunks[i:i + batch_size] 
                    session.add_all(batch)
                await session.commit()
                return len(chunks)
            except Exception as e:
                await session.rollback()
                raise e
    
    async def delete_chunk_by_project_id(self, project_id: int):
        async with self.db_client() as session:
            try:
                stmt = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount
            except Exception as e:
                await session.rollback()
                raise e

    async def get_project_chunk(self, project_id: int, page_no: int = 1, page_size: int = 50):
        async with self.db_client() as session:
            stmt = select(DataChunk).where(DataChunk.chunk_project_id == project_id)\
                                     .offset((page_no - 1) * page_size)\
                                     .limit(page_size)
            result = await session.execute(stmt)
            records = result.scalars().all()
            return records 
        
    async def get_total_chunk_count(self, project_id: int) -> int:
        """
        Returns the total number of chunks for a project as an integer.
        """
        async with self.db_client() as session:
            stmt = select(func.count(DataChunk.chunk_id))\
                   .where(DataChunk.chunk_project_id == project_id)
            result = await session.execute(stmt)
            total_count = result.scalar()  # <-- converts ScalarResult to int
            return total_count or 0       # <-- ensures int even if None
