# -*- coding: utf-8 -*-
# @Time    : 2017/3/2 上午11:59
# @Author  : Yuhsuan
# @File    : action.py
# @Software: PyCharm Community Edition

import desired_capabilities
from log_module import log
import common
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys

# log('[driver_init] start')
# desired_caps = desired_capabilities.get_desired_capabilities('bundleId', 'com.gen.common.deepblu')
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# log('[driver_init] end')
driver = None

# 初始化appium driver, 以便可以做物件抓取
def driver_init():
    global driver
    log('[driver_init] start')
    desired_caps = desired_capabilities.get_desired_capabilities('app', 'ipa/2.2.1.12.ipa')
    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    log('[driver_init] end')

# 跳過最新版本通知畫面
def version_skip():
    log('[version_skip] start')
    if common.wait("id", "Cancel"):
        log("[version_skip] New version is found")
        driver.find_element_by_id("Cancel").click()
    log('[version_skip] end')

# 登入帳號
def login(email=None, pwd=None):
    try:
        log('[login] start')
        version_skip()
        if common.wait("id", "Log in"):
            # click login
            driver.find_element_by_id("Log in").click()

            if email != None and pwd != None:
                # input email
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]").send_keys(
                    email)
                # input password
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]").send_keys(
                    pwd)
            else:
                # input email
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]").send_keys(
                    desired_capabilities.account)
                # input password
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]").send_keys(
                    desired_capabilities.password)
            # hide key board
            driver.hide_keyboard()
            # press login button
            driver.find_element_by_id("Log in").click()

            if common.wait("id", "Menu"):
                log("Login success")

        log('[login] end')
        return True
    except Exception as e:
        return False

# 登出帳號
def logout():
    log("[logout] start")
    common.delay(5)
    if common.wait("id", "Menu"):
        driver.find_element_by_id("Menu").click()

        # 滑到最下面顯示logout
        log("[logout] swap down")
        driver.execute_script("mobile: scroll", {"direction": "down"})
        log("[logout] click logout")
        driver.find_element_by_id("Log out").click()
        log("[logout] click confirm")
        if common.wait('xpath',
                       "//XCUIElementTypeApplication[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeAlert[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]"):
            driver.find_element_by_xpath(
                "//XCUIElementTypeApplication[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeAlert[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[3]").click()
        log("[logout] end")
        return True
    else:
        return False

# type: fb / facebook / email
# code: auto
# 目前只有給Scripts.friend.py做使用，是用來做注冊
def signup_old(type, username=None, email=None, pwd=None, code=None):
    log("[signup] start")
    log("[signup] username: %s email: %s pwd: %s" % (username, email, pwd))
    common.delay(5)

    # skip update new version
    version_skip()

    # sign up with fb
    if type == "fb" or type == "facebook":
        signup_facebook_login()
    # sign up with email
    else:
        if common.wait("id", "Sign up with email"):
            driver.find_element_by_id("Sign up with email").click()
            if common.wait("id", "Sign up"):
                log("[signup] input data")
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
                el.send_keys(username)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
                el.send_keys(email)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
                el.send_keys(pwd)
                driver.hide_keyboard()
                common.screen_shot("input_sign_up_data")
                driver.find_element_by_id("Sign up").click()
                log("[signup] send data")

                if common.wait('id', 'Error'):
                    driver.find_element_by_id("OK").click()
                    log('[signup] Sign up with exists Email')
                    return "Exists Email"
                else:
                    if code == "manual":
                        # auto verify by number
                        log("[signup] manual verify")
                        signup_manual_verify(email)
                    else:
                        # auto verify by link
                        log("[signup] email verify")
                        signup_auto_verify(email)
        else:
            log("[signup] no result")
            pass
    log("[signup] end")
    return True

# 透過Email做註冊
def signup(username=None, email=None, pwd=None):
    try:
        log("[signup] start")
        log("[signup] username: %s email: %s pwd: %s" % (username, email, pwd))
        common.delay(5)

        # skip update new version
        version_skip()

        if common.wait("id", "Sign up with email"):
            driver.find_element_by_id("Sign up with email").click()
            if common.wait("id", "Sign up"):
                log("[signup] input data")
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
                el.send_keys(username)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
                el.send_keys(email)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
                el.send_keys(pwd)
                driver.hide_keyboard()
                common.screen_shot("input_sign_up_data")
                driver.find_element_by_id("Sign up").click()
                log("[signup] send data")
            else:
                return False
        else:
            return False
        log("[signup] end")
        return True
    except Exception as e:
        log(e,'W')
        return False

# 透過Facebook做註冊
def signup_facebook_login():
    log("[signup_facebook_login] start")
    if common.wait("id", "Get Started with Facebook", 30):
        driver.find_element_by_id("Get Started with Facebook").click()
        if common.wait("id", "確定"):
            driver.find_element_by_id("確定").click()
            log("[signup_facebook_login] end")
            return True
    else:
        return False

# 透過Email註冊後，找到驗證碼輸入文字做驗證
def signup_manual_verify(email, code=None):
    try:
        log("[signup_manual_verify] start")
        common.delay(10)
        verifyCode = {}
        verifyCode = common.get_verify_code(email)
        verifyCode = str(verifyCode['code'])

        if common.wait('id', 'Skip'):
            el = driver.find_element_by_xpath(
                '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]')
            el.send_keys(verifyCode)
            common.delay(10)
            # driver.tap(int(common.width() * 0.25), int(common.height() * 0.9))
            TouchAction(driver).tap(x=int(common.width() * 0.25), y=int(common.height() * 0.9)).perform()
            log("[signup_manual_verify] end")
            return True
        else:
            log("[signup_manual_verify] Can't find Skip")
            return False
    except Exception as e:
        log(e,'W')
        common.screen_shot('signup_manual_verify')
        return False

# 透過Email註冊後，找到驗證碼透過Python做驗證
def signup_auto_verify(email):
    try:
        log("[signup_auto_verify] start")
        common.delay(10)
        url = {}
        url = common.get_verify_code(email)
        common.verify_by_link(url['link'])
        common.delay(10)
        # driver.tap(int(common.width() * 0.25), int(common.height() * 0.9))
        TouchAction(driver).tap(x=int(common.width() * 0.25), y=int(common.height() * 0.9)).perform()
        log("[signup_auto_verify] end")
        return True
    except Exception as e:
        log(e,'W')
        common.screen_shot('[signup_auto_verify]')
        return False

# 透過Email註冊已註冊過的帳號
def signup_exist_email(email):
    try:
        log("[signup_exist_email] start")
        if common.wait('id', 'Error'):
            driver.find_element_by_id("OK").click()
            log('[signup_exist_email] Sign up with exists email success')
            log("[signup_exist_email] end")
            return True
        else:
            common.screen_shot('[signup_exist_email]')
            return False
    except Exception as e:
        log(e,'W')
        common.screen_shot('[signup_exist_email]')
        return False

# for test signup and resend email
def signup_resend_email(username=None, email=None, pwd=None, case=None):
    log("[signup_resend_email] start")
    log("[signup_resend_email] username: %s email: %s pwd: %s" % (username, email, pwd))
    common.delay(5)
    # skip update new version
    version_skip()

    if common.wait("id", "Sign up with email"):
        driver.find_element_by_id("Sign up with email").click()
        if common.wait("id", "Sign up"):
            log("[signup_resend_email] input data")
            el = driver.find_element_by_xpath(
                "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
            el.send_keys(username)
            driver.hide_keyboard()
            el = driver.find_element_by_xpath(
                "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
            el.send_keys(email)
            driver.hide_keyboard()
            el = driver.find_element_by_xpath(
                "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
            el.send_keys(pwd)
            driver.hide_keyboard()
            common.screen_shot("input_sign_up_data")
            driver.find_element_by_id("Sign up").click()
            log("[signup_resend_email] send data")

            if case == 1:
                # resend email and manual verify
                res = resend_manual_verify(email)
            elif case == 2:
                # resend email and input wrong verify code
                res = resend_manual_wrong_verify(email)
            else:
                # resend email and auto verify
                res = resend_auto_verify(email)

            if res:
                log("[signup_resend_email] end")
                return True
            else:
                return False

def resend_manual_verify(email):
    log("[resend_manual_verify] start")
    common.delay(5)
    url = {}
    url = common.get_verify_code(email)
    first_code = url['code']

    if common.wait('id', 'Resend Email'):
        for i in range(0, 5):
            common.delay(5)
            url = {}
            url = common.get_verify_code(email)
            if url['code'] == first_code:
                driver.find_element_by_id('Resend Email').click()
            else:
                break

        if signup_manual_verify(email):
            log("[resend_manual_verify] end")
            return True
        else:
            return False

def resend_auto_verify(email):
    log("[resend_auto_verify] start")
    common.delay(5)
    url = {}
    url = common.get_verify_code(email)
    first_code = url['code']

    if common.wait('id', 'Resend Email'):
        for i in range(0, 5):
            common.delay(5)
            url = {}
            url = common.get_verify_code(email)
            if url['code'] == first_code:
                driver.find_element_by_id('Resend Email').click()
            else:
                break

        if signup_auto_verify(email):
            log("[resend_auto_verify] end")
            return True
        else:
            return False

def resend_manual_wrong_verify(email):
    log("[resend_manual_wrong_verify] start")
    common.delay(5)
    url = {}
    url = common.get_verify_code(email)
    first_code = url['code']

    if common.wait('id', 'Resend Email'):
        for i in range(0, 5):
            common.delay(5)
            url = {}
            url = common.get_verify_code(email)
            if url['code'] == first_code:
                driver.find_element_by_id('Resend Email').click()
            else:
                break

        if manual_verify_wrong_code(first_code):
            log("[resend_manual_wrong_verify] end")
            return True
        else:
            return False

# you can use it to verify wrong code
def manual_verify_wrong_code(code):
    log("[manual_verify_wrong_code] start")
    common.delay(10)
    verifyCode = code

    if common.wait('id', 'Skip'):
        el = driver.find_element_by_xpath(
            '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]')
        el.send_keys(verifyCode)

        if common.wait('id', 'Invalid code'):
            el = driver.find_element_by_id("btnBack")
            el.click()
            if common.wait('id', 'Menu'):
                log("[manual_verify_wrong_code] end")
                return True
            else:
                return False

# 1949 change email
def signup_change_email(username=None, email=None, pwd=None):
    try:
        log("[signup_change_email] start")
        log("[signup_change_email] username: %s email: %s pwd: %s" % (username, email, pwd))
        common.delay(5)
        # skip update new version
        version_skip()

        if common.wait("id", "Sign up with email"):
            driver.find_element_by_id("Sign up with email").click()
            if common.wait("id", "Sign up"):
                log("[signup_change_email] input data")
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
                el.send_keys(username)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
                el.send_keys(email)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
                el.send_keys(pwd)
                driver.hide_keyboard()
                common.screen_shot("input_sign_up_data")
                driver.find_element_by_id("Sign up").click()
                log("[signup_change_email] send data")
        log("[signup_change_email] end")
        return True
    except Exception as e:
        log(e,"W")
        return False

def signup_change_email_new(email):
    try:
        log("[signup_change_email_new] start")
        for i in range(0,3):
            if common.wait("id",'Resend Email'):
                driver.find_element_by_id("Change Email").click()
            else:
                break

        if common.wait("id","Change Email"):
            el = driver.find_element_by_xpath("//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
            el.send_keys(email)
            driver.hide_keyboard()
            driver.find_element_by_id("Change Email").click()

        if common.wait("id", 'Resend Email'):
            signup_auto_verify(email)
        log("[signup_change_email_new] end")
        return True
    except Exception as e:
        log(e,"W")
        return False

def signup_change_email_back():
    try:
        log("[signup_change_email_back] start")
        for i in range(0,3):
            if common.wait("id",'Resend Email'):
                driver.find_element_by_id("Change Email").click()
            else:
                break

        if common.wait("id","Change Email"):
            driver.find_element_by_id("btnBack white").click()

        if common.wait("id", 'Resend Email'):
            driver.find_element_by_id("btnBack").click()
        log("[signup_change_email_back] end")
        return True
    except Exception as e:
        log(e,"W")
        return False

def signup_not_verify(username=None, email=None, pwd=None):
    try:
        log("[signup_not_verify] start")
        log("[signup_not_verify] username: %s email: %s pwd: %s" % (username, email, pwd))
        common.delay(5)
        # skip update new version
        version_skip()

        if common.wait("id", "Sign up with email"):
            driver.find_element_by_id("Sign up with email").click()
            if common.wait("id", "Sign up"):
                log("[signup_not_verify] input data")
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
                el.send_keys(username)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
                el.send_keys(email)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
                el.send_keys(pwd)
                driver.hide_keyboard()
                common.screen_shot("input_sign_up_data")
                driver.find_element_by_id("Sign up").click()
                log("[signup_not_verify] send data")
        else:
            return False
        # 跳過驗證
        if common.wait('id','Skip'):
            driver.find_element_by_id("Skip").click()
            driver.find_element_by_id("Skip").click()
        else:
            return False
        # 登出
        if not logout():
            return False
        # 登入
        if not login_not_verify(email, pwd):
            return False
        if common.wait('id','Resend Email'):
            signup_auto_verify(email)
        log("[signup_not_verify] end")
        return True
    except Exception as e:
        log(e,"W")
        return False

def signup_lower_case(username=None, email=None, pwd=None):
    try:
        log("[signup_lower_case] start")
        log("[signup_lower_case] username: %s email: %s pwd: %s" % (username, email, pwd))
        common.delay(5)
        # skip update new version
        version_skip()

        if common.wait("id", "Sign up with email"):
            driver.find_element_by_id("Sign up with email").click()
            if common.wait("id", "Sign up"):
                log("[signup_lower_case] input data")
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]")
                el.send_keys(username)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[4]")
                el.send_keys(email)
                driver.hide_keyboard()
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[6]")
                el.send_keys(pwd)
                driver.hide_keyboard()
                common.screen_shot("input_sign_up_data")
                driver.find_element_by_id("Sign up").click()
                log("[signup_lower_case] send data")
        else:
            return False

        if not signup_auto_verify(str(email).lower()):
            return False

        # 登出
        if not logout():
            return False

        if not login(str(email).lower(),pwd):
            return False
        log("[signup_lower_case] end")
        return True
    except Exception as e:
        log(e,"W")
        return False

def login_not_verify(email,pwd):
    try:
        log('[login_not_verify] start')
        version_skip()
        if common.wait("id", "Log in"):
            # click login
            driver.find_element_by_id("Log in").click()

            if email != None and pwd != None:
                # input email
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]").send_keys(
                    email)
                # input password
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]").send_keys(
                    pwd)
            else:
                # input email
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]").send_keys(
                    desired_capabilities.account)
                # input password
                driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]").send_keys(
                    desired_capabilities.password)
            # hide key board
            driver.hide_keyboard()
            # press login button
            driver.find_element_by_id("Log in").click()
            log('[login_not_verify] end')
            return True
        else:
            return False
    except Exception as e:
        log(e,'W')
        return False

def signup_skip_verify():
    try:
        log('[signup_skip_verify] start')
        if common.wait('id', 'Skip'):
            driver.find_element_by_id("Skip").click()
            common.delay(3)
            driver.find_element_by_id("Skip").click()
            log('signup_skip_verify] end')
            return True
    except Exception as e:
        log(e,'W')
        common.screen_shot('[signup_skip_verify]')
        return False

def skip_edit_person_info():
    try:
        log("[skip_edit_person_info] start")
        common.delay(10)
        # driver.tap(int(common.width() * 0.25), int(common.height() * 0.9))
        TouchAction(driver).tap(x=int(common.width() * 0.25), y=int(common.height() * 0.9)).perform()
        if not common.wait('id','Menu'):
            log('[skip_edit_person_info] Skip fail')
            common.screen_shot('[skip_edit_person_info]')
            return False
        log("[skip_edit_person_info] end")
        return True
    except Exception as e:
        log(e,'W')
        common.screen_shot('[skip_edit_person_info]')
        return False

def check_verify_screen_logout():
    try:
        log("[check_verify_screen_logout] start")
        if common.wait('id','btnBack'):
            driver.find_element_by_id('btnBack').click()
            common.delay(3)
            driver.find_element_by_id('Log out').click()
        else:
            log('[Error][check_verify_screen_logout] fail','W')
            return False
        log("[check_verify_screen_logout] end")
        return True
    except Exception as e:
        log(e,'W')
        common.screen_shot('[check_verify_screen_logout]')
        return False

def signup_auto_verify_edit_profile(email):
    try:
        log("[signup_auto_verify_edit_profile] start")
        common.delay(10)
        url = {}
        url = common.get_verify_code(email)
        common.verify_by_link(url['link'])
        common.delay(10)
        # driver.tap(int(common.width() * 0.25), int(common.height() * 0.9))
        TouchAction(driver).tap(x=int(common.width() * 0.75), y=int(common.height() * 0.9)).perform()
        common.delay(3)
        common.screen_shot('[signup_auto_verify_edit_profile]')
        log("[signup_auto_verify_edit_profile] end")
        return True
    except Exception as e:
        log(e,'W')
        common.screen_shot('[signup_auto_verify_edit_profile]')
        return False

def login_forget_pwd(email):
    try:
        pass
    except Exception as e:
        pass

def check_login(est_status):
    log("[check_login] start")
    version_skip()
    # skip_caution()

    if common.wait("id", "Menu"):
        if est_status == "login":
            pass
        else:
            logout()
    else:
        if est_status == "login":
            login()
        else:
            pass
    log("[check_login] end")

def guest():
    try:
        log('[guest] start')
        if common.wait("id", "Preview the app"):
            driver.find_element_by_id("Preview the app").click()

        if common.wait("id", "connect-with-buddies"):
            log("[guest] pass_login success")
        log('[guest] End')
        return True
    except Exception as e:
        log(e, 'W')
        common.screen_shot('[guest]')
        return False

def guest_pass_signup():
    try:
        log('[guest_pass_signup] start')
        if common.wait("id", "connect-with-buddies"):
            driver.find_element_by_id("NOT NOW").click()
            common.delay(3)
            if not common.wait("id", "connect-with-buddies"):
                log("[guest_pass_signup] pass sign up success")
        log('[guest_pass_signup] End')
        return True
    except Exception as e:
        log(e, 'W')
        common.screen_shot('[guest_pass_signup]')
        return False

def guest_signup():
    # id: Sign up
    pass

def guest_login():
    # id: Log in
    pass

# @Note     : v2.4 修改post的相關路徑
# type: text / video / photo /link
def discover_post(type, text=None, hashtag=None, url=None):
    # id: btn close
    # id: Text / Photo / Video / Dive log / Link
    # video ->  select photo:
    # //XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView[1]/XCUIElementTypeCell[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]
    # //XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView[1]/XCUIElementTypeCell[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]
    # id: send
    # id: btn post gallery / btn link / btn hashtag / Public / Post
    # id: Uploading post… -> 蕭
    # id: total progress -> 消失後才算完整發佈
    # id: Discard progress
    # id: Go back
    log('[discover_post] ' + type + ' start')
    # move to discover
    driver.find_element_by_id("Menu").click()
    driver.find_element_by_id("Discover").click()
    # skip_caution()
    driver.find_element_by_id("btn_post_white").click()

    # show post type screen
    if common.wait("id", "Text", 5) and common.wait("id", "Photo", 5) and common.wait("id", "Video") and common.wait(
            "id", "Link"):
        log("show post type screen")

        # text post
        if type == "text":
            driver.find_element_by_id("Text").click()
            if common.wait("id", "btn hashtag") or common.wait("xpath",
                                                               "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]"):
                el_text = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]")
                if text:
                    el_text.send_keys(text)
                    posts = driver.find_elements_by_id("Post")
                elif hashtag:
                    pass
                else:
                    pass

                # 發表貼文
                driver.find_elements_by_id("Post")[2].click()

                # 如果沒有輸入文字就按下貼文就要做下面的處理
                if not common.wait("id", "Confirm"):
                    pass
                else:
                    driver.find_element_by_id("Confirm").click()
                    driver.find_element_by_id("btn close").click()
                    if common.wait("id", "Discard progress"):
                        driver.find_element_by_id("Discard progress").click()
                    else:
                        pass
                    log("No text, so it doesn't post.")

        # photo / video post
        elif type == "photo" or type == "video":
            if type == "photo":
                driver.find_element_by_id("Photo").click()
            else:
                driver.find_element_by_id("Video").click()

            # 挑選資料夾
            if common.wait("xpath",
                           "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]"):
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]")
                el.click()

            # 挑選照片
            if common.wait("xpath",
                           "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView[1]/XCUIElementTypeCell[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]"):
                el = driver.find_element_by_xpath(
                    "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView[1]/XCUIElementTypeCell[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]")
                el.click()
                driver.find_element_by_id("Confirm").click()

                # input photo screen
                if common.wait("id", "btn post gallery"):
                    if text:
                        # 如果要輸入文字
                        el_text = driver.find_element_by_xpath(
                            "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]")
                        el_text.send_keys(text)
                        driver.hide_keyboard()
                    elif hashtag:
                        # 如果要輸入tag
                        pass
                    else:
                        pass
                    # 發文了
                    if common.wait("id", "Post"):
                        driver.find_elements_by_id("Post")[2].click()
                        if common.wait("id", "total progress"):
                            log("上傳中...等待30秒")
                            for x in range(2):
                                common.delay(1)
                                if not common.wait("id", "total progress"):
                                    log("上傳結束")
                                    break
                        else:
                            # 發文錯誤的handle
                            pass
                        if common.wait("id", "Menu"):
                            log("跳回discover")
                    else:
                        log("找不到post")

                else:
                    # 未跳轉準備發文畫面
                    pass
            else:
                # 如果沒有跳轉選照片
                pass
        # elif type =="video":
        #     pass

        # dive log
        elif type == "dive log":
            pass

        # link post
        elif type == "link":
            log("post link")

            driver.find_element_by_id("Link").click()
            el1 = "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeAlert[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeCollectionView[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]"

            log("input link")
            if common.wait("xpath", el1):
                el = driver.find_element_by_xpath(el1)
                el.send_keys(url)

                log("confirm link")
                # 點擊確認
                if common.wait("id", "OK"):
                    driver.find_element_by_id("OK").click()

                common.wait(3)

                log("input text")
                # 輸入文字
                el_text = "//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTable[1]/XCUIElementTypeCell[1]/XCUIElementTypeTextView[1]"
                if text != None and (common.wait("id", "btn hashtag") or common.wait("xpath", el_text)):
                    input = driver.find_element_by_xpath(el_text)
                    input.send_keys(text)

                log("post")
                if common.wait("id", "Post"):
                    driver.find_elements_by_id("Post")[2].click()
        else:
            driver.find_element_by_id("btn close").click()
            log("type is wrong and not to post")

    # 轉到Following然後截圖
    common.delay(5)
    # skip_caution()
    if common.wait("id", "Following"):
        driver.find_element_by_id("Following").click()
        common.delay(5)
        common.screen_shot("Post " + type)
    log('[discover_post] ' + type + ' end')

# for guest live
def skip_caution():
    log('[skip_caution] start')
    if common.wait('id', "OK"):
        common.delay(5)
        driver.find_element_by_id("OK").click()
    log('[skip_caution] end')

def refresh():
    log("[refresh] start")
    common.delay(3)
    driver.execute_script("mobile: scroll", {"direction": "up"})
    log("[refresh] end")

def live_swap():
    log('[live_swap] start')
    if common.wait('id', "discover"):
        driver.find_element_by_id("discover").click()
    else:
        common.screen_shot('live_swap fail')
    log('[live_swap] end')

def menu_swap():
    log('[menu_swap] start')
    if common.wait('id', 'Menu'):
        driver.find_element_by_id("Menu").click()
    else:
        common.screen_shot('menu_swap fail')
    log('[menu_swap] end')