from dataclasses import dataclass
from typing import Any, ClassVar

from homeassistant.components import light
from homeassistant.util.scaling import scale_ranged_value_to_int_range

from pyhon.parameter import RangeParameter
from .common import EntityDescription, Entity, async_setup_entry_factory


class LightEntity(Entity[RangeParameter], light.LightEntity):
    entity_description: "LightEntityDescription"

    @property
    def supported_color_modes(self) -> set[str]:
        if len(self._source.values) == 2:
            return {light.ColorMode.ONOFF}
        else:
            return {light.ColorMode.BRIGHTNESS}

    @property
    def is_on(self) -> bool:
        return self._source.value > 0

    @property
    def brightness(self) -> int | None:
        s = self._source
        return scale_ranged_value_to_int_range((s.min, s.max), (0, 255), s.value)

    async def async_set(self, value: int) -> None:
        self._source.value = value

        # TODO: Implement command sending
        # await self._appliance.commands[self.entity_description.key.split(".")[0]].send()

    async def async_turn_on(self, **kwargs: Any) -> None:
        s = self._source

        value = scale_ranged_value_to_int_range(
            (0, 255), (s.min, s.max), kwargs.get(light.ATTR_BRIGHTNESS, 255)
        )

        await self.async_set(value)

    async def async_turn_off(self, **kwargs: Any) -> None:
        await self.async_set(self._source.min)


@dataclass(frozen=True, kw_only=True)
class LightEntityDescription(EntityDescription, light.LightEntityDescription):
    sourceType: ClassVar[type[RangeParameter]] = RangeParameter
    entity_cls: ClassVar[type[LightEntity]] = LightEntity


ENTITIES = {
    LightEntityDescription(
        key="lightStatus",
        name="Light",
    ),
}


async_setup_entry = async_setup_entry_factory(ENTITIES)
