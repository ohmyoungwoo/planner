from fastapi import APIRouter, Body, HTTPException, status
from models.events import Event
from typing import List

# 이벤트 라우트 정의 (Chaptor 5 p100의 1)
event_router = APIRouter(
    tags = ["Events"]
)

events = []

# 모든 이벤트 추출  (Chaptor 5의 p100의 2)
@event_router.get("/", response_model = List[Event])
async def retrieve_all_events() -> List[Event]:
    return events

# 특정 ID의 이벤트 추출   (Chaptor 5의 p100의 2)
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist"
    )
    

# 이벤트 생성 및 삭제 라우트 정의 (Chaptor 5의 p101의 3)
@event_router.post("/new")
async def create_event(body: Event = Body(...)) -> dict:
    events.append(body)
    return {
        "message": "Event created successfully."
    }
    
@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    for event in events:
        if event.id == id:
            events.remove(event)
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