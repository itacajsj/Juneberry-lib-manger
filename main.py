#coding:utf-8
import lib,requests
import urlparse,json,os,time,re
from sendemail import send_email
def start():
    pass
def room2dict(rooms):
    rms={}
    for room in rooms:
        rms[room['name'][:3]]=room
    return rms
def getseat(rooms,date):
    import json
    a=lib.lib()
    b=requests.session()
    headers=a.headers
    a.ss=requests.session()
    a.ss.headers=headers
    seats={}
    for i in rooms:
        seat=a.getseat(i['id'],date=date)
        if seat:
            for j in seat:
                dic=[]
                dic.append(i['name'])
                dic.append(j['seatNum'])
                dic.append(j['onclick'])
                dic=tuple(dic)
                nm=i['name'][:3]+j['seatNum']
                seats[nm]=dic
    filename='seats'+ date.replace('/','-')+'.json'
    # filename=os.path.join(os.getcwd(), filename)
    f=open(filename,'w')
    f.close()
    if seats:
        json.dump(seats,open(filename,'w'))
        return seats
    else:
        json.dump({},open(filename,'w'))
        return {}
def getrooms():
    a = lib.lib()
    b = requests.session()
    headers = a.headers
    a.ss = requests.session()
    a.ss.headers = headers
    rooms=a.getroomid()

    json.dump(rooms,open('room.json','w'))
    return rooms
def loadrooms(file):
    if os.path.isfile(file):
        a=json.load(open(file))
        return a
    else:
        return getrooms()
def loadseats(date):
    date=date.replace('/','-')
    filename = 'seats' + date.replace('/', '-') + '.json'
    try:
        return json.load(open(filename))
    except:
        return getseat(loadrooms('room.json'),date)


# b=getrooms()
#c=getseat(b,'2016/10/21')
if __name__=='__main__':
    if os.path.isfile('room.json') is False:
        rooms=getrooms()
    else:
        rooms=loadrooms('room.json')
    libsetseat=lib.lib()
    tim = time.gmtime(time.time())
    dates = "%s/%s/%s" % (tim.tm_year, tim.tm_mon, tim.tm_mday + 1)
    seats=loadseats(dates)
    if seats is None:
        for j in range(4):
            seats=loadseats(dates)
            if seats is not  None:
                break
        if seats is None:
            print 'Sorry,All Seats have Been Occupied'
    try:
        users=json.load(open('user_%s.json'%dates.replace('/','-')))
    except Exception as e:
        print e
    got=[]
    notgot=[]
    fail=[]
    roomdic=room2dict(rooms)
    for user in users:
        try:
            seatid=user['room']+user['seat']
            seatSelect=seats[user['seat']]
        except KeyError:
            notgot.append(user)
            continue
        libsetseat.login(user['user'],user['pws'])
        resault=libsetseat.trysetseat(seatSelect(0),seatSelect(1),seatSelect(2),dates)
        libsetseat.ss.close()
        if re.search(u'座位预约成功',resault):
            got.append({"user":user['user'],
                        "email":user['email'],
                        "cont":"座位预约成功，请在规定的时间内刷卡确认。",
                        'room':seatSelect[0],
                        'seat':seatSelect[1]})
            resault=''
        else:
            notgot.append(user)
            del seats[seatid]
            resault=''
    seats=getseat(loadrooms('room.json'),dates)
    for user in notgot:
        if seats =={}:
            user['cont']=u"所有座位都被抢光啦，sorry"
            fail.append(user)
            break
        user['select']=None
        for seatkey in seats.keys():
            if seatkey[:3] ==user['room']:
                user['select']=seatkey
        if user['select'] is None:
            user['select']=seats.keys()[0]
        libsetseat.login(user=user['user'],pwd=user['pwd'])
        selectSeats=seats[user['select']]
        resault=libsetseat.trysetseat(roomName=selectSeats[0].encode('utf-8'),seatNum=selectSeats[1].encode('utf-8'),seatOnclick=selectSeats[2].encode('utf-8'),datestr=dates)
        if re.search(u'座位预约成功', resault):
            got.append({"user":user['user'],
                        "email":user['email'],
                        "cont":u"座位预约成功，请在规定的时间内刷卡确认。",
                        'room':selectSeats[0],
                        'seat':selectSeats[1]})
        else:
            fail.append({
                'user':user['user'],
                "email":user['email'],
                "cont":"抢座失败"
            })
    for us in got:
        b= (us['user'].encode('utf-8'), us['cont'].encode('utf-8'), us['room'], us['seat'].encode('utf-8'))
        contents = u"学号为 %s 的同学你好:%s,阅览室为 %s ,座位号为 %s。请关注微信号 WavesBreaker,请将本邮件地址设为信任邮箱以免收不到邮件。如有疑问欢迎联系itacajsj@outlook.com." % (us['user'], us['cont'], us['room'], us['seat'])
        contents=contents.encode('utf-8','ignore')
        eaddres = us['email']
        try:
            send_email(us['cont'],contents,eaddres)
        except Exception as e:
            print e
    for user in fail:
        contents='''学号为 %s 的同学你好:
                预约座位失败，原因是：%s
                请关注微信号 WavesBreaker,
                请将本邮件地址设为信任邮箱以免收不到邮件。
                如有疑问欢迎联系itacajsj@outlook.com.''' % (user['user'].encode("utf-8"),user['cont'].encode("utf-8"))
        eaddres = user['email']
        try:
            send_email(user['cont'], contents, eaddres)
        except:
            pass
    print 'down'