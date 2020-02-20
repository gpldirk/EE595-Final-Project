
#include "task.h"

Task::Task() {}

float Task::getRequestedCpu() const {
    return requested_CPU;
}

float Task::getRequestedMemory() const {
    return requested_memory;
}

long Task::getPriority() const {
    return priority;
}

long Task::getTime() const {
    return time;
}

void Task::setRequestedCpu(float requestedCpu) {
    requested_CPU = requestedCpu;
}

void Task::setRequestedMemory(float requestedMemory) {
    requested_memory = requestedMemory;
}

void Task::setPriority(long priority) {
    Task::priority = priority;
}

void Task::setTime(long time) {
    Task::time = time;
}

long Task::getJobId() const {
    return jobID;
}

void Task::setJobId(long jobId) {
    jobID = jobId;
}

long Task::getMachineId() const {
    return machineID;
}

void Task::setMachineId(long machineId) {
    machineID = machineId;
}

long Task::getMissingInfo() const {
    return missing_info;
}

long Task::getTaskIndex() const {
    return task_index;
}

void Task::setMissingInfo(long missingInfo) {
    missing_info = missingInfo;
}

void Task::setTaskIndex(long taskIndex) {
    task_index = taskIndex;
}

const string &Task::getPlatformId() const {
    return platformID;
}

void Task::setPlatformId(const string &platformId) {
    platformID = platformId;
}
