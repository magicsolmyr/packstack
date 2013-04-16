# -*- coding: utf-8 -*-

"""
Test cases for packstack.installer.setup_params module.
"""

from unittest import TestCase

from ..test_base import PackstackTestCaseMixin
from packstack.installer.setup_params import *


class ParameterTestCase(PackstackTestCaseMixin, TestCase):
    def setUp(self):
        super(ParameterTestCase, self).setUp()
        self.data = {
            "CMD_OPTION": "mysql-host",
            "USAGE": ("The IP address of the server on which to "
                      "install MySQL"),
            "PROMPT": "Enter the IP address of the MySQL server",
            "OPTION_LIST": [],
            "VALIDATORS": [],
            "DEFAULT_VALUE": "127.0.0.1",
            "MASK_INPUT": False,
            "LOOSE_VALIDATION": True,
            "CONF_NAME": "CONFIG_MYSQL_HOST",
            "USE_DEFAULT": False,
            "NEED_CONFIRM": False,
            "CONDITION": False}

    def test_parameter_init(self):
        """
        Test packstack.installer.setup_params.Parameter initialization
        """
        param = Parameter(self.data)
        for key, value in self.data.iteritems():
            self.assertEqual(getattr(param, key), value)

    def test_default_attribute(self):
        """
        Test packstack.installer.setup_params.Parameter default value
        """
        param = Parameter()
        self.assertIsNone(param.PROCESSORS)


class GroupTestCase(PackstackTestCaseMixin, TestCase):
    def setUp(self):
        super(GroupTestCase, self).setUp()
        self.attrs = {
            "GROUP_NAME": "MYSQL",
            "DESCRIPTION": "MySQL Config parameters",
            "PRE_CONDITION": "y",
            "PRE_CONDITION_MATCH": "y",
            "POST_CONDITION": False,
            "POST_CONDITION_MATCH": False}
        self.params = [
            {"CONF_NAME": "CONFIG_MYSQL_HOST", "PROMPT": "find_me"},
            {"CONF_NAME": "CONFIG_MYSQL_USER"},
            {"CONF_NAME": "CONFIG_MYSQL_PW"}]

    def test_group_init(self):
        """Test packstack.installer.setup_params.Group initialization"""
        group = Group(attributes=self.attrs, parameters=self.params)
        for key, value in self.attrs.iteritems():
            self.assertEqual(getattr(group, key), value)
        for param in self.params:
            self.assertIn(param['CONF_NAME'], group.parameters)

    def test_search(self):
        """Test packstack.installer.setup_params.Group search method"""
        group = Group(attributes=self.attrs, parameters=self.params)
        param_list = group.search('PROMPT', 'find_me')
        self.assertEqual(len(param_list), 1)
        self.assertIsInstance(param_list[0], Parameter)
        self.assertEqual(param_list[0].CONF_NAME, 'CONFIG_MYSQL_HOST')
