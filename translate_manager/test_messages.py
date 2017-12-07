from django.contrib.auth.models import User
from .models import *

from django.test import TestCase
from .messages import *

class Message_Test(TestCase):
    def test_Encode_Project_MSG(self):
        s = project_msg2json_str( MSG_NOTIFY_TYPE_ASK_ACCEPT_ID, arg_project_id = '21', arg_project_name = 'some project' )
        self.assertEqual( s, '{"msg_type": 1, "project_id": "21", "project_name": "some project"}' )

    def test_Encode_Decode_Project_MSG(self):
        s = project_msg2json_str( MSG_NOTIFY_TYPE_ASK_ACCEPT_ID, arg_project_id = '21', arg_project_name = 'some project' )
        self.assertEqual( decode_json2msg(s), "You are asked to accept the membership of 'some project' project team!" )

    def test_Encode_Project_MSG_Fail(self):
        s = project_msg2json_str( -1, arg_project_name = '*' )
        self.assertFalse( s )