# -*- coding=utf-8 -*-
class  JCB:
    '''
    作业控制模块
    '''
    def __init__(self,name,submittime,needtime):
        self.name=name
        self.submittime=submittime
        self.needtime=needtime
        self.left_serve_time=needtime          #剩余需要服务的时间
        self.left_time=needtime
        self.starttime=0
        self.waittime=0
        self.q=1      #优先权
        self.endtime=0
        self.zztime=0   #周转时间
        self.dqzztime=0  #带权周转时间

        
class  Serve:
    '''
    先来先服务
    短进程优先
    '''
    def __init__(self,jcb_list):
        self.jcb=jcb_list

    def scheduling(self):
        run_time=int(0)
        avgzz_time=int(0)
        avgdq_time=int(0)
        change_list=[]

        while (True):
            for i in range(len(self.jcb)):
                self.jcb[i].starttime=run_time
                self.jcb[i].endtime=self.jcb[i].starttime+self.jcb[i].needtime
                self.jcb[i].zztime=self.jcb[i].endtime-self.jcb[i].submittime
                self.jcb[i].dqzztime=float(self.jcb[i].zztime)/self.jcb[i].needtime
                run_time+=self.jcb[i].needtime

                if i<len(self.jcb)-1:
                    '''
                    SJF时，如果队首的下一列进程的到达时间大于队首进程的完成时间
                    则将之后队列重新排序
                    '''
                    if self.jcb[i+1].submittime>self.jcb[i].endtime:
                        for j in range(i+2,len(self.jcb)):
                            if self.jcb[j].submittime<=self.jcb[i].endtime:
                                self.jcb[i+1],self.jcb[j]=self.jcb[j],self.jcb[i+1]
                                break
                        change_list=self.jcb[i+2:len(self.jcb)]
                        change_list.sort(key=lambda x:x.needtime)
                        self.jcb[i+2:len(self.jcb)]=change_list
                
            for i in range(len(self.jcb)):
                print('作业名:%s,  提交时间:%d,  所需的运行时间:%d,  开始运行时刻:%d,  完成时刻:%d,  周转时间:%d,  带权周转时间:%.2f'%(self.jcb[i].name,self.jcb[i].submittime,self.jcb[i].needtime,self.jcb[i].starttime,self.jcb[i].endtime,self.jcb[i].zztime,self.jcb[i].dqzztime))
            for i in range(len(self.jcb)):
                avgzz_time+=float(self.jcb[i].zztime)/len(self.jcb)
                avgdq_time+=float(self.jcb[i].dqzztime)/len(self.jcb)            
            break
        print('该组作业的平均周转时间:%.2f,  平均带权周转时间:%.2f'%(avgzz_time,avgdq_time))

class HRRN:
    '''
    高响应比优先
    '''
    def __init__(self,jcb_list):
        self.jcb=jcb_list
    
    def run(self):
        run_time=int(0)  
        avgzz_time=int(0)
        avgdq_time=int(0)
        change_list=[]

        while(True):
            #执行程序
            for i in range(len(self.jcb)):               
                self.jcb[i].starttime=run_time
                self.jcb[i].endtime=self.jcb[i].starttime+self.jcb[i].needtime
                self.jcb[i].zztime=self.jcb[i].endtime-self.jcb[i].submittime
                self.jcb[i].dqzztime=float(self.jcb[i].zztime)/self.jcb[i].needtime
                run_time+=self.jcb[i].needtime

                if i <len(self.jcb)-1:
                    for j in range(i+1,len(self.jcb)):
                        self.jcb[j].waittime=run_time-self.jcb[j].submittime
                        #等待时间不为负数
                        if self.jcb[j].waittime<=0:
                            self.jcb[j].waittime=0
                        #计算优先权
                        self.jcb[j].q=1+self.jcb[j].waittime/self.jcb[j].needtime
                        #print(self.jcb[j].name,self.jcb[j].waittime,self.jcb[j].q)
                    change_list=self.jcb[i+1:len(self.jcb)]
                    #按优先权排序
                    change_list.sort(key=lambda x:x.q ,reverse = True) 
                    self.jcb[i+1:len(self.jcb)]=change_list

                    if self.jcb[i+1].submittime>self.jcb[i].endtime:
                        '''如果队首的下一列进程的到达时间大于队首进程的完成时间
                    则将之后队列重新排序
                        '''
                        for j in range(i+2,len(self.jcb)):
                            if self.jcb[j].submittime<=self.jcb[i].endtime:
                                self.jcb[i+1],self.jcb[j]=self.jcb[j],self.jcb[i+1]
                                break
                        change_list=self.jcb[i+2:len(self.jcb)]
                        change_list.sort(key=lambda x:x.q)
                        self.jcb[i+2:len(self.jcb)]=change_list
            
            #打印列表
            for i in range(len(self.jcb)):
                print('作业名:%s,  提交时间:%d,  所需的运行时间:%d,  开始运行时刻:%d,  完成时刻:%d,  周转时间:%d,  带权周转时间:%.2f'%(self.jcb[i].name,self.jcb[i].submittime,self.jcb[i].needtime,self.jcb[i].starttime,self.jcb[i].endtime,self.jcb[i].zztime,self.jcb[i].dqzztime))
            #计算平均周转时间和平均带权周转时间
            for i in range(len(self.jcb)):
                avgzz_time+=float(self.jcb[i].zztime)/len(self.jcb)
                avgdq_time+=float(self.jcb[i].dqzztime)/len(self.jcb)            
            break
        print('该组作业的平均周转时间:%.2f,  平均带权周转时间:%.2f'%(avgzz_time,avgdq_time))

class RR:
    '''
    轮转法
    '''
    def __init__(self,jcb_list,q):
        self.jcb_list=jcb_list
        self.q=q
    def scheduling(self):
        self.jcb_list.sort(key=lambda x:x.submittime)#按照.submittime进行排序
        len_queue=len(self.jcb_list) #进程队列的长度
        index=int(0)  #索引
        q=self.q      #时间片
        running_time=int(0)#已经运行了的时间
        store_list=[]
        avgdq_time=0
        avgzz_time=0

        #调度的循环
        while(True):
            #print('时间片为%d'%(q))
            #当前进程
            n=index%len_queue
            current_process=self.jcb_list[n]
            #判断当前进程是否已经被完成
            if current_process.left_serve_time>0: 
                #计算完成时间
                #还需要服务的时间大于等于时间片，则完成时间+时间片时间  此进程还没结束
                #还需要服务的时间小于时间片，则完成时间在原来基础上加上继续服务的时间
                if current_process.left_serve_time>=q:
                    running_time+=q
                    #print('正在运行: %s , 已运行时间: %d , 索引: %d'%(current_process.name,running_time,index))
                    current_process.left_serve_time-=q

                else :
                    #print('%s 还需要服务的时间小于当前时间片'%current_process.name)
                    running_time+=current_process.left_serve_time
                    current_process.left_serve_time=0
                '''
                for i in range(len_queue):
                    if n+i<len_queue:
                        print('进程名：%s ,到达时间:%d,需要服务时间:%d,已服务的时间：%d,剩余需要服务时间:%d'%(self.jcb_list[n+i].name,self.jcb_list[n+i].submittime,self.jcb_list[n+i].needtime,self.jcb_list[n+i].needtime-self.jcb_list[n+i].left_serve_time,self.jcb_list[n+i].left_serve_time))
                    else:
                        m=(n+i)%len_queue
                        print('进程名：%s ,到达时间:%d,需要服务时间:%d,已服务的时间：%d,剩余需要服务时间:%d'%(self.jcb_list[m].name,self.jcb_list[m].submittime,self.jcb_list[m].needtime,self.jcb_list[m].needtime-self.jcb_list[m].left_serve_time,self.jcb_list[m].left_serve_time))
                print('*****************************************************************')
                '''

            #已完成
            if current_process.left_serve_time==0:
                #计算完成时间
                current_process.endtime=running_time
                #计算周转时间
                current_process.zztime=current_process.endtime-current_process.submittime
                #计算带权周转时间
                current_process.dqzztime=float(current_process.zztime)/current_process.needtime
                '''
                #打印
                print('%s 进程已完成，详细信息如下：'%current_process.name)
                print('进程名称：%s  ，完成时间： %d    ，周转时间：%d  ，带权周转时间： %.2f'%(current_process.name,current_process.endtime,current_process.zztime,current_process.dqzztime))
                print('*****************************************************************')
                '''
                store_list.append(current_process)
                #弹出
                self.jcb_list.remove(current_process)
                len_queue=len(self.jcb_list)
                #有进程完成任务后，index先回退，之后再加，以保持指向下一个需要调度的进程
                index-=1
            #index常规增加
            index+=1     

            #如果队列中没有进程则表示执行完毕
            if len(self.jcb_list)==0:
                #print('全部进程都已完成')
                store_list.sort(key=lambda x:x.submittime)
                for i in range (len(store_list)):
                    print('进程名称：%s，提交时间：%d，所需时间：%d，完成时间：%d，周转时间：%d，带权周转时间： %.2f'%(store_list[i].name,store_list[i].submittime,store_list[i].needtime, store_list[i].endtime,store_list[i].zztime,store_list[i].dqzztime))
                    avgzz_time+=float(store_list[i].zztime)/len(store_list)
                    avgdq_time+=float(store_list[i].dqzztime)/len(store_list)
                print('该组作业的平均周转时间:%.2f,  平均带权周转时间:%.2f'%(avgzz_time,avgdq_time))
                break

            #改变index，避免因为index大于len，导致取模时出错
            if index>=len(self.jcb_list):
                index=index%len_queue

class SJFS:
    '''
    抢占式最短作业优先
    '''
    def __init__(self,jcb_list):
        self.jcb_list=jcb_list

    def funtion(self):
        t=0
        avgzz_time=0
        avgdq_time=0
        wait_list=[]
        finish_list=[]
        a=len(self.jcb_list)
        
        while(len(finish_list)<a):
            if len(self.jcb_list)!=0 and self.jcb_list[0].submittime==t:
                wait_list.append(self.jcb_list[0])

                self.jcb_list.remove(self.jcb_list[0])
            wait_list.sort(key=lambda x:x.needtime)          
            wait_list[0].left_time-=1
            if  wait_list[0].left_time==0:
                wait_list[0].endtime=t+1
                wait_list[0].zztime=wait_list[0].endtime-wait_list[0].submittime
                wait_list[0].dqzztime=float(wait_list[0].zztime)/wait_list[0].needtime
                finish_list.append(wait_list[0])
                wait_list.remove(wait_list[0])
            t=t+1
        #打印列表
        for i in range(len(finish_list)):
            print('作业名:%s,  提交时间:%d,  所需的运行时间:%d,  完成时刻:%d,  周转时间:%d,  带权周转时间:%.2f'%(finish_list[i].name,finish_list[i].submittime,finish_list[i].needtime,finish_list[i].endtime,finish_list[i].zztime,finish_list[i].dqzztime))
        #计算平均周转时间和平均带权周转时间
        for i in range(len(finish_list)):
            avgzz_time+=float(finish_list[i].zztime)/a
            avgdq_time+=float(finish_list[i].dqzztime)/a
        print('该组作业的平均周转时间:%.2f,  平均带权周转时间:%.2f'%(avgzz_time,avgdq_time))

if __name__=='__main__':
    jcb_list=[]
    jcb_list1=[]
    jcb_list2=[]
    jcb_list3=[]
    jcb_list4=[]
    JCBA=JCB('A',0,3) 
    JCBB=JCB('B',2,6)
    JCBC=JCB('C',4,4)
    JCBD=JCB('D',6,5)
    JCBE=JCB('E',8,2)

    jcb_list.append(JCBA),jcb_list.append(JCBB),jcb_list.append(JCBC)
    jcb_list.append(JCBD),jcb_list.append(JCBE)
    jcb_list1.append(JCBA),jcb_list1.append(JCBB),jcb_list1.append(JCBC)
    jcb_list1.append(JCBD),jcb_list1.append(JCBE)
    jcb_list2.append(JCBA),jcb_list2.append(JCBB),jcb_list2.append(JCBC)
    jcb_list2.append(JCBD),jcb_list2.append(JCBE)
    jcb_list3.append(JCBA),jcb_list3.append(JCBB),jcb_list3.append(JCBC)
    jcb_list3.append(JCBD),jcb_list3.append(JCBE)
    jcb_list4.append(JCBA),jcb_list4.append(JCBB),jcb_list4.append(JCBC)
    jcb_list4.append(JCBD),jcb_list4.append(JCBE)

    
    print('********************************先来先服务(FCFS)********************************************************')
    jcb_list.sort(key=lambda X:X.submittime)
    fcfs=Serve(jcb_list)
    fcfs.scheduling()
    print('*******************************************************************************************************')
    print('\n')
    
    print('********************************非抢占式短作业优先(SJF)********************************************************')
    temp_jcb=jcb_list1[1:len(jcb_list1)] #切片 临时存放后备队列  
    temp_jcb.sort(key=lambda X:X.needtime)
    jcb_list1[1:len(jcb_list1)]=temp_jcb
    sjf=Serve(jcb_list1)
    sjf.scheduling()
    print('*******************************************************************************************************')
    print('\n')

    print('********************************抢占式短作业优先(SJF)****************************************************')
    sjf2=SJFS(jcb_list2)
    sjf2.funtion()
    print('*******************************************************************************************************')
    print('\n')

    print('********************************高响应比优先(HRRN)********************************************************')
    hrrn=HRRN(jcb_list3)
    hrrn.run()
    print('*******************************************************************************************************')
    print('\n')

    print('********************************时间片轮转(RR)********************************************************')
    rr=RR(jcb_list4,1)#时间片为1
    rr.scheduling()
    print('*******************************************************************************************************')
    
    

    