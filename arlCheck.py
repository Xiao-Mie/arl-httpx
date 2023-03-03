'''
Created on 2023年3月3日

@author: ss
'''



#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import requests,json,socket,sys,time
import threading
from time import strftime,gmtime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import datetime
import os
import send_vx_message as send_info




########################################################################################################################
arl_url='https://xxx:5003/'
username='admin'
password='xxxx'
#time_sleep=3600 # 秒为单位，获取资产
get_size=100   # 每次获取任务数



########################################################################################################################


def getNeedCheckUrl():
        
    ids=[]
    Token=''
    data = {"username":username,"password":password}
    headers = {'Content-Type': 'application/json; charset=UTF-8'}
    loginreq=requests.post(url=arl_url+'/api/user/login',data=json.dumps(data),headers=headers,timeout=30, verify=False)
    result = json.loads(loginreq.content.decode())
    #登陆
    if result['code'] == 200:
        print(data, '登录成功',result['data']['token'])            
        Token=result['data']['token']
        headers = {'Token': Token,'Content-Type': 'application/json; charset=UTF-8'}
        send_info.push_wechat_group('登录成功,开始获取资产')    
     
        #获取任务id
        taskreq =requests.get(url=arl_url+'/api/task/?page=1&size='+str(get_size), headers=headers,timeout=30, verify=False)
        result = json.loads(taskreq.content.decode())
        for taskList in result['items']:
            if taskList['status']=='done':
                ids.append(taskList['_id'])
        ids=str(ids).replace('\'','"')
        ids_result = json.loads(ids)
        data = {"task_id":ids_result}
        sitereq=requests.post(url=arl_url+'/api/batch_export/site/',data=json.dumps(data),headers=headers,timeout=30, verify=False) 
        if '"not login"' in str(sitereq.text):
            ids = []
            # continue
        target_list=sitereq.text.split()
        if(not(os.path.exists('caches/cache.txt'))):
            os.mkdir('caches')
            open('caches/cache.txt','w',encoding='utf-8').close()
              
        cachs_list = open('caches/cache.txt','r',encoding='utf-8')
        url_list = cachs_list.read().split('\n')
        cachs_list.close()
            
        new_list=set(url_list).symmetric_difference(set(target_list))
        current_time=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).replace(' ','-').replace(':','-')
          
            
        #写入缓存，弄记录日志
        if(not(os.path.exists('applog'))):
            os.mkdir('applog')
            
        write_new = open('caches/cache.txt', 'a', encoding='utf-8')
        write_log = open('applog/'+current_time+'.txt','a', encoding='utf-8')
        write_temp = open('temp.txt','a', encoding='utf-8')
        count = 0;
        for newUrl in new_list:
            if len(newUrl)>1:
                write_new.write(newUrl+'\n')
                write_log.write(newUrl+'\n')
                write_temp.write(newUrl+'\n')
                count = count + 1
        
        send_info.push_wechat_group('获取%s个新的资产' %count)   
        #释放内存                 
        write_new.close()   
        write_log.close() 
        write_temp.close()
        Token = ''
        ids = []  

    else:
        send_info.push_wechat_group('登陆失败')  
        sys.exit()
        
        
if __name__== "__main__" :   
    getNeedCheckUrl()

