
#include "job.h"

Job::Job() {}

bool compare(Task first, Task second)
{
    return first.getTaskIndex() < second.getTaskIndex();
}

void Job::sortTasks() {
    sort(tasks.begin(), tasks.end(), compare);
}

long Job::getJobId() const {
    return jobID;
}

long Job::getTime() const {
    return time;
}

long Job::getPriority() const {
    return priority;
}

void Job::setJobId(long jobId) {
    this->jobID = jobId;
}

void Job::setTime(long time) {
    this->time = time;
}

void Job::setPriority(long priority) {
    this->priority = priority;
}
