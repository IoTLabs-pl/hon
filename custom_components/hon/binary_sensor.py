from dataclasses import dataclass
from typing import ClassVar
from homeassistant.components import binary_sensor

from .common import async_setup_entry_factory, EntityDescription, ParameterBasedEntity


class BinarySensorEntity(
    ParameterBasedEntity,
    binary_sensor.BinarySensorEntity,
):
    entity_description: "BinarySensorEntityDescription"

    @property
    def is_on(self) -> bool:
        return bool(self._source.data.value) != self.entity_description.inverted


@dataclass(frozen=True, kw_only=True)
class BinarySensorEntityDescription(
    EntityDescription,
    binary_sensor.BinarySensorEntityDescription,
):
    inverted: bool = False
    entity_cls: ClassVar[type[BinarySensorEntity]] = BinarySensorEntity


_DeviceClass = binary_sensor.BinarySensorDeviceClass

# TODO: Should entities names be suffixed with "Status"?
ENTITIES = [
    BinarySensorEntityDescription(
        key="ch2oCleaningStatus",
    ),
    # TODO: Generic appliance data cluster not implemented
    # BinarySensorEntityDescription(
    #     name="Connection",
    #     device_class=_DeviceClass.CONNECTIVITY,
    #     value_picker=lambda a: a.connected,
    # ),
    BinarySensorEntityDescription(
        key="doorLockStatus",
        device_class=_DeviceClass.LOCK,
        inverted=True,
    ),
    *(
        BinarySensorEntityDescription(
            key=f"door{i}StatusZ{zone}".removesuffix("Z0"),
            name=f"{name} Door {i}".strip(),
            device_class=_DeviceClass.DOOR,
            icon=icon,
            translation_key=f"door_{name}".removesuffix("_").lower(),
        )
        for i in ("", "2")
        for zone, (name, icon) in enumerate(
            (
                ("", None),
                ("Fridge", "mdi:fridge-top"),
                ("Freezer", "mdi:fridge-bottom"),
            ),
        )
    ),
    BinarySensorEntityDescription(
        key="filterChangeStatusLocal",
        # name="Filter Replacement",
        device_class=_DeviceClass.PROBLEM,
    ),
    BinarySensorEntityDescription(
        key="hobLockStatus",
        device_class=_DeviceClass.LOCK,
        inverted=True,
    ),
    BinarySensorEntityDescription(
        key="holidayMode",
        icon="mdi:palm-tree",
        device_class=_DeviceClass.RUNNING,
    ),
    BinarySensorEntityDescription(
        key="hotStatus",
        device_class=_DeviceClass.HEAT,
        # translation_key="still_hot",
    ),
    BinarySensorEntityDescription(
        key="intelligenceMode",
        icon="mdi:thermometer-auto",
        device_class=_DeviceClass.RUNNING,
        # translation_key="auto_set",
    ),
    BinarySensorEntityDescription(
        key="onOffStatus",
        device_class=_DeviceClass.RUNNING,
        icon="mdi:power-cycle",
    ),
    BinarySensorEntityDescription(
        key="panStatus",
        icon="mdi:pot-mix",
    ),
    BinarySensorEntityDescription(
        key="rinseAidStatus",
        device_class=_DeviceClass.PROBLEM,
        icon="mdi:spray-bottle",
    ),
    BinarySensorEntityDescription(
        key="saltStatus",
        device_class=_DeviceClass.PROBLEM,
        icon="mdi:shaker-outline",
    ),
    *(
        BinarySensorEntityDescription(
            key=f"quickModeZ{zone}",
            # name=name,
            icon=icon,
            device_class=_DeviceClass.RUNNING,
        )
        for zone, (name, icon) in enumerate(
            (
                ("Super Cool", "mdi:snowflake"),
                ("Super Freeze", "mdi:snowflake-variant"),
            ),
            1,
        )
    ),
]

async_setup_entry = async_setup_entry_factory(ENTITIES)
