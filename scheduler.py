# CS337 Project 2
# Ben Raivel
# process scheduling algorithm implementations

import re
import numpy as np
import process


def FCFS_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    first come first served scheduling algorithm
    '''
    # get process with lowest arrival
    current_process = find_lowest_arrival(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        # decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=current_process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    # set wait time and turnaround time
    current_process.wait_time = start_time - current_process.get_arrival_time()
    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
            '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
            '\twait : ' + str(current_process.wait_time) +
            '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def SJF_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    shortest job first scheduling algorithm
    '''
    # get shortest process
    current_process = find_shortest(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        #decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time
    
    # record process data to CPU list
    CPU.append(dict(process=current_process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    current_process.wait_time = start_time - current_process.get_arrival_time()

    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
            '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
            '\twait : ' + str(current_process.wait_time) +
            '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def priority_scheduler(processes, ready, CPU, time, verbose=True):
    '''
    priority scheduling algorithm
    '''
    # get process with highest
    current_process = find_highest_priority(ready)

    # set start time
    start_time = time

    # while burst time remains
    while(current_process.get_burst_time() > 0):

        #decrement burst time
        current_process.set_burst_time(current_process.get_burst_time()-1)

        # increment time
        time += 1

        # move newly arrived processes to ready queue
        add_ready(processes, ready, time)

    # set end time
    end_time = time
    
    # add process data to CPU list
    CPU.append(dict(process=current_process.get_PID(),
                    start=start_time,
                    finish=end_time,
                    priority=current_process.get_priority()))

    current_process.wait_time = start_time - current_process.get_arrival_time()

    current_process.turnaround_time = current_process.wait_time + end_time - start_time

    # print process summary
    if(verbose):
        print('PID: ' + str(current_process.get_PID()) + 
                '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
                '\twait : ' + str(current_process.wait_time) +
                '\tturnaround : ' + str(current_process.turnaround_time))

    return time

def RR_scheduler(processes, ready, waiting, CPU, time, quantum = 2, verbose=True):
    '''
    round robin scheduler
    '''
    # get earliest arrival
    process = find_lowest_arrival(ready)

    # set start time
    start_time = time

     # if response time is 0 (not set)
    if process.response_time == 0:
        
        # set to time
        process.response_time = start_time - process.get_arrival()

    # run process for one quantum
    for i in range(quantum):

        # decrement CPU
        process.get_duty()[0] -= 1

        # increment time
        time += 1

        # add newly arrived processes
        add_ready(processes, ready, time)

        # move processes done with I/O back to ready
        manage_waiting(ready, waiting, time)

        # if the process is finished with the CPU
        if process.get_duty()[0] == 0: break
        
    # set end time 
    end_time = time

    # record process data to CPU list
    CPU.append(dict(process=process.get_PID(), 
                    start=start_time,
                    finish=end_time,
                    priority=process.get_priority()))

    # update waiting, turnaround times
    process.wait_time += start_time - process.get_arrival()
    process.turnaround_time += end_time - process.get_arrival()

    # print process summary
    if(verbose):
        print('PID: ' + str(process.get_PID()) + 
            '\t[start, end]: [' + str(start_time) + ', ' + str(end_time) + ']' +
            '\twait : ' + str(process.wait_time) +
            '\tturnaround : ' + str(process.turnaround_time))


    # if the process is finished with the CPU
    if process.get_duty()[0] == 0:
        
        if len(process.get_duty()) > 1:
            waiting.append(process)

    else:
        # set new arrival time
        process.set_arrival(time)

        # add process back to ready
        ready.append(process)


    return time

def SRT_scheduler(processes, ready, waiting, CPU, time, verbose=True):
    '''
    shortest runtime first scheduler
    '''
    # find shortest process
    process = find_shortest(ready)

    # while CPU burst time remains
    while(process.get_duty()[0] > 0):

        # run for one time slice
        process.get_duty()[0] -= 1

        # check for new arrivals
        add_ready(processes, ready, time)

        # move processes that are done waiting back to ready
        manage_waiting(ready, waiting, time)

        # interrupt if there is a shorter job
        

def PP_scheduler(processes, ready, CPU, time, verbose=True):
    # find highest priority process

    # run one time slice

    # check for new arrivals

    # preempt if higher priority process arrives
    pass

# extension
def MLFQ_scheduler(processes, ready, CPU, time, verbose=True):
    pass

def find_lowest_arrival(ready):
    '''
    returns earliest-arrived process in ready
    '''
    # index of lowest arrival in ready queue
    idx = 0

    # loop over ready queue
    for i in range(len(ready)):

        # if a lower value is encountered
        if(ready[i].get_arrival() < ready[idx].get_arrival()):
            idx = i
  
        # if an equally low value is encountered use PID to break tie
        elif(ready[i].get_arrival() == ready[idx].get_arrival()):
            
            # lower PID goes first
            if(ready[i].get_PID() < ready[idx].get_PID()):
                idx = i

    # remove and return lowest arrival
    return ready.pop(idx)

def find_shortest(ready):
    '''
    returns shortest-cpu-burst process in ready
    '''
    # index of shortest process
    idx = 0

    # loop over ready processes
    for i in range(len(ready)):
        
        # if next CPU burst is less than that of shortest
        if ready[i].get_duty()[0] < ready[idx].get_duty()[0]:

            # current process is new shortest
            idx = i

        # if they are equal
        elif ready[i].get_duty()[0] == ready[idx].get_duty()[0]:

            # resolve based on PID
            if ready[i].get_PID() < ready[idx].get_PID():

                # if PID is lower current process is new shortest
                idx = i

    # remove and return
    return ready.pop(idx)

def find_highest_priority(ready):
    '''
    returns highest priority process in ready
    '''
    # index of highest priority process
    idx = 0

    # loop over ready processes
    for i in range(len(ready)):
       
        # if the current process has higher priority
        if ready[i].get_priority() > ready[idx].get_priority():

            # current is new highest
            idx = i

        # if priority is equal
        elif ready[i].get_priority() == ready[i].get_priority():

            # resolve using PID
            if ready[i].get_PID() < ready[idx].get_PID():

                # lower PID is chosen
                idx = i

    # remove and return
    return ready.pop(idx)

def add_ready(processes, ready, time):
    '''
    adds processes to ready at correct time
    '''
    # loop over processes
    for process in processes:

        # if process arrival is equal to time
        if process.get_arrival() == time:
            
            # add process to ready queue
            ready.append(process)


def manage_waiting(ready, waiting, time):
    '''
    - decrements waiting time of processes in waiting 
    - moves processes that have finished I/O from waiting to ready
    '''
    removed = 0

    # loop over waiting processes
    for i in range(len(waiting)):

        # if process is finished with I/O
        if waiting[i-removed].get_duty()[1] == 1:

            # remove process from waiting queue
            process = waiting.pop(i - removed)

            # increment removed
            removed += 1

            # slice the duty list 
            process.set_duty(process.get_duty()[2:])

            # set new arrival time
            process.set_arrival(time)

            # set process status to running
            process.set_running()
    
            # add process to ready queue
            ready.append(process)
        
        # otherwise
        else:

            # decrement waiting time in duty array
            waiting[i-removed].get_duty()[1] -= 1





def main():
    p0 = process.Process(0, 3, 0, 4)
    p1 = process.Process(1, 6, 3, 7)
    p2 = process.Process(2, 2, 9, 2)
    p3 = process.Process(3, 12, 10, 6)

    ready = [p0, p1]

    lowest_arrival = find_lowest_arrival(ready)

    print(lowest_arrival.get_arrival_time())

    ready = [p3, p2, p1]

    lowest_arrival = find_lowest_arrival(ready)

    print(lowest_arrival.get_arrival_time())

    processes = [p0, p1, p2, p3]

    ready = []

    time = 0

    add_ready(processes, ready, time)

    print(ready, processes)

if __name__ == '__main__':
    main()
