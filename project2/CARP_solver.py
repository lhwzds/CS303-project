import sys
import queue
import random
import time
import copy
import numpy as np
from multiprocessing import Process,Queue

file_path=sys.argv[1]
termin_time=sys.argv[3]
random_seed=sys.argv[5]
start=time.time()
random.seed(random_seed)
f=open(file_path,encoding='utf-8')

sentimentlist = []

for line in f:
    s = line.strip().split('\t')
    slist=s[0].split()
    sentimentlist.append(slist)

f.close()
vertices=0
depot=0
required=0
non_required=0
vehicles=0
capacity=0
total_cost=0
edge_list=[]

for i in sentimentlist:

    if i[0]=='VERTICES':
        vertices=int(i[2])
    elif i[0]=='DEPOT':
        depot=int(i[2])
    elif i[0]=='REQUIRED':
        required=int(i[3])
    elif i[0]=='NON-REQUIRED':
        non_required=int(i[3])
    elif i[0]=='VEHICLES':
        vehicles=int(i[2])
    elif i[0]=='CAPACITY':
        capacity=int(i[2])
    elif i[0]=='TOTAL':
        total_cost=int(i[6])
    elif str.isdigit(i[0]):
        edge_list.append(i)

class Node(object):
    def __init__(self, dis, index):
        self.dis = dis
        self.index = index

    def __lt__(self, other):
        if self.dis!=other.dis:
            return self.dis < other.dis
        elif self.dis==other.dis:
            p=np.random.rand()
            if p>0.5 :return True
            else: return False

class Edge(object):
    def __init__(self, s, t ,c ,d ):
        self.s = s
        self.t = t
        self.c = c
        self.d = d
    
    def __lt__(self, other):
        if self.d!=other.d:
            return self.d < other.d
        elif self.d==other.d:
            p=np.random.rand()
            if p>0.5 :return True
            else: return False

class Individual(object):
    def __init__(self, gene,q):
        self.gene=gene
        self.q=q

    def __lt__(self, other):
        return self.q < other.q

class Graph:
    def __init__(self,n_vertices,depot,required,non_required,vehicles,capacity,total_cost,edge_list):
        self._n_vertices = n_vertices
        self._depot=depot
        self._required=required
        self._non_required=non_required
        self._vehicles=vehicles
        self._capacity=capacity
        self._total_cost=total_cost
        self._edge_list=edge_list
        self._all_distance= [[0 for _ in range(n_vertices+1)] for _ in range(n_vertices+1)]
        self._adj = [[] for _ in range(n_vertices+1)]

        self.cost_dic={}
        self.demand_dic={}
        self.task_dic={}
        self.id_dic={}
        
        idcounter=1
        for i in self._edge_list:
            s=int(i[0])
            t=int(i[1])
            c=int(i[2])
            d=int(i[3])
            self.add_edge(s,t)
            self.add_edge(t,s)
            self.cost_dic[(s,t)]=c
            self.cost_dic[(t,s)]=c
            self.demand_dic[(s,t)]=d
            self.demand_dic[(t,s)]=d
            self.task_dic[idcounter]=(s,t)
            self.task_dic[-idcounter]=(t,s)
            self.id_dic[(s,t)]=idcounter
            self.id_dic[(t,s)]=-idcounter
            idcounter+=1

        # for i in range(1,n_vertices+1):
        #     for j in range(1,n_vertices+1):
        #         self._all_distance[i][j]=self.dijkstra(i, j)
        
        for i in range(1,n_vertices+1):
            for j in range(1,n_vertices+1):
                if (i,j) in self.cost_dic:
                    self._all_distance[i][j]=self.cost_dic[(i,j)]
                elif i==j:
                    self._all_distance[i][j]=0
                else:
                    self._all_distance[i][j]=10000000000000

        for k in range(1,n_vertices+1):
            for i in range(1,n_vertices+1):
                for j in range(1,n_vertices+1):
                    if self._all_distance[i][j]> self._all_distance[i][k]+self._all_distance[k][j]:
                        self._all_distance[i][j]=self._all_distance[i][k]+self._all_distance[k][j]

        # print(time.time()-start)
        self.tasklist=[]
        self.tasklist2=[]
        for i in self._edge_list:
            s=int(i[0])
            t=int(i[1])
            c=int(i[2])
            d=int(i[3])
            if d!=0:
                self.tasklist.append(Edge(s,t,c,d))
                self.tasklist2.append([s,t,c,d])

    def add_edge(self, s, t):
        self._adj[s].append(t)

    def dijkstra(self, s ,t):
        S=set()
        visit=set()
        disdic={}
        pq = queue.PriorityQueue()
        for i in range(1,self._n_vertices+1):
            if i !=s:
                disdic[i]=1000000000000
                pq.put_nowait(Node(1000000000000,i))
            else:
                disdic[i]=0
                pq.put_nowait(Node(0,i))

        while not pq.empty():
            u = pq.get()
            u_index=u.index
            if u_index not in visit:
                if u_index==t:
                    return u.dis
                visit.add(u_index)
                for i in self._adj[u_index]:
                    if disdic[u_index]+self.cost_dic[(u_index,i)] <disdic[i]:
                        pq.put_nowait(Node(disdic[u_index]+self.cost_dic[(u_index,i)],i))
                        disdic[i]=disdic[u_index]+self.cost_dic[(u_index,i)]         
    
    def finish_one_task(self,s,t):
        cost_sum=0
        cost_sum+=self._all_distance[self._depot][t]
        cost_sum+=self._all_distance[self._depot][s]
        cost_sum+=self.cost_dic[(s,t)]
        return cost_sum

    def gene_to_string(self,gene):
        sline='s '
        first=True
        for i in gene:
            if i==[]:
                continue
            first_task=True
            for j in i:
                # j=self.task_dic[j]
                task=self.task_dic[j]
                # task=j
                if first:
                    addstr=f'0,({task[0]},{task[1]})'
                    sline=sline+addstr
                    first=False
                    first_task=False
                else:
                    if first_task:
                        addstr=f',0,({task[0]},{task[1]})'
                        sline=sline+addstr
                        first_task=False
                    else:
                        addstr=f',({task[0]},{task[1]})'
                        sline=sline+addstr         
            addstr=f',0'
            sline=sline+addstr  
        return sline

    def gene_to_q(self,gene):
        q=0
        for i in gene:
            now=self._depot
            for j in i:
                j=self.task_dic[j]
                # if self._all_distance[j[0]][now]!=0:
                #     print(f'Dijkstra: go from {now} to {j[0]} and cost is {self._all_distance[j[0]][now]}')
                # print(f'Cost: go from {j[0]} to {j[1]} and cost is {self.cost_dic[j]}')
                q+=self._all_distance[j[0]][now]
                q+=self.cost_dic[j]
                now=j[1]
            # if now!= self._depot:
            #     print(f'Dijkstra: go from {now} to {self._depot} and cost is {self._all_distance[now][self._depot]}')
            q+=self._all_distance[now][self._depot]
            # print('Next_Car')   
        return f'q {q}'

    def get_q(self,gene):
        q=0
        for i in gene:
            now=self._depot
            for j in i:
                j=self.task_dic[j]
                # print(f'Dijkstra: go from {now} to {j[0]} and cost is {self._all_distance[j[0]][now]}')
                # print(f'Cost: go from {j[0]} to {j[1]} and cost is {self.cost_dic[j]}')
                q+=self._all_distance[j[0]][now]
                q+=self.cost_dic[j]
                now=j[1]
            # if now!= self._depot:
            #     print(f'Dijkstra: go from {now} to {self._depot} and cost is {self._all_distance[now][self._depot]}')
            q+=self._all_distance[now][self._depot]
        # print('Next_Car')   
        return q

    def gene_output(self,gene):
        print(self.gene_to_string(gene[:]))
        print(self.gene_to_q(gene[:]))

    def get_gene(self):
        tasklist=queue.PriorityQueue()
        for i in self._edge_list:
            s=int(i[0])
            t=int(i[1])
            c=int(i[2])
            d=int(i[3])
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=random.randint(0,len(min_list)-1)
                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)
                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return gene

    def get_gene2(self):
        tasklist=copy.deepcopy(self.tasklist2)
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        
        while len(tasklist)>0:
            tasklist.sort(key = lambda x:min(graph._all_distance[now][x[0]],graph._all_distance[now][x[1]]))
            min_list=[]
            min_dis=min(self._all_distance[now][tasklist[0][0]],self._all_distance[now][tasklist[0][1]])
            for i in tasklist:
                if min(self._all_distance[now][i[0]],self._all_distance[now][i[1]])==min_dis and i[3]+task_sum<self._capacity :
                    min_list.append(i)
            if min_list==[]:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
                continue
            np.random.shuffle(min_list)
            min_task=min_list[0]
            tasklist.remove(min_task)
            task_sum+=min_task[3]
            if self._all_distance[now][min_task[0]]<self._all_distance[now][min_task[1]]:
                route.append(self.id_dic[(min_task[0],min_task[1])])
            else:
                route.append(self.id_dic[(min_task[1],min_task[0])])

            now=min_task[1]
            if now==self._depot:
                task_sum=0
                gene.append(route)
                route=[]
        
        gene.append(route)
        task_sum=0
        now=self._depot 
        return gene

    def single_insertion(self,gene,p,k1,k2,k3):
        routek=gene[k1]
        if len(routek)>1:
            pass
        else:
            k2=-1
        if k2!=-1:
            task_k_index=routek.pop(k2)
            task_k=self.task_dic[task_k_index]
            rp=random.random()
            if rp < p:
                if len(routek)==0:
                    insert_index=0
                    routek.append(task_k_index)
                else:
                    insert_index=k3
                    if insert_index==0:
                        after=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[self._depot][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][after[0]]
                        disy=self._all_distance[self._depot][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][after[0]]
                        if disx<disy:
                            routek.insert(insert_index,self.id_dic[task_k])
                        else:
                            routek.insert(insert_index,self.id_dic[(task_k[1],task_k[0])])
                    elif insert_index==(len(routek)-1):
                        before=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][self._depot]
                        disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][self._depot]
                        if disx<disy:
                            routek.append(self.id_dic[task_k])
                        else:
                            routek.append(self.id_dic[(task_k[1],task_k[0])])              
                    else:
                        before=self.task_dic[routek[insert_index-1]]
                        after=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][after[0]]
                        disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][after[0]]
                        if disx<disy:
                            routek.insert(insert_index,self.id_dic[task_k])
                        else:
                            routek.insert(insert_index,self.id_dic[(task_k[1],task_k[0])])
            else:
                if routek==[]:
                    gene.pop(k1)
                
        return gene

    def double_insertion(self,gene,p,k1,k2,k3):
        routek=gene[k1]
        if len(routek)>2:
            pass
        else:
            k2=-1
        if k2!=-1:
            task_k_index=routek.pop(k2)
            task_k_index2=routek.pop(k2)
            task_k=self.task_dic[task_k_index]
            task_k2=self.task_dic[task_k_index2]
            rp=random.random()
            if rp < p:
                if len(routek)==0:
                    routek.append(task_k_index)
                else:
                    insert_index=k3
                    if insert_index== 0:
                        after=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[self._depot][task_k[0]]+self._all_distance[task_k2[1]][after[0]]
                        disy=self._all_distance[self._depot][task_k2[1]]+self._all_distance[task_k[0]][after[0]]
                        if disx<disy:
                            routek.insert(insert_index,self.id_dic[(task_k[0],task_k[1])])
                            routek.insert(insert_index,self.id_dic[(task_k2[0],task_k2[1])])
                        else:
                            routek.insert(insert_index,self.id_dic[(task_k2[1],task_k2[0])])
                            routek.insert(insert_index,self.id_dic[(task_k[1],task_k[0])])
                    elif insert_index==(len(routek)-1):
                        before=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[before[1]][task_k[0]]+self._all_distance[task_k2[1]][self._depot]
                        disy=self._all_distance[before[1]][task_k2[1]]+self._all_distance[task_k[0]][self._depot]
                        if disx<disy:
                            routek.append(self.id_dic[(task_k[0],task_k[1])])
                            routek.append(self.id_dic[(task_k2[0],task_k2[1])])
                        else:
                            routek.append(self.id_dic[(task_k2[1],task_k2[0])])
                            routek.append(self.id_dic[(task_k[1],task_k[0])])
                    else:
                        before=self.task_dic[routek[insert_index-1]]
                        after=self.task_dic[routek[insert_index]]
                        disx=self._all_distance[before[1]][task_k[0]]+self._all_distance[task_k2[1]][after[0]]
                        disy=self._all_distance[before[1]][task_k2[1]]+self._all_distance[task_k[0]][after[0]]
                        if disx<disy:
                            routek.insert(insert_index,self.id_dic[(task_k[0],task_k[1])])
                            routek.insert(insert_index,self.id_dic[(task_k2[0],task_k2[1])])
                        else:
                            routek.insert(insert_index,self.id_dic[(task_k2[1],task_k2[0])])
                            routek.insert(insert_index,self.id_dic[(task_k[1],task_k[0])])
            else:
                if routek==[]:
                    gene.pop(k1)
                route=[]
                route.append(self.id_dic[(task_k[0],task_k[1])])
                route.append(self.id_dic[(task_k2[0],task_k2[1])])
                gene.append(route)
        return gene

    def swap(self,gene,k1,k2,k3):
        routek=gene[k1]
        if len(routek)>2:
            pass
        else:
            k2=-1

        if k2!=-1:
            
            task_k_index=routek[k2]
            task_k_index2=routek[k3]
            task_k=self.task_dic[task_k_index]
            task_k2=self.task_dic[task_k_index2]    
           
            if k2==0:
                after=self.task_dic[routek[k2+1]]
                disx=self._all_distance[self._depot][task_k2[0]]+self._all_distance[task_k2[1]][after[0]]
                disy=self._all_distance[self._depot][task_k2[1]]+self._all_distance[task_k2[0]][after[0]]

                if disx<disy:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[0],task_k2[1])])
                else:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[1],task_k2[0])])

            elif k2== len(routek)-1:
                before=self.task_dic[routek[k2-1]]
                disx=self._all_distance[before[1]][task_k2[0]]+self._all_distance[task_k2[1]][self._depot]
                disy=self._all_distance[before[1]][task_k2[1]]+self._all_distance[task_k2[0]][self._depot]

                if disx<disy:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[0],task_k2[1])])
                else:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[1],task_k2[0])]) 

            else:
                before=self.task_dic[routek[k2-1]]
                after=self.task_dic[routek[k2+1]]
                
                disx=self._all_distance[before[1]][task_k2[0]]+self._all_distance[task_k2[1]][after[0]]
                disy=self._all_distance[before[1]][task_k2[1]]+self._all_distance[task_k2[0]][after[0]]

                if disx<disy:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[0],task_k2[1])])
                else:
                    routek.pop(k2)
                    routek.insert(k2,self.id_dic[(task_k2[1],task_k2[0])]) 

            if k3==0:
                after=self.task_dic[routek[k3+1]]
                disx=self._all_distance[self._depot][task_k[0]]+self._all_distance[task_k[1]][after[0]]
                disy=self._all_distance[self._depot][task_k[1]]+self._all_distance[task_k[0]][after[0]]

                if disx<disy:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[0],task_k[1])])
                else:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[1],task_k[0])]) 

            elif k3== len(routek)-1:
                before=self.task_dic[routek[k3-1]]
                
                disx=self._all_distance[before[1]][task_k[0]]+self._all_distance[task_k[1]][self._depot]
                disy=self._all_distance[before[1]][task_k[1]]+self._all_distance[task_k[0]][self._depot]

                if disx<disy:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[0],task_k[1])])
                else:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[1],task_k[0])]) 

            else:
                before=self.task_dic[routek[k3-1]]
                after=self.task_dic[routek[k3+1]]
                
                disx=self._all_distance[before[1]][task_k[0]]+self._all_distance[task_k[1]][after[0]]
                disy=self._all_distance[before[1]][task_k[1]]+self._all_distance[task_k[0]][after[0]]

                if disx<disy:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[0],task_k[1])])
                else:
                    routek.pop(k3)
                    routek.insert(k3,self.id_dic[(task_k[1],task_k[0])]) 

        return gene

    def list_2_tuple(self,lst):
        result=[]
        for i in lst:
            ti=tuple(i)
            result.append(ti)
        return tuple(result)

    def single_local_search(self,gene):
        before=1000000
        best_q=1000000
        best_gene=gene
        time_out=False
        while True:
            if time_out:
                break
            for i in range(len(gene)):
                if time_out:
                    break
                if len(gene[i])>1:
                    for j in range(len(gene[i])):
                        if time_out:
                            break
                        for k in range(len(gene[i])-1):
                            if time.time()-start>float(termin_time)-0.5:
                                time_out=True
                            if time_out:
                                break
                            copy_gene=copy.deepcopy(gene)
                            self.single_insertion(copy_gene,1,i,j,k)
                            q=self.get_q(copy_gene)
                            if q<best_q:
                                best_gene=copy_gene
                                best_q=q
            if best_q==before:
                break
            else:
                before=best_q
        return best_gene

    def double_local_search(self,gene):
        before=1000000
        best_q=1000000
        best_gene=gene
        time_out=False
        while True:
            if time_out:
                break
            for i in range(len(gene)):
                if time_out:
                    break
                if len(gene[i])>2:
                    for j in range(len(gene[i])-1):
                        if time_out:
                            break
                        for k in range(len(gene[i])-2):
                            if time.time()-start>float(termin_time)-0.5:
                                time_out=True
                            if time_out:
                                break
                            copy_gene=copy.deepcopy(gene)
                            self.double_insertion(copy_gene,1,i,j,k)
                            q=self.get_q(copy_gene)
                            if q<best_q:
                                best_gene=copy_gene
                                best_q=q
            if best_q==before:
                break
            else:
                before=best_q
        return best_gene

    def swap_local_search(self,gene):
        before=1000000
        best_q=1000000
        best_gene=gene
        time_out=False
        while True:
            if time_out:
                break
            for i in range(len(gene)):
                if time_out:
                    break
                if len(gene[i])>2:
                    for j in range(len(gene[i])):
                        if time_out:
                            break
                        for k in range(len(gene[i])):
                            if k!=j:
                                if time.time()-start>float(termin_time)-0.5:
                                    time_out=True
                                if time_out:
                                    break
                                copy_gene=copy.deepcopy(gene)
                                self.swap(copy_gene,i,j,k)
                                q=self.get_q(copy_gene)
                                if q<best_q:
                                    best_gene=copy_gene
                                    best_q=q
            if best_q==before:
                break
            else:
                before=best_q
        return best_gene
    
    def Ulusoy_split(self,ordered_list):
        V=[0 for i in range(len(ordered_list)+1)]
        P=[0 for i in range(len(ordered_list)+1)]
        length=len(ordered_list)
        for i in range(1,length+1):
            V[i]=1000000000
        
        for t in range(1,length+1):
            i=t-1
            j=i
            load=0
            cost=0
            before_task=None
            while j<length:
                task=self.task_dic[ordered_list[j]]
                load+=self.demand_dic[task]
                if i==j:
                    cost=self._all_distance[self._depot][task[0]]+self.cost_dic[task]+self._all_distance[self._depot][task[1]]
                else:
                    cost=self._all_distance[before_task[1]][task[0]]+self.cost_dic[task]+self._all_distance[self._depot][task[1]]-self._all_distance[self._depot][before_task[1]]
                if load<=self._capacity:
                    v_new=V[t-1]+cost
                    if v_new<V[j+1]:
                        V[j+1]=v_new
                        P[j+1]=t-1
                    before_task=task
                    j+=1
                else:
                    break

        output=[]
        j=length
        ptr=P[j]
        while ptr>0:
            route=[]
            for k  in range(ptr,j):
                route.append(ordered_list[k])
            output.append(route)
            j=ptr
            ptr=P[j]
        route=[]
        for k in range(0,j):
            route.append(ordered_list[k])
        output.append(route)
        return output

    def flatten(self,gene):
        output=[]
        for i in gene:
            for j in i:
                output.append(j)
        return output

    def merge(self,gene,list):
        output=[]
        left=[]
        for i in range(len(gene)):
            if i in list:
                output.append(gene[i])
            else:
                left.append(gene[i])
        return output,left

    def MS_local_search(self,gene):
        min_split=None
        min_left=None
        min_score=10000000000
        counter=0
        for i in range(len(gene)):
            for j in range(i+1,len(gene)):
                counter+=1
                if counter>100:
                    pass
                else:
                    for i in range(5):
                        random_select,left=graph.merge(gene,[i,j])
                        split1=graph.Ulusoy_split(graph.PS1(copy.deepcopy(graph.flatten(random_select))))
                        split2=graph.Ulusoy_split(graph.PS2(copy.deepcopy(graph.flatten(random_select))))
                        split3=graph.Ulusoy_split(graph.PS3(copy.deepcopy(graph.flatten(random_select))))
                        split4=graph.Ulusoy_split(graph.PS4(copy.deepcopy(graph.flatten(random_select))))
                        split5=graph.Ulusoy_split(graph.PS5(copy.deepcopy(graph.flatten(random_select))))
                        score1=self.get_q(split1)
                        score2=self.get_q(split2)
                        score3=self.get_q(split3)
                        score4=self.get_q(split4)
                        score5=self.get_q(split5)
                        if score1<min_score:
                            min_score=score1
                            min_split=split1
                            min_left=left
                        if score2<min_score:
                            min_score=score2
                            min_split=split2
                            min_left=left
                        if score3<min_score:
                            min_score=score3
                            min_split=split3
                            min_left=left
                        if score4<min_score:
                            min_score=score4
                            min_split=split4
                            min_left=left
                        if score5<min_score:
                            min_score=score5
                            min_split=split5
                            min_left=left

            for i in min_left:
                min_split.append(i)
            return min_split

    def best_BIH(self):
        population=queue.PriorityQueue()
        gene_set=set()
        counter=0
        misstime=0
        while time.time()-start<float(termin_time):
            copy_gene=self.get_gene2()
            tuple_gene=self.list_2_tuple(copy_gene)
            if tuple_gene not in gene_set:
                counter+=1
                gene_set.add(tuple_gene)
                new_individual=Individual(copy_gene, self.get_q(copy_gene))
                population.put_nowait(new_individual)
                misstime=0
            else:
                misstime+=1
                if misstime>100:
                    break       
        best=population.get()
        self.gene_output(best.gene)

    def cross_over(self,gene1,gene2):
        k1=random.randint(0,len(gene1)-1)
        k2=random.randint(0,len(gene2)-1)
        # print(k1)
        # print(k2)
        R1=gene1[k1]
        R2=gene2[k2]
        # print(f'R1 is {R1}')
        # print(f'R2 is {R2}')
        while len(R1)<2:
            k1=random.randint(0,len(gene1)-1)
            R1=gene1[k1]
        while len(R2)<2:
            k2=random.randint(0,len(gene2)-1)
            R2=gene2[k2]

        s1=random.randint(1,len(R1)-1)
        s2=random.randint(1,len(R2)-1)
        R11=R1[:s1]         
        R22=R2[s2:]
        new=R11+R22
        miss=[]
        dup=[]
        for i in new:
            if i not in R1:
                dup.append(i)
        for i in R1:
            if i not in new:
                miss.append(i)
        for i in dup:
            new.remove(i)

        for i in miss:
            task_k=self.task_dic[i]
            min_distance=1000000000
            min_list=[]
            for j in range(len(new)):
                insert_index=j
                if insert_index==0:
                    after=self.task_dic[new[insert_index]]
                    disx=self._all_distance[self._depot][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][after[0]]
                    disy=self._all_distance[self._depot][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][after[0]]
                    if disx<min_distance :
                        min_list=[]
                        min_list.append((j,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((j,True))
                        min_distance=disx                 
                    if disy<min_distance:
                        min_list=[]
                        min_list.append((j,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((j,False))
                        min_distance=disy
                elif insert_index==(len(new)-1):
                    before=self.task_dic[new[insert_index]]
                    disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][self._depot]
                    disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][self._depot]   
                    if disx<min_distance :
                        min_list=[]
                        min_list.append((j,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((j,True))
                        min_distance=disx                 
                    if disy<min_distance:
                        min_list=[]
                        min_list.append((j,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((j,False))
                        min_distance=disy
                else:
                    before=self.task_dic[new[insert_index-1]]
                    after=self.task_dic[new[insert_index]]
                    disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][after[0]]
                    disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][after[0]]
                    if disx<min_distance :
                        min_list=[]
                        min_list.append((j,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((j,True))
                        min_distance=disx                 
                    if disy<min_distance:
                        min_list=[]
                        min_list.append((j,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((j,False))
                        min_distance=disy
        
            k=random.randint(0,len(min_list)-1)
            min_index=min_list[k][0]
            min_s=min_list[k][1]
            if not min_s:
                task_k=(task_k[1],task_k[0])
            new.insert(min_index,self.id_dic[(task_k[0],task_k[1])])
        gene1.pop(k1)
        gene1.insert(k1,new)
        return gene1

    def PS(self,unordered_list):
        tasklist=[]
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.append((s,t,c,d,self._depot))
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        
        while len(tasklist)>0:
            tasklist.sort(key = lambda x:min(graph._all_distance[now][x[0]],graph._all_distance[now][x[1]]))
            min_list=[]
            min_dis=min(self._all_distance[now][tasklist[0][0]],self._all_distance[now][tasklist[0][1]])
            for i in tasklist:
                if min(self._all_distance[now][i[0]],self._all_distance[now][i[1]])==min_dis and i[3]+task_sum<self._capacity :
                    min_list.append(i)
            if min_list==[]:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
                break
            np.random.shuffle(min_list)
            min_task=min_list[0]
            tasklist.remove(min_task)
            task_sum+=min_task[3]
            if self._all_distance[now][min_task[0]]<self._all_distance[now][min_task[1]]:
                route.append(self.id_dic[(min_task[0],min_task[1])])
            else:
                route.append(self.id_dic[(min_task[1],min_task[0])])

            now=min_task[1]
            if now==self._depot:
                task_sum=0
                gene.append(route)
                route=[]
        
        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def PS1(self,unordered_list):
        tasklist=queue.PriorityQueue()
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=0
                max_distance=-1000000
                for i in range(len(min_list)):
                    task=copy.deepcopy(candidate[min_list[i][0]])
                    s=min_list[i][1]
                    if not s:
                        temp=task.s
                        task.s=task.t
                        task.t=temp
                    dis=self._all_distance[self._depot][task.s]
                    if dis>max_distance:
                        k=i
                        max_distance=dis
                    
                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)

                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def PS2(self,unordered_list):
        tasklist=queue.PriorityQueue()
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=0
                min_distance=1000000
                for i in range(len(min_list)):
                    task=copy.deepcopy(candidate[min_list[i][0]])
                    s=min_list[i][1]
                    if not s:
                        temp=task.s
                        task.s=task.t
                        task.t=temp
                    dis=self._all_distance[self._depot][task.s]
                    if dis<min_distance:
                        k=i
                        min_distance=dis
                    
                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)

                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def PS3(self,unordered_list):
        tasklist=queue.PriorityQueue()
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=0
                max_ratio=-1000000
                for i in range(len(min_list)):
                    task=copy.deepcopy(candidate[min_list[i][0]])
                    s=min_list[i][1]
                    if not s:
                        temp=task.s
                        task.s=task.t
                        task.t=temp
                    ratio=task.d/task.c
                    if ratio>max_ratio:
                        k=i
                        max_ratio=ratio
                    
                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)

                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def PS4(self,unordered_list):
        tasklist=queue.PriorityQueue()
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=0
                min_ratio=1000000
                for i in range(len(min_list)):
                    task=copy.deepcopy(candidate[min_list[i][0]])
                    s=min_list[i][1]
                    if not s:
                        temp=task.s
                        task.s=task.t
                        task.t=temp
                    ratio=task.d/task.c
                    if ratio<min_ratio:
                        k=i
                        min_ratio=ratio
                    
                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)

                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def PS5(self,unordered_list):
        tasklist=queue.PriorityQueue()
        for i in unordered_list:
            task=self.task_dic[i]
            s=int(task[0])
            t=int(task[1])
            c=self.cost_dic[task]
            d=self.demand_dic[task]
            if d!=0:
                tasklist.put_nowait(Edge(s,t,c,d))
        candidate=[]
        route=[]
        gene=[]
        now=self._depot
        task_sum=0 
        while not tasklist.empty():
            while not tasklist.empty():
                leastd=tasklist.get()
                if leastd.d+task_sum<=self._capacity:
                    candidate.append(leastd)
                else:
                    tasklist.put_nowait(leastd)
                    break
            if len(candidate)==0:
                task_sum=0
                gene.append(route)
                route=[]
                now=self._depot
            else:
                min_distance=1000000000
                min_list=[]
                for i in range(len(candidate)):
                    taski=candidate[i]
                    disx=self._all_distance[taski.s][now]
                    disy=self._all_distance[taski.t][now]

                    if disx<min_distance :
                        min_list=[]
                        min_list.append((i,True))
                        min_distance=disx
                    elif disx==min_distance:
                        min_list.append((i,True))
                        min_distance=disx                 

                    if disy<min_distance:
                        min_list=[]
                        min_list.append((i,False))
                        min_distance=disy     
                    elif disy==min_distance:
                        min_list.append((i,False))
                        min_distance=disy

                k=0
                if task_sum<self._capacity/2:
                    max_distance=-1000000
                    for i in range(len(min_list)):
                        task=copy.deepcopy(candidate[min_list[i][0]])
                        s=min_list[i][1]
                        if not s:
                            temp=task.s
                            task.s=task.t
                            task.t=temp
                        dis=self._all_distance[self._depot][task.s]
                        if dis>max_distance:
                            k=i
                            max_distance=dis
                else:
                    min_distance=1000000
                    for i in range(len(min_list)):
                        task=copy.deepcopy(candidate[min_list[i][0]])
                        s=min_list[i][1]
                        if not s:
                            temp=task.s
                            task.s=task.t
                            task.t=temp
                        dis=self._all_distance[self._depot][task.s]
                        if dis<min_distance:
                            k=i
                            min_distance=dis    

                min_index=min_list[k][0]
                min_s=min_list[k][1]
                min_task=candidate.pop(min_index)

                if not min_s:
                    temp=min_task.s
                    min_task.s=min_task.t
                    min_task.t=temp
                for i in candidate:
                    tasklist.put_nowait(i)

                candidate=[]
                task_sum+=min_task.d
                route.append(self.id_dic[(min_task.s,min_task.t)])
                now=min_task.t

        gene.append(route)
        task_sum=0
        now=self._depot 
        return self.flatten(gene)

    def memetic_evolution(self,psize):
        pop=[]
        gene_set=set()
        q_dict={}
        
        while len(pop)<psize:
            trial=0
            copy_gene=None
            tuple_gene=None
            while True:
                trial+=1
                copy_gene=self.get_gene()
                tuple_gene=self.list_2_tuple(copy_gene)
                if trial==50 or tuple_gene not in gene_set:
                    break
            if tuple_gene in gene_set:
                break
            pop.append(copy_gene)
            gene_set.add(tuple_gene)
            q_dict[tuple_gene]=self.get_q(copy_gene)

        psize=len(pop)

        while time.time()-start<float(termin_time):
            popt=copy.deepcopy(pop)
            sett=copy.deepcopy(gene_set)
            for i in range(6*psize):
                if time.time()-start>float(termin_time):
                    break
                s1=random.randint(0,psize-1)
                s2=random.randint(0,psize-1) 
                while s1==s2:
                    s2=random.randint(0,psize-1) 
                S1=pop[s1]
                S2=pop[s2]
                Sx_gene=self.cross_over(copy.deepcopy(S1),copy.deepcopy(S2))
                # print(f's1 {self.get_q(S1)} s2 {self.get_q(S2)} s3 {self.get_q(Sx_gene)}')
                r= random.random()
                if r<0.2:          
                    rr=random.random()
                    Sls_gene=None
                    if rr<0.33:
                        Sls_gene=self.single_local_search(Sx_gene)
                    elif rr<0.66:
                        Sls_gene=self.double_local_search(Sx_gene)  
                    else:
                        Sls_gene=self.swap_local_search(Sx_gene)
                                
                    Sls_tuple=self.list_2_tuple(Sls_gene)
                    Sx_tuple=self.list_2_tuple(Sx_gene)
                    q_dict[Sls_tuple]=self.get_q(Sls_gene)
                    q_dict[Sx_tuple]=self.get_q(Sx_gene)

                    ms_gene=self.MS_local_search(Sls_gene)
                    ms_q=self.get_q(ms_gene)
                    q_dict[self.list_2_tuple(ms_gene)]=ms_q
                    if ms_q<q_dict[Sls_tuple]:
                        Sls_gene=ms_gene

                    if Sls_tuple not in sett:
                        popt.append(Sls_gene)
                        sett.add(Sls_tuple)
                        
                    elif Sx_tuple not in sett:
                        popt.append(Sx_gene)
                        sett.add(Sx_tuple)
                       
                else:
                    Sx_tuple=self.list_2_tuple(Sx_gene)
                    if Sx_tuple not in sett:
                        popt.append(Sx_gene)
                        sett.add(Sx_tuple)
                        q_dict[Sx_tuple]=self.get_q(Sx_gene)
            rank=queue.PriorityQueue()
            for i in popt:
                rank.put_nowait(Individual(i,q_dict[self.list_2_tuple(i)]))
            pop=[]
            for i in range(psize):
                pop.append(rank.get().gene)
             
        min_gene=None
        min_value=1000000000000
        for i in pop:
            q=q_dict[self.list_2_tuple(i)]
            if q<min_value:
                min_gene=i
                min_value=q
        self.gene_output(min_gene)   
        return min_gene

    def memetic_evolution2(self,psize):
        population=queue.PriorityQueue()
        gene_set=set()
        counter=0

        while time.time()-start<float(termin_time)/2:
            r=np.random.rand()
            if r>0.5:
                copy_gene=self.get_gene2()
            else:
                copy_gene=self.get_gene()
            tuple_gene=self.list_2_tuple(copy_gene)
            if tuple_gene not in gene_set:
                counter+=1
                gene_set.add(tuple_gene)
                new_individual=Individual(copy_gene, self.get_q(copy_gene))
                population.put_nowait(new_individual)

        g=0
        while time.time()-start<float(termin_time):
            g+=1
            poplist=[]
            for i in range(psize):
                poplist.append(population.get())
            s1=random.randint(0,psize-1)
            s2=random.randint(0,psize-1) 
            while s1==s2:
                s2=random.randint(0,psize-1) 
            S1=poplist[s1]
            S2=poplist[s2]
            Sx_gene=self.cross_over(copy.deepcopy(S1.gene),copy.deepcopy(S2.gene))
            # print(f's1 {self.get_q(S1.gene)} s2 {self.get_q(S2.gene)} s3 {self.get_q(Sx_gene)}')
            tuple_Sx=self.list_2_tuple(Sx_gene)
            if tuple_Sx not in gene_set:
                counter+=1
                gene_set.add(tuple_Sx)
                Sx=Individual(Sx_gene, self.get_q(Sx_gene))
                population.put_nowait(Sx)
            r= random.random()
            if r<0.2:
                rp= random.random()
                Sls_gene=None
                if rp <0.3:
                    Sls_gene=self.single_local_search(Sx_gene)
                elif rp<0.6:
                    Sls_gene=self.double_local_search(Sx_gene)
                else:
                    Sls_gene=self.swap_local_search(Sx_gene)

                tuple_Sls=self.list_2_tuple(Sls_gene)

                if tuple_Sls not in gene_set:
                    counter+=1
                    gene_set.add(tuple_Sls)
                    Sls=Individual(Sls_gene, self.get_q(Sls_gene))
                    population.put_nowait(Sls) 
                    MS_Sls_gene=self.MS_local_search(Sls_gene)
                    tuple_Sls=self.list_2_tuple(MS_Sls_gene)
                    # print(f's1 {self.get_q(S1.gene)} s2 {self.get_q(S2.gene)} s3 {self.get_q(Sx_gene)} Sls {self.get_q(Sls_gene)} Ms {self.get_q(MS_Sls_gene)}')
                    if tuple_Sls not in gene_set:
                        counter+=1
                        gene_set.add(tuple_Sls)
                        Sls=Individual(MS_Sls_gene, self.get_q(MS_Sls_gene))
                        population.put_nowait(Sls)  

            for i in range(psize):
                population.put_nowait(poplist[i])

        best=population.get()
        self.gene_output(best.gene)
        return best.gene

    def mul_BIH(self,population):
        gene_set=set()
        counter=0
        misstime=0
        while time.time()-start<float(termin_time):
            copy_gene=self.get_gene2()
            tuple_gene=self.list_2_tuple(copy_gene)
            if tuple_gene not in gene_set:
                counter+=1
                gene_set.add(tuple_gene)
                new_individual=Individual(copy_gene, self.get_q(copy_gene))
                population.put(new_individual)
                misstime=0
            else:
                misstime+=1
                if misstime>100:
                    break       
            # best=population.get()
            # self.gene_output(best.gene)
            
graph=Graph(vertices,depot,required,non_required,vehicles,capacity,total_cost,edge_list)
if __name__=='__main__':
    population=Queue()
    processes =[Process(target=graph.mul_BIH,args=(population,)) for _ in range(8)]

    for p in processes:
        p.start()
    
    for p in processes:
        p.join()
    results=[queue.get() for _ in processes]
    results.sort()
    graph.gene_output(results[0].gene)