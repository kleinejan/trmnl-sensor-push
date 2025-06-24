"""Platform for TRMNL Sensor Push integration."""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.helpers.template import Template

# Get the logger
_LOGGER = logging.getLogger(__name__)

def get_trmnl_entities(hass: HomeAssistant):
    """Get entities with TRMNL label using template."""
    template_str = "{{ label_entities('TRMNL') }}"
    template = Template(template_str, hass)
    return template.async_render()

def setup_platform(hass: HomeAssistant, entry) -> None:
    """Set up the TRMNL Sensor Push platform."""
    def process_trmnl_entities():
        """Find and process entities with TRMNL label."""
        # Get all entities with the TRMNL label
        trmnl_entities = get_trmnl_entities(hass)
        
        # Log the number of TRMNL entities found
        _LOGGER.info(f"Found {len(trmnl_entities)} entities with TRMNL label")
        
        # Log the names of these entities
        for entity_id in trmnl_entities:
            _LOGGER.debug(f"TRMNL Entity Found: {entity_id}")

    # Run the processing function
    hass.add_job(process_trmnl_entities)
