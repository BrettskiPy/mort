from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from mort_server.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """CRUD objet with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        """
        self.model = model

    def get(
        self, db: Session, id: Any, *, include_disabled: bool = False
    ) -> Optional[ModelType]:

        if include_disabled or not hasattr(self.model, "is_active"):
            return db.query(self.model).filter(self.model.id == id).first()

        return (
            db.query(self.model)
            .filter(self.model.id == id)
            .filter(self.model.is_active == True)
            .first()
        )

    def get_multi(
        self,
        db: Session,
        *,
        include_disabled: bool = False,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:

        # Include disabled or the model does not support is_active column
        # both is_active = True and is_active = False will be returned
        if include_disabled or not hasattr(self.model, "is_active"):
            return db.query(self.model).offset(skip).limit(limit).all()

        # Not Include disabled.
        # Only is_active = True will be returned
        return (
            db.query(self.model)
            .filter(self.model.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model()
        for k, v in obj_in_data.items():
            if v:
                db_obj.__dict__[k] = v

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):  # pragma: no cover
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:

        """Returns the removed obj"""

        obj = db.query(self.model).filter(self.model.id == id).first()

        if not obj:
            raise RuntimeError("Item not found")

        db.delete(obj)
        db.commit()

        return obj

    def get_by_field(
        self,
        db: Session,
        *,
        field: str,
        value: Union[str, int],
    ) -> Union[ModelType, List[ModelType]]:
        """
        Query by a column on the model.
        Returns a list if multiple results are present.
        """

        if not hasattr(self.model, field):
            raise Exception(f"{self.model} does not have {field} field")

        filter_field = self.model.__dict__

        results = db.query(self.model).filter(filter_field[field] == value).all()
        if len(results) == 1:
            return results[0]
        return results
