from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative

@as_declarative()
class BaseMeta:
    id: any
    __name__: str

    # generate tablename from classname.
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()