from pydantic import BaseModel


class AbstractModel(BaseModel):
    """
    Base Model with ORM Mode as True so it can interface and get data directly from the returned db data
    """

    class Config:
        use_enum_values = True
        from_attributes = True
