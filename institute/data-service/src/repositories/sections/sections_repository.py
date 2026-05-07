from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import SectionModel
from .sections_repository_interface import SectionsRepositoryInterface


class SectionsRepository(SectionsRepositoryInterface):
    def __init__(self, db_session: AsyncSession):
        self._db_session: AsyncSession = db_session

    async def save_section(self, section_model: SectionModel) -> Optional[SectionModel]:
        try:
            self._db_session.add(section_model)
            await self._db_session.commit()
            await self._db_session.refresh(section_model)
            return section_model
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc

    async def get_by_id(self, section_id: int) -> Optional[SectionModel]:
        try:
            model = await self._db_session.get(SectionModel, section_id)
            return model
        except SQLAlchemyError as exc:
            raise exc

    async def delete_section(self, section_model: SectionModel) -> None:
        try:
            await self._db_session.delete(section_model)
            await self._db_session.commit()
        except SQLAlchemyError as exc:
            await self._db_session.rollback()
            raise exc