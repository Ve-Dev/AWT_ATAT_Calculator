from copy import deepcopy
class Calcy:
    def __init__(self, no_of_processes, datastore, rq, gc):
        self.no_of_processes=no_of_processes
        self.datastore=datastore
        self.rq=rq
        self.gc=gc
        self.data_copy=[]

    def take_input(self, process_dict):
        for i in range(self.no_of_processes):
            self.datastore.update({f'P{i+1}' : []})
            self.datastore[f'P{i+1}'].append(process_dict['process_input'][2*i])
            self.datastore[f'P{i+1}'].append(process_dict['process_input'][2*i+1])
        self.data_copy=deepcopy(self.datastore)
        
    def processor(self, choice):
        cycle=0
        while cycle in range(30):
            self.push_rq(cycle)
            if choice == 'sjf':
                cycle=self.sjf(cycle)
            elif choice == 'srtf':
                self.srtf(cycle)
            cycle+=1

    def push_rq(self, cycle_no):
        for key in self.datastore:
            if cycle_no == self.datastore[key][0]:
                self.rq.append(key)

    def calc_WT(self, process):
        temp=[]
        for i, j in enumerate(self.gc):
            if j == process:
                temp.append(i)
        wt, i= temp[0]-self.datastore[process][0], 1
        i=0
        for i in range(len(temp)):
            if i<len(temp)-1 and (temp[i+1] - temp[i]) != 1:
                wt+=temp[i+1]-temp[i]-1
        self.datastore[process].append(wt)

    def calc_ta(self, process):
        self.datastore[process].append(self.data_copy[process][1]+self.datastore[process][2])

    def calc_avg_ta(self):
        for process in self.datastore:
            self.calc_ta(process)
        avg_ta, count=0, 0
        for process in self.datastore:
            avg_ta+=self.datastore[process][3]
            count+=1
        return avg_ta/count

    def calc_avg_wt(self):
        for process in self.datastore:
            self.calc_WT(process)
        avg_wt, count=0, 0
        for process in self.datastore:
            avg_wt+=self.datastore[process][2]
            count+=1
        return avg_wt/count

    def srtf(self, cycle_no):
        for process in self.datastore:
            if self.datastore[process][0] <= cycle_no and self.datastore[process][1] != 0 and process not in self.rq:
                self.rq.append(process)
        current_process=self.minimum_bt()
        if current_process != -1 and current_process !='':
            if current_process in self.rq:
                self.rq.remove(current_process)
                self.gc.append(current_process)
            if self.datastore[current_process][1] > 0:
                self.datastore[current_process][1]-=1
        elif current_process == '':
            self.gc.append(current_process)

    def minimum_bt(self):
        min_process=''
        if len(self.gc) != 0 and self.gc[-1] != '' and self.datastore[self.gc[-1]][1] != 0:
            min_bt=self.datastore[self.gc[-1]][1]
            min_process=self.gc[-1]
        elif len(self.rq) != 0:
            min_bt=self.datastore[self.rq[0]][1]
        for process in self.rq:
            if self.datastore[process][1] <= min_bt:
                min_bt=self.datastore[process][1]
                min_process=process
        return min_process 

    def output(self):
        return self.calc_avg_wt(), self.calc_avg_ta()
    
    def completion_time_calc(self):
        for process in self.datastore:
            self.datastore[process].append(self.datastore[process][1]+self.datastore[process][2])

#POST={'process_input' : [3,1,1,4]}
#obj1=Calcy(2, {}, [], [])
#obj1.take_input(POST)
#obj1.processor('srtf')
#print(obj1.output())
#print(obj1.datastore)


            
