#coding:utf-8
#get info from html
from bs4 import BeautifulSoup
import re
import ast

class regex(object):
    def BespeakSeat(self,html):
        #get info from /FunctionPages/SeatBespeak/BespeakSeat.aspx
        sp=BeautifulSoup(html)
        js=sp.findAll('script',text=re.compile("ext:qtip"))
        if len(js)==1:
            print "js get all right"
            js=js[0]
        else:
            js=js[0]
        filtoflib='"X_Items":(\[.+?\]),'
        js=js.text
        #Ext.grid.GridPanel({x_state:{"RecordCount":6,"X_Rows":{"Values":[["101001","408阅览室","南京林业大学图书馆","28","0","<a ext:qtip=\"座位已被全部预约\"  class=\"x-item-disabled\" disabled=\"disabled\"><img src=\"/Images/icon/bullet_cross.png\"  ext:qtip=\"座位已被全部预约\"  /></a>"],["101002","407阅览室","南京林业大学图书馆","28","4","<a ext:qtip=\"预约座位\"  href=\"javascript:;\" onclick=\"Ext.defer(function(){X(&#39;WindowEdit&#39;).x_show(&#39;/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx?roomId=101002&amp;date=636125184000000000&#39;,&#39;座位视图&#39;);},0);X.util.stopEventPropagation.apply(null, arguments);\"><img src=\"/Images/icon/zoom.png\"  ext:qtip=\"预约座位\"  /></a>"],["101003","306阅览室","南京林业大学图书馆","32","4","<a ext:qtip=\"预约座位\"  href=\"javascript:;\" onclick=\"Ext.defer(function(){X(&#39;WindowEdit&#39;).x_show(&#39;/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx?roomId=101003&amp;date=636125184000000000&#39;,&#39;座位视图&#39;);},0);X.util.stopEventPropagation.apply(null, arguments);\"><img src=\"/Images/icon/zoom.png\"  ext:qtip=\"预约座位\"  /></a>"],["101004","301阅览室","南京林业大学图书馆","62","28","<a ext:qtip=\"预约座位\"  href=\"javascript:;\" onclick=\"Ext.defer(function(){X(&#39;WindowEdit&#39;).x_show(&#39;/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx?roomId=101004&amp;date=636125184000000000&#39;,&#39;座位视图&#39;);},0);X.util.stopEventPropagation.apply(null, arguments);\"><img src=\"/Images/icon/zoom.png\"  ext:qtip=\"预约座位\"  /></a>"],["101005","308阅览室","南京林业大学图书馆","28","0","<a ext:qtip=\"座位已被全部预约\"  class=\"x-item-disabled\" disabled=\"disabled\"><img src=\"/Images/icon/bullet_cross.png\"  ext:qtip=\"座位已被全部预约\"  /></a>"],["101008","307阅览室","南京林业大学图书馆","28","5","<a ext:qtip=\"预约座位\"  href=\"javascript:;\" onclick=\"Ext.defer(function(){X(&#39;WindowEdit&#39;).x_show(&#39;/FunctionPages/SeatBespeak/BespeakSeatLayout.aspx?roomId=101008&amp;date=636125184000000000&#39;,&#39;座位视图&#39;);},0);X.util.stopEventPropagation.apply(null, arguments);\"><img src=\"/Images/icon/zoom.png\"  ext:qtip=\"预约座位\"  /></a>"]],"DataKeys":[[null],[null],[null],[null],[null],[null]],"States":[[],[],[],[],[],[]]}},id:"gridRoomList",renderTo:"gridRoomList_wrapper",bodyStyle:"",border:true,autoHeight:true,animCollapse:true,collapsible:false,collapsed:false,title:"阅览室列表",sm:x4_sm,cm:x4_cm,store:x4_store,enableHdMenu:false,stripeRows:true,bbar:x4_paging,draggable:false,enableColumnMove:false,enableDragDrop:false,listeners:{headerclick:function(cmp,columnIndex){if(!cmp.getColumnModel().config[columnIndex].sortable){return false;}var args='Sort$'+columnIndex;__doPostBack('gridRoomList',args);cmp.getStore().headerclickprocessed=true;},viewready:function(cmp){cmp.x_setSortIcon(0, 'ASC');cmp.x_selectRows();},render:function(cmp){cmp.x_loadData();}}})
        libs=re.search(filtoflib,js).group(1)
        filtfroom = '"Values":(\[.+?\]\]),'
        rooms = re.search(filtfroom, js).group(1)
        libs=ast.literal_eval(libs)
        rooms=ast.literal_eval(rooms)
        room=map(lambda x:x[:4],rooms)
        rooms=[]
        for x in room:
            dic={}
            dic["id"]=x[0]
            dic['name']=x[1]
            dic['lib']=x[2]
            dic['seats']=x[3]
            rooms.append(dic)

        return libs,rooms
    def SeatLayoutHandle(self,html):
        sp=BeautifulSoup(html)
        divs=sp.find("div",id='divSeatLayout')
        canbesets=divs.findAll('div',attrs={"class":"CanBespeakSeat"})
        data=[]
        for i in canbesets:
            dict={}
            dict['id']=i.attrs['id']
            dict['onclick']=re.search('Click\("(.+?)"\)',i.attrs['onclick']).group(1)
            dict['seatNum']=i.text
            data.append(dict)
        return data
    def BespeakSubmitWindow(self,html):
        sp = BeautifulSoup(html)
        dic={}
        inputs=sp.findAll('input')
        for i in inputs:
            try:
                dic[i.attrs['name']]=i.attrs['value']
            except KeyError:
                dic[i.attrs['name']]=''
        return dic

