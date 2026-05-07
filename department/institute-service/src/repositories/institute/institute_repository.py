from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from entities import InstituteModel
from .institute_repository_interface import InstituteRepositoryInterface


class InstituteRepository(InstituteRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save(self, institute_model: InstituteModel) -> InstituteModel:
        try:
            self._db_session.add(institute_model)
            await self._db_session.commit()
            await self._db_session.refresh(institute_model)
            return institute_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_all(self) -> List[InstituteModel]:
        try:
            result = await self._db_session.execute(select(InstituteModel))
            return list(result.scalars().all())
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_id(self, institute_id: int) -> Optional[InstituteModel]:
        try:
            model = await self._db_session.get(InstituteModel, institute_id)
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def get_by_name(self, institute_name: str) -> Optional[InstituteModel]:
        try:
            query = select(InstituteModel).where(InstituteModel.name == institute_name)
            result = await self._db_session.execute(query)
            model = result.scalars().first()
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def delete_institute_by_id(self, institute_model: InstituteModel) -> None:
        try:
            await self._db_session.delete(institute_model)
            await self._db_session.commit()
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc