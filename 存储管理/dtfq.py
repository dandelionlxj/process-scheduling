# -*- coding :utf-8 -*-
import copy
class JCB:
    def __init__(self,name,needtime,ram):
        
        self.name=name
        self.starttime=0
        self.run_time=0
        self.place=0
        self.needtime=needtime
        self.ram=ram
        self.endtime=0

class freetable:
    def __init__(self,id,room,address):
        self.id=id
        self.room=room
        self.address=address
        self.status=0  #0表示空闲，1表示非空闲

class FF:
    def __init__(self,ftable_list,jcb_list):
        self.ftable=ftable_list
        self.jcb=jcb_list
    
    def run(self):
        t=-1
        c=0
        finish_list=[]
        run_list=[]
        m=len(self.jcb)
        while(len(finish_list)<m):
            t+=1
            l=0
            #print(len(self.jcb))
            while(l<len(self.ftable)):
                #print(self.ftable[l])
                if len(self.jcb)!=0 and self.jcb[0].ram>self.ftable[l].room or  self.ftable[l].status==1:
                    l+=1
                    continue
                if len(self.jcb)!=0 and self.jcb[0].ram<=self.ftable[l].room and self.ftable[l].status==0:                   
                    self.jcb[0].starttime=t
                    self.jcb[0].place=self.ftable[l].id
                    run_list.append(self.jcb[0])
                    #print(len(run_list))
                    self.ftable[l].status=1
                    if self.jcb[0].ram<self.ftable[l].room:
                        self.ftable.insert(l+1,freetable(len(self.ftable)+1,self.ftable[l].room-self.jcb[0].ram,self.jcb[0].ram+self.ftable[l].address))
                        self.ftable[l].room=self.jcb[0].ram
                        if l+2<len(self.ftable):
                            c=l+2
                            while(c<len(self.ftable)):
                                self.ftable[c].address=self.ftable[c-1].room+self.ftable[c-1].address
                                c+=1
                    print('作业%s,大小为%d,插入位置id为%d,插入后的空闲分区表如下'%(self.jcb[0].name,self.jcb[0].ram,self.jcb[0].place))
                    self.jcb.remove(self.jcb[0])
                    a=0
                    while(a<len(self.ftable)):
                        print('分区号：%d，id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(a+1,self.ftable[a].id,self.ftable[a].room,self.ftable[a].address,self.ftable[a].status))
                        a+=1
                    print('--------------------------------------------------------------------')
                
                l+=1
                
            n=0
            while(n<len(run_list)):
                run_list[n].run_time+=1
                if run_list[n].run_time==run_list[n].needtime:
                    run_list[n].endtime=t
                    finish_list.append(run_list[n])
                    #self.ftable[run_list[n].place].status=0
                    d=0
                    while(d<len(self.ftable)):
                        if self.ftable[d].id==run_list[n].place:
                            if d+1<len(self.ftable) and self.ftable[d+1].status==0:#与后一空闲区邻接
                                self.ftable[d].room+=self.ftable[d+1].room
                                self.ftable[d].status=0
                                self.ftable.remove(self.ftable[d+1])
                            if d-1>=0 and self.ftable[d-1].status==0:#与前一空闲区邻接   
                                self.ftable[d-1].room+=self.ftable[d].room
                                self.ftable[d-1].status=0
                                self.ftable.remove(self.ftable[d])
                            if d+1==len(self.ftable) and self.ftable[d-1].status==1:
                                self.ftable[d-1].status=0
                        d+=1
                    print('作业%s,大小为%d ,id为%d,回收后的空闲分区表如下'%(run_list[n].name,run_list[n].ram,run_list[n].place))                                           
                    b=0
                    while(b<len(self.ftable)):
                        print('分区号：%d， id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(b+1,self.ftable[b].id,self.ftable[b].room,self.ftable[b].address,self.ftable[b].status))
                        b+=1
                    print('--------------------------------------------------------------------')
                    run_list.remove(run_list[n])
                else:
                    n+=1
        finish_list.sort(key=lambda x:x.starttime)
        for i in range(len(finish_list)):
            print('作业名：%s， 占用内存：%d， 需要时间：%d， 开始时间：%d，完成时间：%d'%(finish_list[i].name,finish_list[i].ram,finish_list[i].needtime,finish_list[i].starttime,finish_list[i].endtime))

class BF:
    def __init__(self,ftable_list,jcb_list):
        self.ftable=ftable_list
        self.jcb=jcb_list
    
    def bubble_sort(self,list):
    # 冒泡排序
        count = len(list)
        for i in range(0, count):
            for j in range(i + 1, count):
                if list[i].room > list[j].room:
                    list[i], list[j] = list[j], list[i]
        return list

    def schudeing(self):
        t=-1
        c=0
        change_list=[]
        
        finish_list=[]
        run_list=[]
        m=len(self.jcb)
        while(len(finish_list)<m):
            t+=1
            l=0
            change_list=copy.copy(self.ftable)
            change_list=self.bubble_sort(change_list)
            #print(len(self.jcb))
            while(l<len(change_list)):   
                #print(self.ftable[l])
                if len(self.jcb)!=0 and self.jcb[0].ram>change_list[l].room or  change_list[l].status==1:
                    l+=1
                    continue
                if len(self.jcb)!=0 and self.jcb[0].ram<=change_list[l].room and change_list[l].status==0:                   
                    self.jcb[0].starttime=t
                    self.jcb[0].place=change_list[l].id
                    run_list.append(self.jcb[0])
                    #print(len(run_list))
                    e=0
                    while(e<len(self.ftable)):
                        if self.ftable[e].id==change_list[l].id:
                            self.ftable[e].status=1
                            if self.jcb[0].ram<self.ftable[e].room:
                                self.ftable.insert(e+1,freetable(len(self.ftable)+1,self.ftable[e].room-self.jcb[0].ram,self.jcb[0].ram+self.ftable[e].address))
                                self.ftable[e].room=self.jcb[0].ram
                                if e+2<len(self.ftable):
                                    c=e+2
                                    while(c<len(self.ftable)):
                                        self.ftable[c].address=self.ftable[c-1].room+self.ftable[c-1].address
                                        c+=1
                    
                        e+=1
                    
                    print('作业%s,大小为%d,插入位置id为%d,插入后的空闲分区表如下'%(self.jcb[0].name,self.jcb[0].ram,self.jcb[0].place))
                    self.jcb.remove(self.jcb[0])
                    a=0
                    
                    while(a<len(self.ftable)):
                        print('分区号：%d，id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(a+1,self.ftable[a].id,self.ftable[a].room,self.ftable[a].address,self.ftable[a].status))
                        a+=1
                    print('--------------------------------------------------------------------')
                    
                
                l+=1
                
            n=0
            while(n<len(run_list)):
                run_list[n].run_time+=1
                if run_list[n].run_time==run_list[n].needtime:
                    run_list[n].endtime=t
                    finish_list.append(run_list[n])
                    #self.ftable[run_list[n].place].status=0
                    d=0
                    while(d<len(self.ftable)):
                        if self.ftable[d].id==run_list[n].place:
                            if d+1<len(self.ftable) and self.ftable[d+1].status==0:#与后一空闲区邻接
                                self.ftable[d].room+=self.ftable[d+1].room
                                self.ftable[d].status=0
                                self.ftable.remove(self.ftable[d+1])
                            if d-1>=0 and self.ftable[d-1].status==0:#与前一空闲区邻接   
                                self.ftable[d-1].room+=self.ftable[d].room
                                self.ftable[d-1].status=0
                                self.ftable.remove(self.ftable[d])
                            if d+1==len(self.ftable) and self.ftable[d-1].status==1:
                                self.ftable[d-1].status=0
                        d+=1
                    print('作业%s,大小为%d ,id为%d,回收后的空闲分区表如下'%(run_list[n].name,run_list[n].ram,run_list[n].place))                                           
                    
                    b=0
                    while(b<len(self.ftable)):
                        print('分区号：%d， id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(b+1,self.ftable[b].id,self.ftable[b].room,self.ftable[b].address,self.ftable[b].status))
                        b+=1
                    print('--------------------------------------------------------------------')
                    self.ftable.sort(key=lambda x:x.room)
                    run_list.remove(run_list[n])
                else:
                    n+=1
        finish_list.sort(key=lambda x:x.starttime)
        for i in range(len(finish_list)):
            print('作业名：%s， 占用内存：%d， 需要时间：%d， 开始时间：%d，完成时间：%d'%(finish_list[i].name,finish_list[i].ram,finish_list[i].needtime,finish_list[i].starttime,finish_list[i].endtime))
    			
if __name__ == '__main__':
    jcb_list=[]
    jcb_list1=[]
    table=[]
    table1=[]   

    freetablea=freetable(1,50,85)
    freetableb=freetable(2,70,135)
    freetablec=freetable(3,120,205)
    freetabled=freetable(4,115,325)
    freetablee=freetable(5,145,440)
    table.append(freetablea),table.append(freetableb),table.append(freetablec)
    table.append(freetabled),table.append(freetablee)
    table1.append(freetablea),table1.append(freetableb),table1.append(freetablec)
    table1.append(freetabled),table1.append(freetablee)

    JCBA=JCB('A',15,60) 
    JCBB=JCB('B',18,100)
    JCBC=JCB('C',9,130)
    JCBD=JCB('D',12,60)
    JCBE=JCB('E',6,200)
    jcb_list.append(JCBA),jcb_list.append(JCBB),jcb_list.append(JCBC)
    jcb_list.append(JCBD),jcb_list.append(JCBE)
    jcb_list1.append(JCBA),jcb_list1.append(JCBB),jcb_list1.append(JCBC)
    jcb_list1.append(JCBD),jcb_list1.append(JCBE)
    
    '''
    print('**************************************首次适应(FF)********************************')
    print('初始空闲分区表如下')
    print('---------------------------------------------------------------------')
    for i in range(len(table)):
        print('分区号：%d，id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(i+1,table[i].id,table[i].room,table[i].address,table[i].status))
    print('---------------------------------------------------------------------')
    ff=FF(table,jcb_list)
    ff.run()
    print('*******************************************************************************')
    print('\n')

    '''
    print('**************************************最佳适应(BF)********************************')
    
    print('初始空闲分区表如下')
    print('---------------------------------------------------------------------')
    for i in range(len(table1)):
        print('分区号：%d，id:%d, 分区大小：%d，  分区始址：%d，  状态：%d'%(i+1,table1[i].id,table1[i].room,table1[i].address,table1[i].status))
    print('---------------------------------------------------------------------')
    bf=BF(table1,jcb_list1)
    bf.schudeing()
    
    