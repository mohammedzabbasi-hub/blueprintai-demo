import secrets


def generate_state_token(length: int = 32) -> str:
    return secrets.token_urlsafe(length)


def generate_api_token(length: int = 32) -> str:
    return secrets.token_hex(length)
    
