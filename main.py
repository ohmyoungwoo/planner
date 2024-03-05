import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from typing import List

from routes.users import user_router
from routes.events import event_router
from routes.audits import audit_router

from database.connection import conn


app = FastAPI()

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")
app.include_router(audit_router, prefix="/audit")

@app.on_event("startup")
def on_startup():
    conn()
    
@app.get("/")
async def home():
    #return RedirectResponse(url="/event/")
    return RedirectResponse(url="/audit/")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)