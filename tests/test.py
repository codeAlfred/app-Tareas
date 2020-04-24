import unittest
from flask import current_app
from app import db, User, Task
from app import create_app

from config import config

class DemoTestCase(unittest.TestCase):
    def setUp(self):
        config_class = config['test']
        # generar nuestra aplicacion
        self.app = create_app(config_class)
        # definimos un id
        self.id=1
    
    def tearDown(self):
        # eliminar todas nuestras tablas despues de cada prueba
        db.drop_all()
        db.session.remove()
    
    def test_demo(self):
        self.assertTrue(1==1)
        
    def test_user_existes(self):
        user = User.get_by_id(self.id)
        self.assertTrue(User is None)
        
        # falta terminar las pruebas-falta configrar el error con bluepreint y bootstrap
