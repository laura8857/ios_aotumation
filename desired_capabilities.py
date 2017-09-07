# -*- coding: utf-8 -*-
# @Time    : 2017/3/2 上午11:22
# @Author  : Yuhsuan
# @File    : desired_capabilities.py
# @Software: PyCharm Community Edition

# 2017-03-02 by Yuhsuan
# Default test device is iPhone 5s with ios 10.2.1
# If we need to test browser, need to disable app and add browser in desired_capabilities.

import os
from configure.conf import configuration

# desired_caps['browserName'] = 'safari'
# desired_caps['app'] = directory+'DeepbluApp_2.0.0_adhoc.ipa'
# desired_caps['bundleId'] = 'com.deepblu.deepblu'
def get_desired_capabilities(test_type, app_path):
    desired_caps = {
        'deviceName': configuration['device_name'],
        'platformName': configuration['device_os'],
        'platformVersion': configuration['device_os_version'],
        'udid': configuration['device_uid'],
        'bundleId' : 'Settings',
        'automationName': 'XCUITest',
        'autoWebview': False,
        'browserName': '',
        'locationServicesEnabled': True,
        'locationServicesAuthorized': True,
        'wdaLocalPort': '8100',
        'webDriverAgentUrl': 'http://localhost:8100',
        'showXcodeLog':'true',
        'wdaStartupRetries':10,
        'noRest':False
    }

    directory = '%s/' % os.getcwd()

    if test_type == 'app':
        if app_path=='Settings':
            desired_caps['app'] = app_path
        else:
            # Need to install app
            desired_caps['app'] = directory + app_path
            # print(desired_caps['app'])
            desired_caps['bundleId'] = ''

    elif test_type == 'bundleId':
        # Know bundle id
        desired_caps['bundleId'] = app_path

    elif test_type == 'browser':
        # Test browser
        desired_caps['browserName'] = 'safari'
    else:
        # Default is using com.deepblu.deepblu
        desired_caps['bundleId'] = 'com.deepblu.deepblu'

    return desired_caps