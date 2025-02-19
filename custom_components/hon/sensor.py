from dataclasses import dataclass, replace

from homeassistant.components import sensor

from .common import (
    async_setup_entry_factory,
    Entity,
    EntityDescription,
    ParameterBasedEntity,
)

from typing import ClassVar
from . import units

_DeviceClass = sensor.const.SensorDeviceClass
_StateClass = sensor.const.SensorStateClass


class SensorEntity(ParameterBasedEntity, sensor.SensorEntity):
    entity_description: "SensorEntityDescription"

    @property
    def native_value(self):
        return self._source.data.value


@dataclass(frozen=True, kw_only=True)
class SensorEntityDescription(
    EntityDescription,
    sensor.SensorEntityDescription,
):
    entity_cls: ClassVar[type[Entity]] = SensorEntity


def with_zones(*desc: SensorEntityDescription):
    yield from desc
    yield from (
        replace(d, name=f"{d.name} {i}", key=f"{d.key}Z{i}")
        for d in desc
        for i in range(1, 4)
    )


ENTITIES = {
    SensorEntityDescription(
        key="airQuality",
        icon="mdi:weather-dust",
    ),
    SensorEntityDescription(
        key="coLevel",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.CO,
        native_unit_of_measurement=units.CONCENTRATION_PARTS_PER_MILLION,
    ),
    SensorEntityDescription(
        key="currentElectricityUsed",
        # translation_key="energy_current",
        device_class=_DeviceClass.ENERGY,
        native_unit_of_measurement=units.KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="currentWaterUsed",
        # translation_key="water_current",
        device_class=_DeviceClass.WATER,
        state_class=_StateClass.TOTAL_INCREASING,
        native_unit_of_measurement=units.LITERS,
    ),
    SensorEntityDescription(
        key="delayTime",
        icon="mdi:clock-start",
        native_unit_of_measurement=units.MINUTES,
    ),
    SensorEntityDescription(
        key="delayTimeStatus",
        icon="mdi:clock-start",
    ),
    SensorEntityDescription(
        key="dirtyLevel",
        icon="mdi:liquid-spot",
    ),
    SensorEntityDescription(
        key="dryLevel",
        icon="mdi:hair-dryer",
        # translation_key="dry_levels",
    ),
    SensorEntityDescription(
        key="errors",
        icon="mdi:math-log",
    ),
    SensorEntityDescription(
        key="fanSpeed",
        icon="mdi:fan",
    ),
    # TODO: Should be moved to binary_sensor?
    SensorEntityDescription(
        key="filterCleaningAlarmStatus",
    ),
    SensorEntityDescription(
        key="filterCleaningStatus",
    ),
    SensorEntityDescription(
        key="filterLife",
        icon="mdi:air-filter",
        native_unit_of_measurement=units.PERCENTAGE,
    ),
    *(
        SensorEntityDescription(
            key=f"humidity{k}",
            state_class=_StateClass.MEASUREMENT,
            device_class=_DeviceClass.HUMIDITY,
            native_unit_of_measurement=units.PERCENTAGE,
            # translation_key="humidity",
        )
        for k, name in (
            ("Indoor", ""),
            ("Env", "Room"),
        )
    ),
    *with_zones(
        SensorEntityDescription(
            key="humidity",
            state_class=_StateClass.MEASUREMENT,
            device_class=_DeviceClass.HUMIDITY,
            native_unit_of_measurement=units.PERCENTAGE,
        ),
    ),
    SensorEntityDescription(
        key="humidityLevel",
        icon="mdi:water-outline",
    ),
    # TODO: Should be formatted as time?
    SensorEntityDescription(
        key="lastWorkTime",
        icon="mdi:clock-start",
    ),
    SensorEntityDescription(
        key="lightStatus",
        icon="mdi:lightbulb",
    ),
    SensorEntityDescription(
        key="machMode",
        # translation_key="washing_modes",
        icon="mdi:information",
    ),
    SensorEntityDescription(
        key="pm10ValueIndoor",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.PM10,
        native_unit_of_measurement=units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    SensorEntityDescription(
        key="pm2p5ValueIndoor",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.PM25,
        native_unit_of_measurement=units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
    SensorEntityDescription(
        key="power",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.POWER,
    ),
    # TODO: Should be supported for
    # wm, td, ov, ih, dw, ac, wc
    SensorEntityDescription(
        key="prCode",
        # name="Program",
        icon="mdi:play",
        # TODO: Options
        # translation_key="programs_wm",
    ),
    # TODO: Should be supported for
    # wm, td, dw
    SensorEntityDescription(
        key="prPhase",
        # name="Program Phase",
        # translation_key="program_phases_wm",
        icon="mdi:washing-machine",
    ),
    SensorEntityDescription(
        key="preFilterStatus",
        icon="mdi:air-filter",
        # translation_key="filter_cleaning",
        native_unit_of_measurement=units.PERCENTAGE,
    ),
    SensorEntityDescription(
        key="quickDelayTimeStatus",
    ),
    SensorEntityDescription(
        key="remainingTimeMM",
        # name="Remaining Time",
        device_class=_DeviceClass.DURATION,
        native_unit_of_measurement=units.MINUTES,
    ),
    SensorEntityDescription(
        key="rgbLightColor",
        # name="RGB Light Color",
        icon="mdi:lightbulb",
    ),
    SensorEntityDescription(
        key="rgbLightStatus",
        # name="RGB Light Status",
        icon="mdi:lightbulb",
    ),
    SensorEntityDescription(
        key="spinSpeed",
        icon="mdi:speedometer",
        native_unit_of_measurement=units.REVOLUTIONS_PER_MINUTE,
    ),
    SensorEntityDescription(
        key="stainType",
        icon="mdi:liquid-spot",
    ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.ecoIndex",
    #     icon="mdi:sprout",
    #     state_class=_StateClass.MEASUREMENT,
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.energyLabel",
    #     icon="mdi:lightning-bolt-circle",
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.liquidDetergentDose",
    #     icon="mdi:cup-water",
    #     translation_key="det_liquid",
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.powderDetergentDose",
    #     icon="mdi:cup",
    #     translation_key="det_dust",
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.remainingTime",
    #     name="Program Time",
    #     device_class=_DeviceClass.DURATION,
    #     native_unit_of_measurement=units.MINUTES,
    # ),
    #     ConfigSensorEntityDescription(
    #     key="startProgram.temp",
    #     name="Temperature",
    #     state_class=_StateClass.MEASUREMENT,
    #     device_class=_DeviceClass.TEMPERATURE,
    #     native_unit_of_measurement=units.CELSIUS,
    # ),
    # *(
    #     ConfigSensorEntityDescription(
    #         key=f"startProgram.suggestedLoad{suffix}",
    #         name="Suggested Load",
    #         device_class=_DeviceClass.WEIGHT,
    #         native_unit_of_measurement=units.KILOGRAMS,
    #     )
    #     for suffix in ("", "W", "D")
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.waterEfficiency",
    #     icon="mdi:water",
    #     state_class=_StateClass.MEASUREMENT,
    # ),
    # ConfigSensorEntityDescription(
    #     key="startProgram.waterSaving",
    #     icon="mdi:water-percent",
    #     state_class=_StateClass.MEASUREMENT,
    #     native_unit_of_measurement=units.PERCENTAGE,
    # ),
    SensorEntityDescription(
        key="steamLevel",
        icon="mdi:weather-dust",
    ),
    SensorEntityDescription(
        key="steamType",
        icon="mdi:weather-dust",
    ),
    *with_zones(
        SensorEntityDescription(
            key="temp",
            name="Temperature",
            state_class=_StateClass.MEASUREMENT,
            device_class=_DeviceClass.TEMPERATURE,
            native_unit_of_measurement=units.CELSIUS,
        ),
    ),
    *(
        SensorEntityDescription(
            key=f"temp{part}{area}",
            # name=f"{part} {area} Temperature".strip(),
            state_class=_StateClass.MEASUREMENT,
            device_class=_DeviceClass.TEMPERATURE,
            native_unit_of_measurement=units.CELSIUS,
        )
        for area in ("Indoor", "Outdoor")
        for part in ("", "Coiler", "Air", "Defrost", "In Air")
    ),
    SensorEntityDescription(
        key="tempEnv",
        # name="Room Temperature",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.TEMPERATURE,
        native_unit_of_measurement=units.CELSIUS,
    ),
    SensorEntityDescription(
        key="tempLevel",
        name="Temperature level",
        icon="mdi:thermometer",
        # TODO: Probably enum
        # translation_key="tumbledryertemplevel",
    ),
    *with_zones(
        SensorEntityDescription(
            key="tempSel",
            name="Selected Temperature",
            translation_key="target_temperature",
            state_class=_StateClass.MEASUREMENT,
            device_class=_DeviceClass.TEMPERATURE,
            native_unit_of_measurement=units.CELSIUS,
        ),
    ),
    SensorEntityDescription(
        key="totalElectricityUsed",
        # translation_key="energy_total",
        state_class=_StateClass.TOTAL_INCREASING,
        device_class=_DeviceClass.ENERGY,
        native_unit_of_measurement=units.KILO_WATT_HOUR,
    ),
    SensorEntityDescription(
        key="totalWaterUsed",
        # translation_key="water_total",
        state_class=_StateClass.TOTAL_INCREASING,
        device_class=_DeviceClass.WATER,
        native_unit_of_measurement=units.LITERS,
    ),
    SensorEntityDescription(
        key="totalWashCycle",
        # translation_key="cycles_total",
        icon="mdi:counter",
        state_class=_StateClass.TOTAL_INCREASING,
    ),
    SensorEntityDescription(
        key="totalWorkTime",
        native_unit_of_measurement=units.MINUTES,
        device_class=_DeviceClass.DURATION,
    ),
    SensorEntityDescription(
        key="vocValueIndoor",
        # name="VOC",
        state_class=_StateClass.MEASUREMENT,
        device_class=_DeviceClass.VOLATILE_ORGANIC_COMPOUNDS,
        native_unit_of_measurement=units.CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    ),
}

async_setup_entry = async_setup_entry_factory(ENTITIES)
