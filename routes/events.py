from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlmodel import select

from database.connection import get_session
from models.events import Event, EventUpdate

from typing import List

# 이벤트 라우트 정의 (Chaptor 5 p100의 1)
event_router = APIRouter(
    tags = ["Events"]
)

events = []

# 모든 이벤트 추출 in SQL dB  (Chaptor 6의 p115)
@event_router.get("/", response_model = List[Event])
async def retrieve_all_events(session=Depends(get_session)):
    statement = select(Event)
    events = session.exec(statement).all()
    
    return events

# 모든 이벤트 추출 in SQL dB  (Chaptor 6의 p115)
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session=Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    

# 이벤트 생성 및 삭제 라우트 정의 SQL dB에서 (Chaptor 6의 p114)
@event_router.post("/new")
async def create_event(new_event: Event, session=Depends(get_session)) -> dict:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully."
    }
    
@event_router.delete("/{id}")
async def delete_event(id: int, session=Depends(get_session)):
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {
            "message": "Event deleted successfully."
            }
        
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist."
    )
        
@event_router.delete("/")
async def delete_all_events() -> dict:
    events.clear()
    return {
        "message": "Events deleted successfully."
    }
    
# SQL dB 활용한 Table Update
@event_router.put("/edit/{id}", response_model=Event)
async def update_event(id: int, new_data: EventUpdate, session=Depends(get_session)):
    event = session.get(Event, id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        
        for key, value, in event_data.items():
            setattr(event, key, value)
            
        session.add(event)
        session.commit()
        session.refresh(event)
        
        return event
    
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist."
    )