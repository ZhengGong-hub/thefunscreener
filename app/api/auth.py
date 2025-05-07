from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from app.config.config import Config

API_KEY_NAME = "thefunscreener-api-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """Validate API key from header.
    
    Args:
        api_key_header: API key from request header
        
    Returns:
        str: Validated API key
        
    Raises:
        HTTPException: If API key is invalid
    """
    config = Config().load_configuration()
    if api_key_header != config.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key_header 