import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    UNIT_PERCENT,
    DEVICE_CLASS_BATTERY,
    ICON_BATTERY,
    DEVICE_CLASS_TEMPERATURE,
    UNIT_CELSIUS,
    STATE_CLASS_MEASUREMENT,
)
from . import WavinAHC9000

CONF_PARENT_ID = "wavin_ahc9000_id"
CONF_CHANNEL = "channel"
CONF_TYPE = "type"

SENSOR_TYPES = {
    "battery": sensor.sensor_schema(
        unit_of_measurement=UNIT_PERCENT,
        device_class=DEVICE_CLASS_BATTERY,
        icon=ICON_BATTERY,
        accuracy_decimals=0,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "comfort_setpoint": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_min_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
    "floor_max_temperature": sensor.sensor_schema(
        unit_of_measurement=UNIT_CELSIUS,
        device_class=DEVICE_CLASS_TEMPERATURE,
        accuracy_decimals=1,
        state_class=STATE_CLASS_MEASUREMENT,
    ),
}

def _validate(config):
    sensor_type = config[CONF_TYPE]
    schema = SENSOR_TYPES[sensor_type].extend({
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*SENSOR_TYPES.keys(), lower=True),
    })
    return schema(config)

CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
    cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
    cv.Required(CONF_TYPE): cv.one_of(*SENSOR_TYPES.keys(), lower=True),
    cv.Optional("name"): cv.string,
}).extend(cv.COMPONENT_SCHEMA)

CONFIG_SCHEMA = cv.All(
    sensor.sensor_schema().extend({
        cv.GenerateID(CONF_PARENT_ID): cv.use_id(WavinAHC9000),
        cv.Required(CONF_CHANNEL): cv.int_range(min=1, max=16),
        cv.Required(CONF_TYPE): cv.one_of(*SENSOR_TYPES.keys(), lower=True),
    }),
    _validate,
)

async def to_code(config):
    hub = await cg.get_variable(config[CONF_PARENT_ID])
    sens = await sensor.new_sensor(config)
    sensor_type = config[CONF_TYPE]
    if sensor_type == "battery":
        cg.add(hub.add_channel_battery_sensor(config[CONF_CHANNEL], sens))
    elif sensor_type == "comfort_setpoint":
        cg.add(hub.add_channel_comfort_setpoint_sensor(config[CONF_CHANNEL], sens))
    elif sensor_type == "floor_temperature":
        cg.add(hub.add_channel_floor_temperature_sensor(config[CONF_CHANNEL], sens))
    elif sensor_type == "floor_min_temperature":
        cg.add(hub.add_channel_floor_min_temperature_sensor(config[CONF_CHANNEL], sens))
    elif sensor_type == "floor_max_temperature":
        cg.add(hub.add_channel_floor_max_temperature_sensor(config[CONF_CHANNEL], sens))
    else:
        cg.add(hub.add_channel_temperature_sensor(config[CONF_CHANNEL], sens))
    cg.add(hub.add_active_channel(config[CONF_CHANNEL]))
