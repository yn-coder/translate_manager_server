from django.contrib.auth.models import User
from .models import *

from django.test import TestCase

USER_TEST_NAME = 'SOME USER TEST NAME'
USER_TEST_PW   = '123'

class Project_Test(TestCase):
    def setUp(self):
        if not User.objects.filter( username = USER_TEST_NAME ).exists():
            test_user = User.objects.create_user( username = USER_TEST_NAME, password = USER_TEST_PW )

    def test_User_Member_Zero(self):
        p = Project(shortname='PROJECT_NAME')
        p.save()
        self.assertEqual( p.Get_Members().count(), 0 )

    def test_User_Member_One(self):
        p1 = Project(shortname='PROJECT_NAME #1')
        p1.save()
        a = Assignment( project = p1, assigned_user = User.objects.get( username = USER_TEST_NAME ) )
        a.save()
        self.assertEqual( p1.Get_Members().count(), 1 )