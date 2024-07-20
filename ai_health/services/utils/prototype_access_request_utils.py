from passlib.context import CryptContext
from nanoid import generate


prototype_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_prototype_password(plain_password, hashed_password):
    return prototype_pwd_context.verify(plain_password, hashed_password)


def get_prototype_password_hash(password):
    return prototype_pwd_context.hash(password)


def generate_password_and_hash() -> tuple[str]:
    password = generate(size=10)

    hash_password = get_prototype_password_hash(password=password)
    return password, hash_password
