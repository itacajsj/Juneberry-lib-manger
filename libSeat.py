#coding:utf-8
import requests
from urlparse import urljoin
from bs4 import BeautifulSoup
from regex import regex as filter
# import chardet
def ConventDate(date):
    #没有用
    import time
    return str(int(time.mktime(time.strptime('%s 08', '%Y%m%d %H') % date)) * 10000000 + 621355968000000000)
class lib:
    def __init__(self):
        self.url="http://202.119.210.15/"
        self.host="202.119.210.15"
        self.login="/"
        self.getroom='/FunctionPages/SeatBespeak/BespeakSeat.aspx'
        # self.getseat='/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx'#?roomId=101008&date=636125184000000000
        self.getseatstatus='/FunctionPages/SeatBespeak/SeatLayoutHandle.ashx'
        #/FunctionPages/SeatBespeak/BespeakSubmitWindow.aspx
        self.setseat1='/FunctionPages/SeatBespeak/BespeakSubmitWindow.aspx'
        headers={
            'Host' : self.host,
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding' : 'gzip, deflate',
            'X-Requested-With' : 'XMLHttpRequest',
            'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
            'Connection' : 'keep-alive'
         }
        self.ss=requests.session()
        self.ss.headers=headers
        self.select={}
    def userlogin(self,user,pwd):
        # headers={
        #     'Host' : self.host,
        #     'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        #     'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        #     'Accept-Language' : 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        #     'Accept-Encoding' : 'gzip, deflate',
        #     'X-Requested-With' : 'XMLHttpRequest',
        #     'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
        #     'Connection' : 'keep-alive'
        #  }
        postdata={}
        loginurl=urljoin(self.url,self.login)
        login1=self.ss.get(loginurl)
        if login1.status_code==200:
            login1text=login1.text
        else:
            return "Error"
        sp=BeautifulSoup(login1text,"html.parser")
        # try:
        viewstate=sp.find('input',attrs={'name':"__VIEWSTATE"}).attrs['value']
        eventvalidation=sp.find('input',attrs={'name':"__EVENTVALIDATION"}).attrs['value']
        # except Exception as e:
        #     print login1text
        #     viewstate=''
        #     eventvalidation=''
        postdata['__VIEWSTATE']=viewstate
        postdata['__EVENTVALIDATION']=eventvalidation
        postdata['txtUserName']=user
        postdata['txtPassword']=pwd
        postdata['cmdOK.x']='0'
        postdata['cmdOK.y'] = '0'
        result=self.ss.post(loginurl,data=postdata)
        if result.url==urljoin(self.url,'/Florms/FormSYS.aspx'):
            return True
    def showroom(self):
        #self.rooms
        #self.lib
        headers={
            'Referer':urljoin(self.url,'/Florms/FormSYS.aspx')
        }
        roomurl=urljoin(self.url,self.getroom)
        roomResponse=self.ss.get(roomurl,headers=headers)
        roomText=roomResponse.text
        libs,rooms=filter().BespeakSeat(roomText)
        self.rooms=rooms
        self.libs=libs
    def getseat(self,room,date):
        # room=self.select['room']
        # date=self.select['date']
        roomId=room['id']
        import time
        #2016/10/20 0:00:00
        dates=time.strftime("%Y/%m/%d", time.strptime(date, "%Y-%m-%d"))
        datestr=dates+" 0:00:00"
        # datestr= ConventDate(date)
        postdata={
            "roomNum":roomId,
            "date":datestr,
            "divTransparentTop":"0",
            "divTransparentLeft":"0"
        }
        result=self.ss.post(urljoin(self.url,self.getseatstatus),data=postdata)
        if result.status_code==200:
            resdata=filter().SeatLayoutHandle(result.text)
        else:
            resdata=''
        self.seats=resdata
        self.date=dates
        return resdata
    def getparam(self,seatOnclick=None):
        seat=self.select['seat']
        if seatOnclick:
            parameters=seatOnclick
        else:
            parameters=seat['onclick']
        # datestrr=ConventDate(date)
        headers={
            'Referer':'http://202.119.210.15/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx'
        }
        url=urljoin(self.url, self.setseat1)
        url=url+'?parameters=%s'% parameters
        html=self.ss.get(url,headers=headers).text
        dic=filter().BespeakSubmitWindow(html)
        self.paramedic=dic
    def setseat(self,roomName=None,seatNum=None,seatOnclick=None):
        import base64,re
        if roomName and seatNum and seatOnclick:
            parameters=seatOnclick
            sNum=seatNum
        else:
            room=self.select['room']
            seat=self.select['seat']
            roomName=room['name']
            seatNum=seat["seatNum"]
            parameters=seat['onclick']
            sNum = str(seatNum).encode('utf-8')
        dic=self.paramedic

        url=urljoin(self.url, self.setseat1)
        url = url + '?parameters=%s' % parameters
        dic['__EVENTARGUMENT']='ContentPanel1$btnBespeak'
        dic2={
            'X_CHANGED':'false',
            'X_TARGET':'ContentPanel1_btnBespeak',
            'Form2_Collapsed':'false',
            'ContentPanel1_Collapsed':'false',
            'X_STATE':'',
            'X_AJAX':'true'
        }
        #strcompare='eyJGb3JtMl9jdGwwMF9sYmxSb29tTmFtZSI6eyJUZXh0IjoiMzAx6ZiF6KeI5a6kIn0sIkZvcm0yX2N0bDAxX2xibFNlYXRObyI6eyJUZXh0IjoiMDI3In0sIkZvcm0yX2N0bDAyX2xibGJlZ2luRGF0ZSI6eyJUZXh0IjoiMjAxNi8xMC8yMCJ9LCJGb3JtMl9jdGwwM19sYmxFbmREYXRlIjp7IlRleHQiOiI3OjMw6IezODozMCJ9fQ=='
        #str(roomName).encode('utf-8')
        # b=chardet.detect(roomName)
        # str(seatNum).encode('utf-8')
        # b = chardet.detect(Datestr)
        room1=roomName

        dastr=self.date
        strdic='''{\"Form2_ctl00_lblRoomName\":{\"Text\":\"%s\"},\"Form2_ctl01_lblSeatNo\":{\"Text\":\"%s\"},\"Form2_ctl02_lblbeginDate\":{\"Text\":\"%s\"},\"Form2_ctl03_lblEndDate\":{\"Text\":\"7:30至8:30\"}}'''%  (room1,sNum,dastr)
        # s=str(strdic)
        # s=s.encode('utf-8')
        ss=strdic.replace("'",'"')
        encodedstr=base64.b64encode(ss)
        # print encodedstr
        dic2['X_STATE']=encodedstr
        # postdata=dict(dic,**dic2)
        for key in dic2.keys():
            dic[key]=dic2[key]
        dic["__EVENTTARGET"]=dic["__EVENTARGUMENT"]
        dic["__EVENTARGUMENT"]=""
        header={
            'Referer':url
        }
        response=self.ss.post(url,data=dic,headers=header)
        result = re.search('alert\((.+?)\)',response.text)
        if result:
            return result.group(1)
        else:
            return '服务器错误'

if __name__=="__main__":
    user=raw_input("input user")
    pwd=raw_input("input pwd")
    libget=lib()
    libget.userlogin(user=user,pwd=pwd)
    libget.showroom()
    room=libget.rooms
    for i in room:
        print room.index(i)+1,".",i['name']
    while True:
        index=raw_input('请输入序号：')
        date=raw_input("请输入日期，形式为2016-10-20，如不输入则默认为第二天：")
        try:
            if index is None:
                break
            libget.select['room']=room[int(index)-1]
            libget.select['date']=date
            break
        except :
            print("输入错误，请重新输入")
    libget.getseat(libget.select['room'],libget.select['date'])
    for i in libget.seats:
        print libget.seats.index(i)+1,'.', i['seatNum']
    while True:
        index=raw_input('请输入序号：')
        try:
            if index is None:
                break
            libget.select['seat']=libget.seats[int(index)-1]
            break
        except :
            print("输入错误，请重新输入")
    libget.getparam()
    res=libget.setseat()
    print res
