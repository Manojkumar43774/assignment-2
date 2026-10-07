from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models import User
from app.schemas import AdminUsersResponse, UserResponse
from app.auth import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=AdminUsersResponse)
def list_users(admin_username: str = Depends(require_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    return AdminUsersResponse(users=users)


@router.post("/users/{username}/promote", response_model=UserResponse)
def promote_user(username: str, admin_username: str = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.role = "admin"
    db.commit()
    db.refresh(user)
    return user


@router.delete("/users/{username}")
def delete_user(username: str, admin_username: str = Depends(require_admin), db: Session = Depends(get_db)):
    if username == admin_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Admins cannot delete their own account")

    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User '{username}' deleted"}
