# -*- coding: utf-8 -*-
# @Time    : 2017/5/3 上午11:40
# @Author  : Yuhsuan
# @File    : LoginTestCases.py
# @Software: PyCharm Community Edition
# appium --session-override --command-timeout 72000000 --log /Users/yuhsuan/Desktop/appium.log
from appium_controller import appium_controller
import unittest
import action
from log_module import log
from common import *
from desired_capabilities import *
from configure.conf import configuration

#Login account / password
usr = configuration['signup_username']
acc = configuration['login_account']
pwd = configuration['login_password']

class test_loginUniTest(unittest.TestCase):
    Result = False
    
    #開始必做
    def setUp(self):
        log('[Test Case][%s] start' % (self._testMethodName),lvl='i')
        test_loginUniTest.Result=False
        action.driver_init()

    #結束必做
    def tearDown(self):
        screen_shot('[Test Case]['+self._testMethodName+']')
        if test_loginUniTest.Result:
            log('[Test Case][%s] Success' % (self._testMethodName),lvl='i')
        else:
            log('[Test Case][%s] Fail' % (self._testMethodName), lvl='w')
        log('[Test Case][%s] end' % (self._testMethodName),lvl='i')
        log('='*30+'\n\n')

    # 註冊新帳號，並且用驗證碼完成驗證
    def test_93_1(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res1 = action.signup(usr,acc,pwd)
        res2 = action.signup_manual_verify(acc)
        if res1==True and res2==True:
            test_loginUniTest.Result = True
        self.assertTrue(test_loginUniTest.Result)

    # 註冊新帳號，並且用Email內的連結完成驗證
    def test_93_2(self):
        rm_email("yuhsuan@deepblu.com")
        rm_fb(acc)
        action.check_login("logout")
        # action.signup("email", usr, acc, pwd, "auto")
        res1 = action.signup(usr,acc,pwd)
        res2 = action.signup_auto_verify(acc)
        if res1 ==True and res2==True:
            test_loginUniTest.Result = True

    # 登出帳號
    def test_97(self):
        action.check_login('login')
        action.logout()
        test_loginUniTest.Result = True

    # 註冊已經存在的帳號
    def test_253(self):
        action.check_login("logout")
        res1 = action.signup(usr,acc,pwd)
        res2 = action.signup_exist_email(acc)
        if res1 == True and res2 ==True:
            test_loginUniTest.Result = True

    # 註冊後重新發送email, 用新的驗證碼驗證，可以成功
    def test_1948_1(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res = action.signup_resend_email(usr, acc, pwd,1)
        test_loginUniTest.Result = res

    # 註冊後重新發送email, 用舊的驗證碼驗證
    def test_1948_2(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res = action.signup_resend_email(usr, acc, pwd,2)
        test_loginUniTest.Result = res

    # 註冊新帳號，並且用Email內的連結完成驗證
    def test_1948_3(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res = action.signup_resend_email(usr, acc, pwd,3)
        test_loginUniTest.Result = res

    # 註冊之後修改Email
    def test_1949_1(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")

        res1 = action.signup_change_email(usr,acc+'1',pwd)
        res2 = action.signup_change_email_new(acc)
        if res1==True and res2 == True:
            test_loginUniTest.Result = True

    # 註冊之後，從修改Email畫面返回
    def test_1949_2(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res1 = action.signup_change_email(usr,acc,pwd)
        res2 = action.signup_change_email_back()
        if res1==True and res2 == True:
            test_loginUniTest.Result = True

    # 註冊之後跳過驗證，重新登入必須要可以出現驗證畫面
    def test_1951(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res = action.signup_not_verify(usr, acc, pwd)
        test_loginUniTest.Result = res

    # 用大寫註冊，小寫登入
    def test_1415(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res = action.signup_lower_case(usr, "YUHSUAN@DEEPBLU.COM", pwd)
        test_loginUniTest.Result = res

    # 註冊之後編輯個人資訊
    def test_2020(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res1 = action.signup(usr, acc, pwd)
        res2 = action.signup_auto_verify_edit_profile(acc)
        if int(res1)*int(res2)==1:
            test_loginUniTest.Result=True

    # 註冊之後，Token過期還未驗證
    def test_2085(self):
        rm_email(acc)
        rm_fb(acc)
        action.check_login("logout")
        res1 = action.signup(usr, acc, pwd)
        res2 = action.signup_skip_verify()
        res3 = action.skip_edit_person_info()
        token_expired(acc)
        action.refresh()
        res4 = action.check_verify_screen_logout()
        if int(res1)*int(res2)*int(res3)*int(res4)==1:
            test_loginUniTest.Result=True

    # 登入帳號
    def test_95(self):
        action.check_login("logout")
        res1 = action.login("test01@test.com", "123456")
        test_loginUniTest.Result=res1

    # 跳過登入
    def test_1412(self):
        action.check_login("logout")
        res1 = action.guest()
        res2 =  action.guest_pass_signup()
        if int(res1)*int(res2)==1:
            test_loginUniTest.Result=True

    def test_101(self):
        action.check_login("logout")
        res1 = action.login_forget_pwd('yuhsuan@gmail.com')


if __name__ == '__main__':
    m = appium_controller()
    m.start()
    unittest.main()
    m.end()