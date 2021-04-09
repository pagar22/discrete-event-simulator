from des import SchedulerDES
from process import Process
from process import ProcessStates
from event import Event, EventTypes


class FCFS(SchedulerDES):
    def scheduler_func(self, cur_event):
        # pop first process from list since list is already sorted by arrival time and return it
        run_process = self.processes.pop(0)
        run_process.process_state = ProcessStates.READY
        return run_process

    def dispatcher_func(self, cur_process):
        run_time = cur_process.run_for(cur_process.service_time, self.time)
        # if process finished executing, terminate and add to end of list
        if (run_time == cur_process.service_time):  # always true but still added
            cur_process.process_state = ProcessStates.TERMINATED
            self.processes.append(cur_process)
        event_run = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                          event_time=self.time)
        return event_run


class SJF(SchedulerDES):
    def scheduler_func(self, cur_event):
        # sort according to amount of service time and pop and return the first process
        self.processes.sort(key=lambda x: x.service_time)
        for i in range(len(self.processes)):
            p = self.processes.__getitem__(i)
            if p.process_state != ProcessStates.TERMINATED:
                run_process = self.processes.pop(i)
                run_process.process_state = ProcessStates.READY
                return run_process

    def dispatcher_func(self, cur_process):
        # runs for entire service time
        run_time = cur_process.run_for(cur_process.service_time, self.time)
        if (run_time == cur_process.service_time):  # always true but still added
            cur_process.process_state = ProcessStates.TERMINATED
            self.processes.append(cur_process)
        event_run = Event(process_id=cur_process.process_id, event_type=EventTypes.PROC_CPU_DONE,
                          event_time=self.time)
        return event_run


class RR(SchedulerDES):
    def scheduler_func(self, cur_event):
        # similar to FCFS, runs processes on quantum time based on who arrives first
        for i in range(len(self.processes)):
            p = self.processes.__getitem__(i)
            if p.process_state != ProcessStates.TERMINATED:
                run_process = self.processes.pop(i)
                run_process.process_state = ProcessStates.READY
                return run_process

    def dispatcher_func(self, cur_process):
        # run for a fixed quantum of 0.5 ms
        run_time = Process.run_for(cur_process, 0.5, self.time)
        event_TYPE = EventTypes.PROC_CPU_DONE
        # if it completed, state=terminated, else state=ready and put process back in queue
        if (run_time == cur_process.remaining_time):
            cur_process.process_state = ProcessStates.TERMINATED
        else:
            cur_process.process_state = ProcessStates.READY
            event_TYPE = EventTypes.PROC_CPU_REQ

        self.processes.append(cur_process)
        event_run = Event(process_id=cur_process.process_id, event_type=event_TYPE, event_time=self.time)
        return event_run


class SRTF(SchedulerDES):
    def scheduler_func(self, cur_event):
        # sort according to amount of remaining time and pop and return the non-terminated process
        self.processes.sort(key=lambda x: x.service_time)
        for i in range(len(self.processes)):
            p = self.processes.__getitem__(i)
            if p.process_state != ProcessStates.TERMINATED:
                run_process = self.processes.pop(i)
                run_process.process_state = ProcessStates.READY
                return run_process

    def dispatcher_func(self, cur_process):
        # run for the least remaining time
        run_time = Process.run_for(cur_process, cur_process.remaining_time, self.time)
        event_TYPE= EventTypes.PROC_CPU_DONE
        if (run_time == cur_process.remaining_time):
            cur_process.process_state = ProcessStates.TERMINATED
        else:
            cur_process.process_state = ProcessStates.READY
            event_TYPE= EventTypes.PROC_CPU_REQ

        self.processes.append(cur_process)
        event_run = Event(process_id=cur_process.process_id, event_type=event_TYPE, event_time=self.time)
        return event_run