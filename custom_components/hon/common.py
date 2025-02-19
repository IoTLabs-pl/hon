from functools import cached_property
from .const import DOMAIN
from typing import Generic, Iterable, TYPE_CHECKING, Any, TypeVar
from homeassistant.helpers.device_registry import format_mac
from dataclasses import dataclass
from homeassistant.helpers import entity
from homeassistant.helpers.typing import UNDEFINED
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from pyhon.entities.parameter import Parameter
from pyhon.entities.command import Command
from pyhon.entities.observer import Subscriber
# from pyhon.commands import HonCommand as Command

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from pyhon import Hon
    from pyhon.entities.appliance import Appliance

from logging import getLogger

T = TypeVar("T")


_LOGGER = getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EntityDescription(entity.EntityDescription):
    # TODO: Remove entity_cls and introspect the entity class
    # from the EntitySubclasses entity_description fields
    entity_cls: type["Entity"]

    def __post_init__(self):
        key = self.key
        if "." in key:
            """Removes the domain command prefix from the key"""
            key = key.rsplit(".", 1)[-1]

        if key[-1].isdigit() and key[-2] == "Z":
            """Remove zone suffix from the key"""
            key = f"{key[:-2]} {key[-1]}"

        if not self.name or self.name is UNDEFINED:
            """Converts the camelCase key to a human readable name"""
            name = key[0].upper() + "".join(
                f" {c}" if c.isupper() else c for c in key[1:]
            )
            object.__setattr__(self, "name", name)

        if not self.translation_key:
            """Converts the camelCase key to a snake_case translation key"""
            translation_key = "".join(
                f"_{c.lower()}" if c.isupper() else c for c in key
            )
            object.__setattr__(self, "translation_key", translation_key)

@dataclass(frozen=True, kw_only=True)
class CmdParameterEntityDescription(EntityDescription):
    command: str

# TODO: Fix Coordinator data typing
class Entity(Generic[T], CoordinatorEntity[DataUpdateCoordinator[dict[str, Any]]]):
    _attr_has_entity_name = True
    _attr_should_poll = False

    _source: T

    @classmethod
    def try_create(cls, *args, **kwargs):
        try:
            return cls(*args, **kwargs)
        except (AttributeError, KeyError):
            return None

    def __init__(
        self,
        hass: "HomeAssistant",
        entry: "ConfigEntry",
        appliance: "Appliance",
        description: EntityDescription,
    ) -> None:
        self.appliance = appliance
        self.entity_description = description

        if bool(self._source) is False:
            raise KeyError(f"Entity source for key: {description.key} not found")

        mac = format_mac(appliance.data.mac_address)

        self._attr_unique_id = f"{mac}-{description.key}"
        self._attr_device_info = entity.DeviceInfo(
            identifiers={(DOMAIN, mac)},
            manufacturer=appliance.data.brand,
            model_id=str(appliance.data.appliance_model_id),
            model=appliance.data.model_name,
            name=appliance.data.nick_name,
            serial_number=appliance.data.serial_number,
            sw_version=appliance.data.fw_version,
        )

        super().__init__(hass.data[DOMAIN][entry.unique_id]["coordinator"])


class ParameterBasedEntity(Entity[Parameter], Subscriber[Parameter]):
    @cached_property
    def _source(self) -> Parameter:
        s = self.appliance.parameters[self.entity_description.key]
        s.subscribe(self)
        return s

    def update(self, data: Parameter) -> None:
        self.async_write_ha_state()


class RemoteControlEntity(Generic[T], Entity[T]):
    @property
    def available(self) -> bool:
        return (
            super().available
            and (p := self.appliance.parameters.get("remoteCtrValid")) is not None
            and p.data.value == 1
        )
    
class CommandBasedEntity(Entity[Command]):
    @cached_property
    def _source(self) -> Command:
        return self.appliance.commands[self.entity_description.key]


def async_setup_entry_factory(entity_descriptions: Iterable[EntityDescription]):
    async def async_setup_entry(
        hass: "HomeAssistant",
        entry: "ConfigEntry",
        async_add_entities: "AddEntitiesCallback",
    ) -> None:
        hon: "Hon" = hass.data[DOMAIN][entry.unique_id]["hon"]

        async_add_entities(
            entity
            for a in hon.appliances
            for d in entity_descriptions
            if (entity := d.entity_cls.try_create(hass, entry, a, d))
        )

    return async_setup_entry
