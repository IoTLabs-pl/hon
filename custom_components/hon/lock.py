from typing import Any, ClassVar
from dataclasses import dataclass
from homeassistant.components import lock

from pyhon.parameter import RangeParameter

from .common import (
    EntityDescription,
    async_setup_entry_factory,
    RemoteControlEntity,
    Parameter,
)


class LockEntity(RemoteControlEntity[Parameter], lock.LockEntity):
    entity_description: "LockEntityDescription"

    @property
    def is_locked(self) -> bool | None:
        return self._source.value == 1

    # TODO: Parameter should point to its command
    async def async_set(self, value: int) -> None:
        s = self._source
        s.value = value

        await self._source.send()

    async def async_lock(self, **kwargs: Any) -> None:
        s = self._source
        await self.async_set(s.max if isinstance(s, RangeParameter) else 1)

    async def async_unlock(self, **kwargs: Any) -> None:
        s = self._source
        await self.async_set(s.min if isinstance(s, RangeParameter) else 0)


@dataclass(frozen=True, kw_only=True)
class LockEntityDescription(EntityDescription, lock.LockEntityDescription):
    entity_cls: ClassVar[type[LockEntity]] = LockEntity
    sourceType: ClassVar[type[Parameter]] = Parameter


ENTITIES = {
    LockEntityDescription(
        key="settings.lockStatus",
        translation_key="mode",
    ),
}

async_setup_entry = async_setup_entry_factory(ENTITIES)
