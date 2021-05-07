#include <iostream>
#include <fstream>
#include <sstream>
#include <string>

// STL library
#include <map>
#include <vector>
#include <array>
#include <queue>
// STL algorithm
#include <algorithm>

#include "task.h"
#include "job.h"
#include "base.h"

using namespace std;

// sorting jobs by priority from higher to lower (object sorting)
inline bool compare(Base first, Base second) {
    return second.getTime() - first.getTime();
}

// delete white space, tab at start or end of string (reference)
inline string& Trim(string &s) {
    s.erase(0, s.find_first_not_of(" "));
    s.erase(s.find_last_not_of(" ") + 1);
    return s;
}

int main() {
    map<long, Job> map;

    // this can be 1, 6, 9
    array<int, 3> arr = {1, 6, 9};

    // task_events.csv = "part-0000(1, 6, 9)-of-00500.csv"
    for (int i = 0; i < 3; i++) {
        string fileName = "./part-0000" + to_string(arr[i]) + "-of-00500.csv";
        ifstream fin(fileName, ios::in);
        string line;

        while (getline(fin, line)) {
            Task task;
            string field;
            vector<string> fields;
            istringstream sin(line); // put line into istringstream sin
            while (getline(sin, field, ',')) { // put istringstream sin into field and seperated by ','
                fields.push_back(field); // put filed into vector fields
            }
            // filtering missing data of tasks
            if (fields[0] == "" || fields[2] == "" || fields[3] == "" || fields[4] == "") {
                continue;
            }
            if (fields[8] == "" || fields[9] == "" || fields[10] == "") {
                continue;
            }

            Base * base = &task;
            // timestamp
            base->setTime(stol(Trim(fields[0])));
            // cout << base->getTime() << endl;

            // jobID
            base->setJobId(stol(Trim(fields[2])));
            // cout << base->getJobId() << endl;

            // taskIndex
            task.setTaskIndex(stol(Trim(fields[3])));
            // cout << task.getTaskIndex() << endl;

            // machineID
            // task.setMachineId(stol(Trim(fields[4])));
            // cout << task.getMachineId() << endl;

            // priority
            // task.setPriority(stol(Trim(fields[8])));
            // cout << task.getPriority() << endl;

            // req_CPU
            task.setRequestedCpu(stof(Trim(fields[9])));
            // cout << task.getRequestedCpu() << endl;

            // req_memory
            task.setRequestedMemory(stof(Trim(fields[10])));
            // cout << task.getRequestedMemory() << endl;

            map[task.getJobId()].tasks.push_back(task);
            map[task.getJobId()].setPriority(task.getPriority());
        }

        // sort all tasks in that job by the index of task from low to high
        queue<vector<Task>> q;
        for(auto &kv : map) {
            kv.second.sortTasks();
            q.push(kv.second.tasks);
        }

        // sort all the jobs by its priority from high to low -- UPDATE: Not needed, this would kill the time order
        // sort(jobs.begin(), jobs.end(), compare); 

        // after sorting jobs and tasks, put required info of tasks into txt file
        ofstream fout("./tasks-" + to_string(arr[i])+ ".txt");
        while(!q.empty()) {
            vector<Task> tasks = q.front();
            q.pop();
            for (int j = 0; j < tasks.size(); j++) {
                fout << tasks[j].getTime() << " " << tasks[j].getJobId() << " " << tasks[j].getRequestedCpu() << " " << tasks[j].getRequestedMemory() << " " << tasks[j].getPriority() << endl;
                /*<< jobs[i].tasks[j].getMachineId() << " " << jobs[i].tasks[j].getPriority() */
            }
        }
    }
    
    return 0;
}
