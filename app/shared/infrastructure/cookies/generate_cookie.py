def generate_cookie(key: str, value: str, max_age):
    return {
        "key": key,
        "value": value,
        "httponly": False,
        "secure": False,  # 🔒 Set to True in production (HTTPS)
        "samesite": "lax",  # Or "none" if you're dealing with cross-origin
        "max_age": max_age,  # Optional: 15 minutes
        "path": "/",
    }
