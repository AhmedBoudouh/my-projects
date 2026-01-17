from models.user import User

def verify_pin(user: User, input_pin: str) -> bool:
    """
    Verifies if the input PIN matches the user's stored PIN code.
    Case-sensitive, exact match.
    
    Args:
        user (User): the user object to verify
        input_pin (str): PIN entered by the user
    
    Returns:
        bool: True if the PIN is correct, False otherwise
    """
    return user.pin_code == input_pin