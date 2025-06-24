"""The TRMNL Entity Push integration."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta
import asyncio
import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.template import Template

from .const import DOMAIN, MIN_TIME_BETWEEN_UPDATES
#from .trmnl_sensor_push import label_entities

_LOGGER = logging.getLogger(__name__)

# Since this integration only supports config entries, use this schema
CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

def create_entity_payload(state) -> dict:
    """Create the payload for a single entity."""
    payload = {
        "name": state.attributes.get('friendly_name', state.entity_id),
        "value": state.state,
        "device_class": state.attributes.get('device_class', None),
        "unit_of_measurement": state.attributes.get('unit_of_measurement', None),
        "icon": state.attributes.get('icon', None),
        "friendly_name": state.attributes.get('friendly_name', state.entity_id),
        "attributes": state.attributes
    }
    _LOGGER.debug("TRMNL: Created payload for %s: %s", state.entity_id, payload)
    return payload

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the TRMNL Entity Push component."""
    _LOGGER.debug("TRMNL: Setting up TRMNL Entity Push component")
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up TRMNL Entity Push from a config entry."""
    _LOGGER.debug("TRMNL: Setting up config entry")
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {}

    url = entry.data["url"]
    _LOGGER.debug("TRMNL: Using webhook URL: %s", url)

    def get_trmnl_entities():
        """Get entities with TRMNL label using template."""
        _LOGGER.debug("TRMNL: Fetching entities with TRMNL label")
        template_str = "{{ label_entities('TRMNL') }}"
        template = Template(template_str, hass)
        result = template.async_render()
        _LOGGER.debug("TRMNL: Template rendered result: %s", result)
        return result

    async def process_trmnl_entities(*_):
        """Find and process entities with TRMNL label."""
        _LOGGER.debug("TRMNL: Starting entity processing")
        # Get all entities with the TRMNL label
        trmnl_entities = get_trmnl_entities()

        # if 0 entities found log error, return
        if len(trmnl_entities) == 0:
            _LOGGER.error("TRMNL: No entities found with TRMNL label")
            return

        # Log the number of TRMNL entities found
        _LOGGER.info("TRMNL: Found %d entities with TRMNL label", len(trmnl_entities))

        # Create payload for each entity
        entities_payload = []
        for entity_id in trmnl_entities:
            state = hass.states.get(entity_id)
            if state:
                _LOGGER.debug("TRMNL: Processing entity: %s", entity_id)
                entities_payload.append(create_entity_payload(state))

        # Send to TRMNL webhook if we have entities
        if entities_payload:
            payload = {
                "merge_variables": {
                    "entities": entities_payload
                }
            }
            _LOGGER.debug("TRMNL: Preparing to send payload: %s", payload)
            
            try:
                async with aiohttp.ClientSession() as session:
                    _LOGGER.debug("TRMNL: Sending POST request to %s", url)
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            _LOGGER.info("TRMNL: Successfully sent data to webhook")
                            _LOGGER.debug("TRMNL: Webhook response: %s", await response.text())
                        else:
                            _LOGGER.error("TRMNL: Error sending to webhook: %s", response.status)
                            response_text = await response.text()
                            _LOGGER.error("TRMNL: Response: %s", response_text)
            except Exception as err:
                _LOGGER.error("TRMNL: Failed to send data to webhook: %s", err)
        else:
            _LOGGER.debug("TRMNL: No entities to send")

    # Set up periodic timer
    _LOGGER.debug("TRMNL: Setting up periodic timer for %d seconds", MIN_TIME_BETWEEN_UPDATES)
    remove_timer = async_track_time_interval(
        hass,
        process_trmnl_entities,
        timedelta(seconds=MIN_TIME_BETWEEN_UPDATES)
    )

    # Store the timer removal function
    hass.data[DOMAIN][entry.entry_id]["remove_timer"] = remove_timer

    # Run initial scan
    _LOGGER.debug("TRMNL: Running initial entity scan")
    await process_trmnl_entities()

    _LOGGER.info("TRMNL: Integration setup completed for URL: %s", url)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        # Remove the timer
        if entry.entry_id in hass.data[DOMAIN]:
            _LOGGER.debug("TRMNL: Removing timer and cleaning up")
            hass.data[DOMAIN][entry.entry_id]["remove_timer"]()
            hass.data[DOMAIN].pop(entry.entry_id)
            _LOGGER.info("TRMNL: Successfully unloaded integration")
    except Exception as err:
        _LOGGER.error("TRMNL: Error unloading integration: %s", err)
        return False
    return True