from .BaseDataModel import BaseDataModel 
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client = db_client) 
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value] 
    
    @classmethod
    async def create_instance(cls , db_client: object):
        instance = cls(db_client=db_client) 
        await instance.init_collection() 
        return instance

    async def init_collection(self):
        all_collection = await self.db_client.list_collection_names() # get all collections
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collection: # if collection does not exist
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
            indexes = Project.get_indexes() # get indexes
            for index in indexes: # loop through indexes
                await self.collection.create_index( # create index
                                                index["key"],
                                                name=index["name"],
                                                unique=index["unique"]
                                                )

    async def creatre_project(self, project: Project):

        result =  await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project.id = result.inserted_id

        return project
    
    async def get_project_or_create(self, project_id: str):
        recored = await self.collection.find_one({"project_id": project_id})
        if recored is None:
            # create project
            project = Project(project_id=project_id)
            project = await self.creatre_project(project=project)
            return project 
        
        return Project(**recored) 
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        total_docs = await self.collection.count_documents({})
        total_pages = total_docs // page_size 
        if total_docs % page_size >0:
            total_pages += 1 

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []

        async for doc in cursor:
            projects.append(Project(**doc))

        return projects, total_pages 
    