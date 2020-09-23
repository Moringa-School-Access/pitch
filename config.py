import os


class Config:
    """
    General configuration parent class
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://moringa:alex17176251@localhost/pitches'
    SECRET_KEY = 'alexotieno900'
    UPLOADED_PHOTOS_DEST = 'app/static/photos'


class ProdConfig(Config):
    """
    Production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig,
}
