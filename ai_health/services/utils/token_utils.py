from random import randint


def gen_otp_verification_redis_key(user_email: str):
    return f"account_verifications__{user_email}"


def gen_forgot_password_redis_key(user_email: str):
    return f"forgot_password__{user_email}"


def random_with_N_digits(n=6):
    """
    Generate some random number of digits

    Useful for the otp feature.
    """
    range_start = 10 ** (n - 1)
    range_end = (10**n) - 1
    return randint(range_start, range_end)


