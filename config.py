# configuraciones globales
class Config:
    SECRET_KEY = 'codigofacilito'


# configuraciones especificas para el entorno de desarrollo
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/project_python_web'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/project_python_web_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig,
    'test':TestConfig
}