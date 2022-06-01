def password_valid(password: str) -> bool:
    """
    # FIXME: rewrite to marshmallow.validator to detalize errors
    #  https://marshmallow.readthedocs.io/en/stable/marshmallow.validate.html#marshmallow.validate.And

    Passwords must contain at least one digit or special character.
    Passwords must be between 8 and 128 characters.
    Passwords cannot contain spaces.

    Returns: True if password meets conditions, False otherwise
    """
    conditions = [
        lambda s: any(x.isdigit() or not x.isalnum() for x in s),
        lambda s: all(not x.isspace() for x in s),
        lambda s: 8 <= len(s) <= 128,
    ]
    return all(cond(password) for cond in conditions)
