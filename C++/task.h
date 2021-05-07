
#ifndef PROJECT_TASK_H
#define PROJECT_TASK_H

#include <iostream>
#include "base.h"
using namespace std;

class Task: public Base {
public:
    Task();

    void setRequestedCpu(float requestedCpu);
    void setRequestedMemory(float requestedMemory);
    void setMachineId(long machineId);
    void setMissingInfo(long missingInfo);
    void setTaskIndex(long taskIndex);
    void setPlatformId(const string &platformId);

    const string &getPlatformId() const;
    long getMissingInfo() const;
    long getTaskIndex() const;
    float getRequestedCpu() const;
    float getRequestedMemory() const;
    long getMachineId() const;

private:
    long missing_info; // used to filter missing data (task_events table)
    long task_index; // the order within the job (task_events table)
    long machineID; // VM type  (machine_events table)
    string platformID;
    float requested_CPU; // (task_events table)
    float requested_memory; // (task_events table)
};

#endif //PROJECT_TASK_H
