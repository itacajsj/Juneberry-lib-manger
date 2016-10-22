#coding:utf-8
import json
while True:
    date=raw_input("Input date you want to apply for:")
    if date=="":
        break
    user=raw_input("Input User:")
    if user=='':
        break
    pwd=raw_input("Input pwd:")
    if pwd=='':
        break
    room=raw_input("Input room(3 character e.g 407 ):")
    if room=='':
        break
    seat=raw_input("Input seat(3 cahracter e.g 012 ):")
    if seat=='':
        break
    email=raw_input("Input email:")
    if email=='':
        break
    dic={'user':user,
        'pwd':pwd,
        'room':room,
        'seat':seat,
        'email':email}
    try:
        dics=json.load(open('user_'+date+'.json'))
    except:
        dics=[]
    dics.append(dic)
    json.dump(dics,open('user_'+date+'.json','w'))
    print("Write Successfully")
    dics=json.load(open('user_'+date+'.json'))
    print dics
