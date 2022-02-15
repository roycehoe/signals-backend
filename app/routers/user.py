from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.errors import USERNAME_TAKEN, UsernameNotUniqueError
from app.services import user

router = APIRouter(tags=["user"], prefix="/user")


@router.post(
    "/new",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(request: schemas.UserIn, session: Session = Depends(get_session)):
    """Creates and stores a new user in a database

    :param request: The request body for users to input their new account credentials
    :type: schemas.UserIn
    :param session: The database that user's credentials are uploaded to
    :type session: Session
    :returns: The user's username
    :rtype: schemas.UserOut
    :raises HTTPException: If username validation fails
    """

    try:
        return user.create_user(request, session)

    except UsernameNotUniqueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": USERNAME_TAKEN},
        )
