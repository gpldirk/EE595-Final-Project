
#ifndef PROJECT_JOB_H
#define PROJECT_JOB_H

#include <iostream>
#include "task.h"
#include <vector>

using namespace std;

class Job {
public:
    Job();
    Job(int jobID, int time);
    vector<Task> tasks;
    void sortTasks();

    long getJobId() const;
    long getTime() const;
    long getPriority() const;

    void setJobId(long jobId);
    void setTime(long time);
    void setPriority(long priority);

private:
    long jobID; // task_events table
    long time; // job_events table
    long priority; // task_events table
};

#endif //PROJECT_JOB_H
