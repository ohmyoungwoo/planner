from fastapi import APIRouter, HTTPException, status
from models.users import User, UserSignIn

user_router = APIRouter(
    tags = ["User"],
)

users= {}

@user_router.post("/signup")
async def sign_new_user(data: User):
    if data.email in users:
        raise HTTPException(
         status_code= status.HTTP_409_CONFLICT,
         detail="이미 username이 존재 합니다."   
        )
    users[data.email] = data
    return{
        "message": "User 성공적으로 등록되었습니다!"
    }
    
@user_router.post("/signin")
async def sign_user_in(user: UserSignIn):
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User 가 존재하지 않습니다."
        )
        
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail="password가 다릅니다."
        )
    
    return {
        "message": "User Signed in Successfully."
    }