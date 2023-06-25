from mongoengine import Document, FloatField, StringField


class Configuration(Document):
    approx_lat = FloatField(min_value=-90, max_value=90)
    approx_lon = FloatField(min_value=-180, max_value=180)
    config_file = StringField(default='', null=True)
    pio_env = StringField(default='', null=True)
    release_version = StringField(default='', null=True)
    uuid = StringField()
