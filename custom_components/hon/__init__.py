from functools import partial
import logging

from homeassistant.core import HomeAssistant, Event, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, EVENT_HOMEASSISTANT_STOP
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from pyhon import Hon


from .const import DOMAIN, PLATFORMS, CONF_REFRESH_TOKEN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=DOMAIN,
    )

    hon = await Hon(
        email=entry.data.get(CONF_EMAIL),
        password=entry.data.get(CONF_PASSWORD),
        refresh_token=entry.data.get(CONF_REFRESH_TOKEN),
        enable_mqtt=True,
        autoload=True,
    ).__aenter__()

    hass.data.setdefault(DOMAIN, {}).update(
        {
            entry.unique_id: {
                "hon": hon,
                "coordinator": coordinator,
            }
        }
    )
    hass.bus.async_listen_once(
        EVENT_HOMEASSISTANT_STOP, partial(store_refresh_token, hass, entry, hon)
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


@callback
def store_refresh_token(
    hass: HomeAssistant, entry: ConfigEntry, hon: Hon, event: Event = None
):
    refresh_token = hon._api._session._auth.refresh_token

    _LOGGER.debug("Storing refresh token: %s", refresh_token)

    hass.config_entries.async_update_entry(
        entry, data={**entry.data, CONF_REFRESH_TOKEN: refresh_token}
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry_data = hass.data[DOMAIN][entry.unique_id]
    hon: Hon = entry_data["hon"]

    store_refresh_token(hass, entry, hon)
    unload = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload:
        await hon.__aexit__()
        if not hass.data[DOMAIN]:
            hass.data.pop(DOMAIN, None)
    return unload
