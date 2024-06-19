from aiomono.exceptions import ValidationException


def validate_token(token: str):
    if not isinstance(token, str):
        raise ValidationException(
            f"Token is invalid! It must be 'str' type instead of {type(token)} type."
        )
