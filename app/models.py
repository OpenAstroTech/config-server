from mongoengine import *


class Configuration(Document):
    lat = FloatField(min_value=-90, max_value=90)
    lon = FloatField(min_value=-180, max_value=180)
    config_file = StringField()
    pio_env = StringField()
    release_version = StringField()
    uuid = StringField()
