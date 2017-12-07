from django.contrib.auth.models import User
from .models import *

from django.test import TestCase

USER_TEST_NAME = 'USER TEST NAME'
USER_TEST_PW   = '123'

class Profile_Test(TestCase):
    def setUp(self):
        if not User.objects.filter( username = USER_TEST_NAME ).exists():
            test_user = User.objects.create_user( username = USER_TEST_NAME, password = USER_TEST_PW )            

    def test_User_notifications_Zero(self):
        u = User.objects.get(username=USER_TEST_NAME)
        self.assertEqual( GetUserNoticationsQ( u, True).count(), 0 )

from django.test import Client
class Profile_Test_Client(TestCase):
    def test_Profile_Test_Client_Root(self):
        c = Client()
        response = c.post( '/webapi/get_my_profile/?format=json' )
        self.assertEqual( response.status_code, 403 ) # we are not authorized - login required

class Profile_Test_Client_Try_Wrong_Login(TestCase):
    def test_Profile_Test_Client_Root(self):
        c = Client()        
        res = c.login(username='perfect_stranger', password='yaoyao!')
        self.assertFalse( res )