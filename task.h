
#ifndef PROJECT_TASK_H
#define PROJECT_TASK_H

#include <iostream>
using namespace std;

class Task {
public:
    Task();

    void setJobId(long jobId);
    void setRequestedCpu(float requestedCpu);
    void setRequestedMemory(float requestedMemory);
    void setMachineId(long machineId);
    void setPriority(long priority);
    void setTime(long time);
    void setMissingInfo(long missingInfo);
    void setTaskIndex(long taskIndex);
    void setPlatformId(const string &platformId);

    const string &getPlatformId() const;
    long getMissingInfo() const;
    long getTaskIndex() const;
    long getJobId() const;
    float getRequestedCpu() const;
    float getRequestedMemory() const;
    long getMachineId() const;
    long getPriority() const;
    long getTime() const;

private:
    long time; // Soft deadline of task  (task_events table)
    long missing_info; // used to filter missing data (task_events table)
    long jobID; // specify which job this task belong to (task_events table)
    long task_index; // the order within the job (task_events table)
    long machineID; // VM type  (machine_events table)
    long priority; // Priority  (task_events table)
    string platformID;
    float requested_CPU; // (task_events table)
    float requested_memory; // (task_events table)
};

#endif //PROJECT_TASK_H
