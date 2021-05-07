
#ifndef PROJECT_JOB_H
#define PROJECT_JOB_H

#include <iostream>
#include "base.h"
#include "task.h"
#include <vector>

using namespace std;

class Job: public Base {
public:
    Job();
    Job(int jobID, int time);
    vector<Task> tasks;
    void sortTasks();
};

#endif //PROJECT_JOB_H
