from .BaseDataModel import BaseDataModel 
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy import select 


class AssetModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client):
        return cls(db_client=db_client)

    async def create_asset(self, asset: Asset):
        async with self.db_client() as session:
            session.add(asset)
            await session.commit()
            await session.refresh(asset)
            return asset

    async def get_all_project_asset(self, asset_project_id: int, asset_type: str):
        async with self.db_client() as session:
            result = await session.execute(
                select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_type == asset_type
                )
            )
            return result.scalars().all()

    async def get_asset_record(self, asset_project_id: int, asset_name: str):
        async with self.db_client() as session:
            result = await session.execute(
                select(Asset).where(
                    Asset.asset_project_id == asset_project_id,
                    Asset.asset_name == asset_name
                )
            )
            return result.scalars().one_or_none()