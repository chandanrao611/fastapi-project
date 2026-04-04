import re
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

def map_to_schema(schema, data):
    return [schema.model_validate(item) for item in data]

def validate_password(data: str):
    if not data:
        return "Password is required"
    if len(data) < 8:
        return "Password must be at least 8 characters long"
    if len(data) > 16:
        return "Password must be at most 16 characters long"
    if not any(c.isalpha() for c in data):
        return "Password must contain at least one letter"
    if not any(c.isdigit() for c in data):
        return "Password must contain at least one digit"
    return None

def validate_email(data: str):
    if not data:
        return "Email is required"
    if len(data) > 255:
        return "Email must be at most 255 characters long"
    if '@' not in data or '.' not in data:
        return "Email must be a valid email address"
    if not re.match(EMAIL_REGEX, data):
        return "Email must be a valid email address"
    return None

def validate_mobile(data: int):
    if not data:
        return "Mobile number is required"
    if len(str(data)) != 10:
        return "Mobile number must be 10 digits long"
    if not str(data).isdigit():
        return "Mobile number must contain only digits"
    return None
