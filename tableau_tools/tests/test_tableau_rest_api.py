#!/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from ..tableau_rest_api.tableau_rest_api_connection import TableauRestApiConnection

import io
import json

import unittest
import mock
import requests

class TestTableauRestApi(unittest.TestCase):

    def setUp(self):
        self.server = 'http://127.0.0.1'
        self.username = 'user'
        self.password = 'pass'
        self.tableau_api_connection = TableauRestApiConnection(
            self.server, self.username, self.password )
        # patcher_restapi_33 = mock.patch('common.TableauRestApiConnection33', autospec=True)
        # self.mock_restapi_33 = patcher_restapi_33.start()
        # self.addCleanup(patcher_restapi_33.stop)

        # spring_profiles_list = [e.strip() for e in self.config.get_required_value('spring', ['profiles']).split(',')]

        # self.tableau_server = connect_to_tableau_server(self.tableau_config, None)
        # self.deploy_config = DeployConfig(spring_profiles_list, self.tableau_config, self.projects_path, self.tableau_server, 'test_tag', None)

    def test__create_connection_credentials(self):
        username = 'a'
        password = 'b'
        oauth_flag = False
        save_credentials = False
        cc = self.tableau_api_connection._create_connection_credentials(username, password, oauth_flag, save_credentials)
        self.assertEquals(username, cc.get('name'))
        self.assertEquals(password, cc.get('password'))
        self.assertEquals('false', cc.get('embed'))
        self.assertIsNone(cc.get('oAuth'))

        password = None
        cc = self.tableau_api_connection._create_connection_credentials(username, password, oauth_flag, save_credentials)
        self.assertEquals(username, cc.get('name'))
        self.assertIsNone(cc.get('password'))
        self.assertEquals('false', cc.get('embed'))
        self.assertIsNone(cc.get('oAuth'))

        oauth_flag = True
        cc = self.tableau_api_connection._create_connection_credentials(username, password, oauth_flag, save_credentials)
        self.assertEquals(username, cc.get('name'))
        self.assertIsNone(cc.get('password'))
        self.assertEquals('false', cc.get('embed'))
        self.assertEquals('True', cc.get('oAuth'))

        save_credentials = True
        cc = self.tableau_api_connection._create_connection_credentials(username, password, oauth_flag, save_credentials)
        self.assertEquals(username, cc.get('name'))
        self.assertIsNone(cc.get('password'))
        self.assertEquals('true', cc.get('embed'))
        self.assertEquals('True', cc.get('oAuth'))

if __name__ == '__main__':
    unittest.main()