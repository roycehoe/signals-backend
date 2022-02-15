from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.errors import (
    INVALID_CREDENTIALS,
    InvalidCredentialsError,
    InvalidUserQueryError,
    UserNotFoundError,
)
from app.services.authentication import get_access_token

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenOut,
)
def login(
    request: schemas.UserIn,
    session: Session = Depends(get_session),
):
    """Creates a JWT access token for an authenticated user

    :param request: The request body for users to key in their authentication credentials
    :type: schemas.UserIn
    :param session: The database that user's credentials are authenticated with
    :type session: Session
    :returns: A created JWT access token
    :rtype: schemas.TokenOut
    :raises HTTPException: if token validation fails
    """

    try:
        return get_access_token(request, session)

    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": INVALID_CREDENTIALS},
        )

    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": INVALID_CREDENTIALS},
        )

    except InvalidUserQueryError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": INVALID_CREDENTIALS},
        )
