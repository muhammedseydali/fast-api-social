from fastapi import HTTPException, status

def raise_not_found_exception(detail: str = " Resource not Found"):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def raise_forbidden_exception(detail: str = " Not Authorized To Perform This Action"):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

def raise_bad_exception(detail: str = " Invalid Request"):
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

def raise_unauthorized_exception(detail: str = "Incorrect Username"):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )

def raise_conflict_exception(detail: str = "Conflict Occured"):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

