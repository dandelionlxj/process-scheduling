# -*- coding=utf-8 -*-
global N,Z 
N=100     #内存
Z=5       #资源

class JCB:
    def __init__(self,name,submittime,needtime,ram,resourse):
        self.name=name
        self.submittime=submittime
        self.needtime=needtime
        self.ram=ram
        self.resourse=resourse
        self.starttime=0
        self.runtime=0
        self.endtime=0
        self.zztime=0   #周转时间
        self.dqzztime=0  #带权周转时间

class Serve:
    def __init__(self,jcb_list):
        self.jcb=jcb_list


    def run(self):
        current_ram=N
        current_resouce=Z
        t=int(0)
        n=0
        l=0
        m=len(self.jcb)
        avgzz_time=int(0)
        avgdq_time=int(0)
        change_list=[]
        wait_list=[]
        run_list=[]
        finish_list=[]

        while (len(finish_list)<m):

            if(len(self.jcb)>0 and t==self.jcb[0].submittime):
                
                wait_list.append(self.jcb[0])
                self.jcb.remove(self.jcb[0])
                #print(len(wait_list))
                #print(len(self.jcb))
                #print('\n')
            while(len(wait_list)!=0 and wait_list[0].ram<=current_ram and wait_list[0].resourse<=current_resouce):
                wait_list[0].starttime=t
                run_list.append(wait_list[0])
                current_ram-=wait_list[0].ram
                current_resouce-=wait_list[0].resourse
                wait_list.remove(wait_list[0])
                #print(len(wait_list))
                #print(len(run_list))
                #print('\n')

            n=0
            while (n<len(run_list)):
                
                run_list[n].runtime+=1
                if run_list[n].runtime==run_list[n].needtime:
                    run_list[n].endtime=t+1
                    run_list[n].zztime=run_list[n].endtime-run_list[n].submittime
                    run_list[n].dqzztime=float(run_list[n].zztime)/run_list[n].runtime
                    finish_list.append(run_list[n])                   
                    current_ram+=run_list[n].ram
                    current_resouce+=run_list[n].resourse
                    run_list.remove(run_list[n])
                    #print('len of finish%d'%(len(finish_list)))
                else:
                    n+=1
            t+=1
            

        finish_list.sort(key=lambda x:x.starttime)
        for i in range(len(finish_list)):
            print('作业名:%s,  占用内存：%d,  占用资源：%d,  提交时间:%d,  所需的运行时间:%d,  开始运行时刻:%d,  完成时刻:%d,  周转时间:%d,  带权周转时间:%.2f'%(finish_list[i].name,finish_list[i].ram,finish_list[i].resourse,finish_list[i].submittime,finish_list[i].needtime,finish_list[i].starttime,finish_list[i].endtime,finish_list[i].zztime,finish_list[i].dqzztime))
            
        for i in range(len(finish_list)):
            avgzz_time+=float(finish_list[i].zztime)/len(finish_list)
            avgdq_time+=float(finish_list[i].dqzztime)/len(finish_list)            
            
        print('该组作业的平均周转时间:%.2f,  平均带权周转时间:%.2f'%(avgzz_time,avgdq_time))




if __name__=='__main__':
    jcb_list=[]
    jcb_list1=[]
    JCBA=JCB('A',0,15,20,2) 
    JCBB=JCB('B',20,18,60,1)
    JCBC=JCB('C',30,9,45,3)
    JCBD=JCB('D',35,12,10,2)
    JCBE=JCB('E',45,6,25,3)
    jcb_list.append(JCBA),jcb_list.append(JCBB),jcb_list.append(JCBC)
    jcb_list.append(JCBD),jcb_list.append(JCBE)
    jcb_list1.append(JCBA),jcb_list1.append(JCBB),jcb_list1.append(JCBC)
    jcb_list1.append(JCBD),jcb_list1.append(JCBE)

    
    print('*********************************************先来先服务(FCFS)**********************************************')
    jcb_list.sort(key=lambda x:x.submittime)
    fcfs=Serve(jcb_list)
    fcfs.run()
    print('*******************************************************************************************************')
    print('\n')
    
    