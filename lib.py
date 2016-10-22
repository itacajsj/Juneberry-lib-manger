#coding:utf-8

import requests
import urlparse
from bs4 import BeautifulSoup
from regex import regex as rgx
import sqlalchemy
import urllib
class lib(object):
    def __init__(self,indexurl='http://202.119.210.15/'):
        # self.user={'user':'',
        #            'pwd':''}
        self.indexurl=indexurl
        self.makeurls()
    def makeurls(self):
        index=self.indexurl
        #取出hostname
        host= urlparse.urlparse(index).hostname
        if host==None:
            pass
        #阅览室url
        getroom = '/FunctionPages/SeatBespeak/BespeakSeat.aspx'
        self.getroom=urlparse.urljoin(index,getroom)
        seatinf='/FunctionPages/SeatBespeak/SeatLayoutHandle.ashx'
        self.seatinf=urlparse.urljoin(index,seatinf)
        setseat = '/FunctionPages/SeatBespeak/BespeakSubmitWindow.aspx'
        self.setseat=urlparse.urljoin(index,setseat)
        #初始请求头
        headers = {
            'Host': host,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection': 'keep-alive'
        }
        self.headers=headers
        #session
    def login(self,user='',pwd=''):
        self.ss=requests.session()
        self.ss.headers=self.headers
        login1 = self.ss.get(self.indexurl)
        if login1.status_code==200:
            login1text = login1.text
        else:
            pass
            login1text=''
        sp = BeautifulSoup(login1text)
        #获取viewstate 和 eventvalidation，因为每个学校的这两个都不一样
        viewstate = sp.find('input', attrs={'name': "__VIEWSTATE"}).attrs['value']
        eventvalidation = sp.find('input', attrs={'name': "__EVENTVALIDATION"}).attrs['value']
        #构造postdata
        postdata={}
        postdata['__VIEWSTATE']=viewstate
        postdata['__EVENTVALIDATION']=eventvalidation
        postdata['txtUserName']=user
        postdata['txtPassword']=pwd
        postdata['cmdOK.x']='0'
        postdata['cmdOK.y'] = '0'
        login2 = self.ss.post(self.indexurl, data=postdata,allow_redirects=False)
        if login2.status_code==302:
            return True
        else:
            return False
    def getroomid(self):
        headers = {
            'Referer': urlparse.urljoin(self.indexurl, '/Florms/FormSYS.aspx')
        }
        roomResponse = self.ss.get(self.getroom, headers=headers)
        roomText = roomResponse.text
        libs, rooms = rgx().BespeakSeat(roomText)
        return rooms
    def getseat(self,roomid,date):
        #date=2016/10/22
        datestr = date + " 0:00:00"
        postdata = {
            "roomNum": roomid,
            "date": datestr,
            "divTransparentTop": "0",
            "divTransparentLeft": "0"
        }
        seat=self.ss.post(self.seatinf, data=postdata)
        if seat.status_code==200:
            seatdata=rgx().SeatLayoutHandle(seat.text)
        elif seat.status_code==500:
            print('get seat Server Error %s_%s'%(roomid,date))
            seatdata= None
        else:
            print('Unknown getseat Server Error %s_%s' % (roomid, date))
            seatdata=None
        return seatdata
    def trysetseat(self,roomName,seatNum,seatOnclick,datestr):
        def getparam(setseaturl,seatonclick):
            headers = {
                'Referer': 'http://202.119.210.15/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx'
            }
            url = setseaturl + '?parameters=%s' % seatonclick
            html = self.ss.get(url, headers=headers).text
            dic = rgx().BespeakSubmitWindow(html)
            return url,dic

        import base64, re
        seturl,param=getparam(self.setseat,seatOnclick)
        dic2 = {
            'X_CHANGED': 'false',
            'X_TARGET': 'ContentPanel1_btnBespeak',
            'Form2_Collapsed': 'false',
            'ContentPanel1_Collapsed': 'false',
            'X_STATE': '',
            'X_AJAX': 'true'
        }
        #不清楚服务器是否对字典顺序有要求，故而干脆用最笨的方法
        strdic='''{\"Form2_ctl00_lblRoomName\":{\"Text\":\"%s\"},\"Form2_ctl01_lblSeatNo\":{\"Text\":\"%s\"},\"Form2_ctl02_lblbeginDate\":{\"Text\":\"%s\"},\"Form2_ctl03_lblEndDate\":{\"Text\":\"7:30至8:30\"}}'''%  (roomName,seatNum,datestr)
        strdic= strdic.replace("'", '"')
        encodedstr = base64.b64encode(strdic)
        dic2['X_STATE'] = encodedstr
        postdata=dict(param,**dic2)
        postdata["__EVENTTARGET"]='ContentPanel1$btnBespeak'
        header = {
            'Referer': seturl
        }
        response = self.ss.post(seturl, data=postdata, headers=header)
        result = re.search('alert\((.+?)\)',response.text)
        if result:
            return result.group(1)
        else:
            return '服务器错误'

if __name__=='__main__':
    import json,re
    a=lib()
    a.login('130302126','130302126')
    room=json.load(open('room.json'))
    select={}
    for i in room:
        if re.match('408',room['name']):
            select['roomid']=i['id']
            select['roomname']=i['name']


