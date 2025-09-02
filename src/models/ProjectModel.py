from .BaseDataModel import BaseDataModel 
from .db_schemes import Project
from sqlalchemy.future import select
from sqlalchemy import func 

class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client=db_client)
        self.db_client = db_client

    @classmethod
    async def create_instance(cls, db_client):
        return cls(db_client=db_client)

    async def create_project(self, project: Project):
        async with self.db_client() as session:
            session.add(project)
            await session.commit()
            await session.refresh(project)
            return project

    async def get_project_or_create(self, project_id: int):
        async with self.db_client() as session:
            result = await session.execute(
                select(Project).where(Project.project_id == project_id)
            )
            project = result.scalars().first()
            if not project:
                project = Project(project_id=project_id)
                session.add(project)
                await session.commit()
                await session.refresh(project)
            return project
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        async with self.db_client() as session:
            total_documents = await session.execute(
                select(func.count(Project.project_id))
            )
            total_documents = total_documents.scalar_one()
            total_pages = (total_documents + page_size - 1) // page_size

            result = await session.execute(
                select(Project)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )
            projects = result.scalars().all()
            return projects, total_pages