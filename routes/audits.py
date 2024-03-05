from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlmodel import select

from database.connection import get_session
from models.audits import Audit, AuditUpdate

from typing import List

# 이벤트 라우트 정의 (Chaptor 5 p100의 1)
audit_router = APIRouter( tags = ["Audits"])
templates = Jinja2Templates(directory="templates")

audits = []

# 모든 이벤트 추출 in SQL dB  (Chaptor 6의 p115)
@audit_router.get("/", response_model = List[Audit])
async def search_all_audits(session=Depends(get_session)):
    statement = select(Audit)
    audit_list = session.exec(statement).all()
    return audit_list

#@audit_router.get("/", response_class=HTMLResponse)
#async def search_all_audits(request: Request, id: str):
    #return templates.TemplateResponse(name="audit_list.html", request=audits) 

# 모든 이벤트 추출 in SQL dB  (Chaptor 6의 p115)
@audit_router.get("/{id}", response_model=Audit)
async def search_audit(id: int, session=Depends(get_session)):
    audit = session.get(Audit, id)
    if audit:
        return audit
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="진단했던 이력이 없습니다."
    )
    

# 이벤트 생성 및 삭제 라우트 정의 SQL dB에서 (Chaptor 6의 p114)
@audit_router.post("/new")
async def create_audit(new_audit: Audit, session=Depends(get_session)) -> dict:
    session.add(new_audit)
    session.commit()
    session.refresh(new_audit)

    return {
        "message": "진단결과가 추가 되었습니다."
    }
    
@audit_router.delete("/{id}")
async def delete_audit(id: int, session=Depends(get_session)):
    audit = session.get(Audit, id)
    if audit:
        session.delete(audit)
        session.commit()
        return {
            "message": "진단결과를 삭제 했습니다."
            }
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="삭제할 진단결과가 없습니다."
    )

# 모든 진단결과를 삭제
"""        
@audit_router.delete("/")
async def delete_all_audits() -> dict:
    audits.clear()
    return {
        "message": "모든 진단결과를 지웠습니다."
    }
"""
    
# SQL dB 활용한 Table Update
@audit_router.put("/edit/{id}", response_model=Audit)
async def update_event(id: int, new_data: AuditUpdate, session=Depends(get_session)):
    audit = session.get(Audit, id)
    if audit:
        audit_data = new_data.dict(exclude_unset=True)
        
        for key, value, in audit_data.items():
            setattr(audit, key, value)
            
        session.add(audit)
        session.commit()
        session.refresh(audit)
        
        return audit
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="수정할 진단결과가 없습니다."
    )