from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Single Bearer token for Swagger UI
bearer_scheme = HTTPBearer()

FAKE_TOKEN = "fake-jwt-token"

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> str:
    """
    Validate the token for protected endpoints.
    """
    if credentials.credentials != FAKE_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return "mock-user"