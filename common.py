# -*- coding: utf-8 -*-
# @Time    : 2017/3/2 下午12:23
# @Author  : Yuhsuan
# @File    : common.py
# @Software: PyCharm Community Edition

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from log_module import log
import action
import datetime
import time
import os
import json
import requests
from pymongo import *

def now():
    return datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

def screen_shot(action_name):
    directory = dic()
    directory = directory+datetime.datetime.now().strftime('%Y%m%d_')+"result/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_name = now+'_'+action_name+'.png'
    path = directory+file_name
    log('[screen_shot] %s' % (path))
    action.driver.save_screenshot(path)

def delay(x):
    time.sleep(x)

def dic():
    directory = '%s/' % os.getcwd()
    return directory

def read_json(file_path):
    empty = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except Exception as e:
            log('[Error][read_json] %s' % (e))
            return empty
    else:
        log('[Error][read_json] The json file path is not exist, %s' % (file_path))
        return empty

def wait(type=None,el=None,time=None):
    if type == 'id':
        type = By.ID
    elif type == 'class':
        type = By.CLASS_NAME
    elif type == 'name':
        type = By.NAME
    elif type == 'tag':
        type = By.TAG_NAME
    elif type == 'xpath':
        type = By.XPATH
    else:
        type = By.ID

    if time == None:
        time = 5

    try:
        waite_element = WebDriverWait(action.driver,time).until(EC.presence_of_element_located((type,el)))
        return True
    except Exception as e:
        screen_shot('Wait_element')
        log("[Error][wait] The element: %s can't be found." % (el),lvl='e')
        return False

def width():
    return size()['width']

def height():
    return size()['height']

def size():
    size = action.driver.get_window_size()
    return size

def get_verify_code(email):
    url = "http://test.tritondive.co:3000/1/api/users?access_token=YnlyhlAnurDmKOsknbEcR1tuyvrX6Xr9wRR5fwq79WwrQtOlgRC9sQmKmzYAfqqy&filter={\"where\":{\"email\":\""+email+"\"}}"
    result = requests.get(url)
    if result.status_code == 200:
        if len(result.json())==1:
            code = result.json()[0]['code']
            link = "https://test.tritondive.co/apis/user/v0/activeAccount?ownerId="+result.json()[0]['id']+"&code="+code
            dict = {"code":code,"link":link}
            return dict
        else:
            return {}

def token_expired(email):
    # connect to mongo
    client = MongoClient("52.197.14.177", 27017)
    client.deepblu.authenticate('deepblu2', 'DGeANYhWyx8prMFgYEj6', mechanism='MONGODB-CR')
    db = client.deepblu

    if db.user.find_one({"email":email}):
        user = {}
        token =""
        user = db.user.find_one({"email": email})
        id = user['_id']
        #print(str(id))

        for doc in db.AccessToken.find({"userId":id}).sort("created",-1).limit(1):
            token = doc['_id']
            #print(token)

        #call api
        url = "http://test.tritondive.co:8000/apis/user/v0/tokenExpire"
        data = {}
        data['accessToken']=token
        headers = {"Accept-Language": "en"}
        result = requests.post(url,json=data,headers = headers)
        if result.status_code == 200:
            log(result.text)
    else:
        log("The mail "+email+" can't be found.")
    client.close()

# rename the email from AAA@AAA.com to AAAYYYYMMDDHHMMSS@AAA.com
def rm_email(email):
    now = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    tmp = email.split("@")
    new_mail = tmp[0]+now+'@'+tmp[1]

    #update to mongodb
    client = MongoClient("52.197.14.177", 27017)
    client.deepblu.authenticate('deepblu2', 'DGeANYhWyx8prMFgYEj6', mechanism='MONGODB-CR')
    db = client.deepblu

    if db.user.find_one({"email":email}):
        db.user.update_one({"email": email}, {"$set": {"email": new_mail}})
        if db.user.find_one({"email":email}):
            log("Please check DB, the email can't be changed")
        else:
            log("The email already modify to "+new_mail)
    else:
        log("The mail "+email+" can't be found.")
    client.close()

# remove Facebook connection
def rm_fb(email):
    client = MongoClient("52.197.14.177", 27017)
    client.deepblu.authenticate('deepblu2', 'DGeANYhWyx8prMFgYEj6', mechanism='MONGODB-CR')
    db = client.deepblu

    if db.socialId.find_one({"email":email}):
        db.socialId.delete_one({"email":email})
        if db.socialId.find_one({"email":email}):
            log("Please check DB, the fb can't be changed")
        else:
            log("The facebook account is removed.")
    else:
        log("The facebook account "+email+" can't be found.")

    client.close()

# click email verification link
def verify_by_link(url):
    log('[verify_by_link] start')
    json = {"accept-language": "en"}
    res = requests.get(url,headers=json)
    log('[verify_by_link] end')