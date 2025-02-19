from dataclasses import dataclass
from typing import ClassVar
from homeassistant.components import select, sensor
from homeassistant.helpers.entity import EntityCategory
from pyhon.parameter import EnumParameter

from . import units
from .common import (
    async_setup_entry_factory,
    Entity,
    EntityDescription,
    CmdParameterEntityDescription,
    RemoteControlEntity,
)

_DeviceClass = sensor.const.SensorDeviceClass


class SelectEntity(Entity[EnumParameter], select.SelectEntity):
    entity_description: "SelectEntityDescription"

    @property
    def options(self):
        return self._source.values

    @property
    def current_option(self) -> str | None:
        return self._source.value

    async def async_select_option(self, option):
        self._source.value = option
        self.async_write_ha_state()


# class ConfigSelectEntity(RemoteControlEntity, SelectEntity):
#     pass

    # TODO: What async_select option should really do?
    # async def async_select_option(self, option: str) -> None:
    #     setting = self._appliance.settings[self.entity_description.key]
    #     setting.value = self._option_to_number(option, setting.values)
    #     command = self.entity_description.key.split(".")[0]
    #     await self._appliance.commands[command].send()
    #     if command != "settings":
    #         self._appliance.sync_command(command, "settings")
    #     self.coordinator.async_set_updated_data({})


@dataclass(frozen=True, kw_only=True)
class SelectEntityDescription(CmdParameterEntityDescription, select.SelectEntityDescription):
    # translation_table: TranslationTable = TranslationTable()
    entity_cls: ClassVar[type[SelectEntity]] = SelectEntity
    command: ClassVar[str] = "settings"


@dataclass(frozen=True, kw_only=True)
class ConfigSelectEntityDescription(SelectEntityDescription):
    command: ClassVar[str] = "startProgram"
    entity_category: ClassVar[EntityCategory] = EntityCategory.CONFIG


ENTITIES = {
    ConfigSelectEntityDescription(
        key="program",
        # translation_key=f"programs_{slug}",
    ),
    ConfigSelectEntityDescription(
        key="temp",
        # name="Temperature",
        icon="mdi:thermometer",
        device_class=_DeviceClass.TEMPERATURE,
        unit_of_measurement=units.CELSIUS,
    ),
    ConfigSelectEntityDescription(
        key="spinSpeed",
        icon="mdi:numeric",
        unit_of_measurement=units.REVOLUTIONS_PER_MINUTE,
    ),
    ConfigSelectEntityDescription(
        key="steamLevel",
        icon="mdi:weather-dust",
        # translation_table=STEAM_LEVEL,
    ),
    ConfigSelectEntityDescription(
        key="dirtyLevel",
        icon="mdi:liquid-spot",
        # translation_table=DIRTY_LEVEL,
    ),
    ConfigSelectEntityDescription(
        key="extendedStainType",
        # name="Stain Type",
        icon="mdi:liquid-spot",
    ),
    ConfigSelectEntityDescription(
        key="waterLevel",
        # name="Dry Time",
        icon="mdi:timer",
        unit_of_measurement=units.MINUTES,
    ),
    ConfigSelectEntityDescription(
        key="dryLevel",
        icon="mdi:hair-dryer",
        # translation_key="dry_levels",
        # translation_table=DRY_LEVEL,
    ),
    ConfigSelectEntityDescription(
        key="zone",
        icon="mdi:radiobox-marked",
        # translation_key="ref_zones",
    ),
    SelectEntityDescription(
        key="tempSelZ3",
        # name="Temperature",
        icon="mdi:thermometer",
        unit_of_measurement=units.CELSIUS,
    ),
    ConfigSelectEntityDescription(
        key="remainingTime",
        icon="mdi:timer",
        unit_of_measurement=units.MINUTES,
    ),
    SelectEntityDescription(
        key="aromaStatus",
        # name="Diffuser Level",
        icon="mdi:air-purifier",
        # translation_table=DIFFUSER_LEVEL,
        # translation_key="diffuser",
    ),
    SelectEntityDescription(
        key="machMode",
        # name="Mode",
        icon="mdi:play",
        # translation_table=MACH_MODE,
    ),
    SelectEntityDescription(
        key="humanSensingStatus",
        # name="Eco Pilot",
        icon="mdi:run",
        # translation_table=HUMAN_SENSE,
    ),
    SelectEntityDescription(
        key="windDirectionHorizontal",
        # name="Fan Direction Horizontal",
        icon="mdi:fan",
        translation_key="fan_horizontal",
        # translation_table=POSITION_HORIZONTAL,
    ),
    SelectEntityDescription(
        key="windDirectionVertical",
        # name="Fan Direction Vertical",
        icon="mdi:fan",
        translation_key="fan_vertical",
        # translation_table=POSITION_VERTICAL,
    ),
}


async_setup_entry = async_setup_entry_factory(ENTITIES)
