
    def single_insertion(self,input,p):
        gene=input[:]
        k1=random.randint(0,len(gene)-1)
        routek=gene[k1]
        if len(routek)>1:
            k2=random.randint(0,len(routek)-1)
        else:
            k2=0
        task_k_index=routek.pop(k2)
        task_k=self.task_dic[task_k_index]
        rp=random.random()
        if rp < p:
            if len(routek)>1:
                insert_index=random.randint(0,len(routek)-1)
                if insert_index!=(len(routek)-1):
                    before=self.task_dic[routek[insert_index]]
                    after=self.task_dic[routek[insert_index+1]]
                    disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][after[0]]
                    disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][after[0]]
                    if disx<disy:
                        routek.insert(insert_index,self.id_dic[task_k])
                    else:
                        routek.insert(insert_index,self.id_dic[(task_k[1],task_k[0])])
                else:
                    before=self.task_dic[routek[insert_index]]
                    disx=self._all_distance[before[1]][task_k[0]]+self.cost_dic[task_k]+self._all_distance[task_k[1]][self._depot]
                    disy=self._all_distance[before[1]][task_k[1]]+self.cost_dic[task_k]+self._all_distance[task_k[0]][self._depot]
                    if disx<disy:
                        routek.append(self.id_dic[task_k])
                    else:
                        routek.append(self.id_dic[(task_k[1],task_k[0])])
        else:
            route=[]
            route.append(task_k_index)
            gene.append(route)
        # emptyindex=[]
        # for i in range(len(gene)):
        #     if gene[i]==[]:
        #         emptyindex.append(i)
        # for i in emptyindex[::-1]:
        #     gene.pop(i)
        return gene
    
    def memetic_evolution(self,population_size,mutation_rate):    
        population=queue.PriorityQueue()
        gene=self.get_gene()
        best=Individual(gene, self.gene_to_q(gene))
        self.gene_output(best.gene)
        for i in range(population_size):
            new_gene=graph.single_insertion(gene[:],1)
            new_individual=Individual(new_gene[:], self.gene_to_q(new_gene[:]))
            population.put_nowait(new_individual)
        while time.time()-start<(int)(termin_time):
            best_ones=[]
            for i in range(int(population_size*mutation_rate)):
                best_ones.append(population.get())
            for i in best_ones:
                new_gene=graph.single_insertion(i.gene[:],1)
                new_individual=Individual(new_gene[:], self.gene_to_q(new_gene[:]))
                population.put_nowait(new_individual)
            for i in range(int(population_size*(1-mutation_rate))):
                best_ones.append(population.get())     
            population=queue.PriorityQueue()
            for i in range(len(best_ones)):
                population.put_nowait(best_ones[i])
            bestinp=population.get()
            population.put_nowait(bestinp)
            if bestinp.q<best.q:
                print(f'bestinp.q is {bestinp.q} and best.q is {best.q}')
                best=bestinp
        self.gene_output(best.gene)
            