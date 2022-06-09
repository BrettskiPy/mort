from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generates __tablename__ for model automatically from the class name
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
