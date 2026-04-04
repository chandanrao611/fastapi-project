from typing import Type, Generic, TypeVar, List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

T = TypeVar("T")


class BaseRepository(Generic[T]):

    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    # ✅ Create
    def create(self, data: dict) -> T:
        if hasattr(data, "dict"):
            data = data.dict()
        obj = self.model(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        if hasattr(obj, "password"):
            del obj.password
        return obj

    # ✅ Get by ID
    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    # ✅ Delete
    def delete(self, id: int):
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
        return obj

    # ✅ Generic Pagination + Search + Sort
    def get_paginated(
        self,
        page: int = 1,
        size: int = 10,
        search: Optional[str] = None,
        search_fields: List = [],
        sort_by: str = "id",
        order: str = "desc"
    ) -> Tuple[List[T], int]:

        query = self.db.query(self.model)

        # 🔍 SEARCH
        if search and search_fields:
            from sqlalchemy import or_
            conditions = [
                field.ilike(f"%{search}%") for field in search_fields
            ]
            query = query.filter(or_(*conditions))

        # 🔽 SORT
        sort_column = getattr(self.model, sort_by, self.model.id)

        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # 📊 COUNT
        total = query.count()

        # 📄 PAGINATION
        skip = (page - 1) * size
        data = query.offset(skip).limit(size).all()

        return data, total