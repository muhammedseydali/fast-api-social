from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas, auth
from ..database import get_db
from ..exceptions import (
    raise_not_found_exception,
    raise_bad_exception,
    raise_conflict_exception,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.Usercreate, db:db_dependency):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise_conflict_exception("Username already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        username = user.username, email = user.email, hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#follow user endpoint

@router.post("/{user_id}/follow", status_code=204)
def follow_user(user_id:int, db:db_dependency, current_user: models.User = Depends(auth.get_current_user),):
    user_to_follow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_follow:
        raise_not_found_exception("user not found")
    if user_to_follow == current_user:
        raise_bad_request_exception("cannot follow yourself")
    if user_to_follow in current_user.following:
        raise_bad_request_exception("Already following this user")
    current_user.following.append(user_to_follow)
    db.commit()
    return

#unfollow user endpoint
@router.post("/{user_id}/unfollow", status_code=204)
def unfollow_user(user_id: int, db:db_dependency, current_user: models.User = Depends(auth.get_current_user),):
    user_to_unfollow = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_unfollow:
        raise_not_found_exception("user not found")
    if user_to_unfollow == current_user:
        raise_bad_request_exception("cannot unfollow yourself")
    if user_to_unfollow not in current_user.following:
        raise_bad_request_exception("not following this user")
    current_user.following.remove(user_to_unfollow)
    db.commit()
    return