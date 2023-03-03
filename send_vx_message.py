'''
Created on 2023年3月3日

@author: ss
'''
import requests,sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#! /usr/bin/env python3
# -*- coding: utf-8 -*-
webhook_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx'  #漏洞结果，企业微信漏洞通知key


######################################################################################################
def push_wechat_group(content):
    try:
        # print('开始推送')
        # 这里修改为自己机器人的webhook地址
        resp = requests.post(webhook_url,
                             json={"msgtype": "markdown",
                                   "markdown": {"content": content}})
        print(content)
        if 'invalid webhook url' in str(resp.text):
            print('企业微信key 无效,无法正常推送')
            sys.exit()
        if resp.json()["errcode"] != 0:
            raise ValueError("push wechat group failed, %s" % resp.text)
    except Exception as e:
        print(e)
        


if __name__== "__main__" :
    if 1 < len(sys.argv):
        push_wechat_group(sys.argv[1])
    