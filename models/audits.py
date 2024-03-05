from sqlmodel import JSON, SQLModel, Field, Column
from typing import Optional, List
#from datetime import date

class Audit(SQLModel, table=True):
    id: int = Field(default=None, primary_key= True)
    title: str
    #description: str
    auditor: str
    #dt_date: str
    #file_ppt: str
    #tags: List[str] = Field(sa_column=Column(JSON))
    
    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example":{
                "title": "진단제목",
    #            "description": "진단내용 간략히...",
                "auditor": "홍길동",
    #            "dt_date": "2023.02.01",
    #            "file_ppt": "https://linktomyimage.com/image.png",
    #            "tags": ["키친", "냉장고", "이슈", "화재"]
            }
        }

class AuditUpdate(SQLModel):
    title: Optional[str]
    #description: Optional[str]
    auditor: Optional[str]
    #dt_date: Optional[str]
    #file_ppt: Optional[str]
    #tags: Optional[List[str]]
    
    class Config:
        schema_extra = {
            "example":{
                "title": "진단제목",
                "description": "진단내용 간략히...",
                "auditor": "홍길동",
                "dt_date": "2023.02.01",
                "file_ppt": "https://linktomyimage.com/image.png",
                "tags": ["키친", "냉장고", "이슈", "화재"]
            }
        }