# TODO: Implement native HA diagnostics interface
from dataclasses import dataclass
from typing import ClassVar
# from pathlib import Path
# import yaml

# from homeassistant.components import persistent_notification
from homeassistant.components import button
# from homeassistant.helpers.entity import EntityCategory

from .common import (
    async_setup_entry_factory,
    # Entity,
    RemoteControlEntity,
    CommandBasedEntity,
    EntityDescription,
    Command
)



# _DATA_ARCHIVE_NOTIFICATION_MESSAGE = "\n\n".join(
#     (
#         '<a href="/local/{path}" target="_blank">{path}</a>',
#         "Use this data for [GitHub Issues of Haier hOn](https://github.com/IoTLabs-pl/hon).",
#         "Or add it to the [hon-test-data collection](https://github.com/IoTLabs-pl/hon-test-data).",
#     )
# )


# _DEVICE_INFO_NOTIFICATION_MESSAGE = "\n".join(
#     (
#         "**Warning!** The data below is not anonymized and may contain personal information. "
#         "Please be careful with sharing it.",
#         "```",
#         "{diagnostic_info}",
#         "```",
#     )
# )


# class DiagnosticButtonEntity(Entity, button.ButtonEntity):
#     entity_description: "ButtonEntityDescription"


class ButtonEntity(CommandBasedEntity, button.ButtonEntity):
    entity_description: "ButtonEntityDescription"

    async def async_press(self) -> None:
        payload = self._source.create_payload_template()
        await self._source.execute(payload)


# class DataArchiveButtonEntity(DiagnosticButtonEntity):
#     async def async_press(self) -> None:
#         output_path = Path(self.hass.config.config_dir) / "www"

#         # TODO: import asynchronously
#         from pyhon.diagnostic import Diagnoser

#         # TODO: This call does not give factory call
#         # i.e. first call to Haier servers with all devices belonging
#         # to the user. Consider to implement partial dumps in pyhon diagnostics
#         await Diagnoser(self._appliance).api_dump(output_path, as_zip=True)

#         persistent_notification.create(
#             self.hass,
#             title=f"{self._appliance.nick_name} Data Archive",
#             message=_DATA_ARCHIVE_NOTIFICATION_MESSAGE.format(path=output_path),
#         )


# class DeviceInfoButtonEntity(ButtonEntity):
#     async def async_press(self):
#         # TODO: import asynchronously
#         from pyhon.diagnostic import Diagnoser

#         device_info = await Diagnoser(self._appliance).as_dict(anonymous=False)

#         persistent_notification.create(
#             self.hass,
#             title=f"{self._appliance.nick_name} Device Info",
#             message=_DEVICE_INFO_NOTIFICATION_MESSAGE.format(
#                 # TODO: Investigate, why .replace(" ", "\u200b ") was used?
#                 device_info=yaml.dump(device_info)
#             ),
#         )


@dataclass(frozen=True, kw_only=True)
class ButtonEntityDescription(EntityDescription, button.ButtonEntityDescription):
    entity_cls: ClassVar[type["ButtonEntity"]] = ButtonEntity


ENTITIES = {
    ButtonEntityDescription(
        key="startProgram",
        icon="mdi:play",
    ),
    ButtonEntityDescription(
        key="stopProgram",
        icon="mdi:stop",
    ),
    # ButtonEntityDescription(
    #     name="Create Data Archive",
    #     icon="mdi:archive-arrow-down",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     entity_registry_enabled_default=False,
    #     entity_cls=DataArchiveButtonEntity,
    # ),
    # ButtonEntityDescription(
    #     name="Show Device Info",
    #     icon="mdi:information",
    #     entity_category=EntityCategory.DIAGNOSTIC,
    #     entity_registry_enabled_default=False,
    #     entity_cls=DeviceInfoButtonEntity,
    # ),
}

async_setup_entry = async_setup_entry_factory(ENTITIES)
