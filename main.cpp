#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <vector>

#include "task.h"
#include "job.h"

using namespace std;

// sorting jobs by priority from higher to lower
bool compare(Job first, Job second) {
    return  - first.getPriority() + second.getPriority();
}

// delete white space, tab in one filed
string& Trim(string &s) {
    s.erase(0,s.find_first_not_of(" "));
    s.erase(s.find_last_not_of(" ") + 1);
    return s;
}

int main() {
    map<long, Job> map;
    vector<Job> jobs;

    // task_events.csv = from part-00000-of-00500.csv to part-00499-of-00500.csv
    for (int i = 0; i < 1; i++) {
        string fileName = "./part-00" + to_string(i / 100) +
                to_string(i % 100 / 10) + to_string(i % 10) + "-of-00500.csv";
        // string fileName = "../part-00000-of-00500.csv";
        ifstream fin(fileName, ios::in);
        string line;

        int index = 0;
        while (getline(fin, line)) {
            // cout << line << endl;

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

            task.setTime(stol(Trim(fields[0])));
            // cout << task.getTime() << endl;

            task.setJobId(stol(Trim(fields[2])));
            // cout << task.getJobId() << endl;

            task.setTaskIndex(stol(Trim(fields[3])));
            // cout << task.getTaskIndex() << endl;

            task.setMachineId(stol(Trim(fields[4])));
            // cout << task.getMachineId() << endl;

            task.setPriority(stol(Trim(fields[8])));
            // cout << task.getPriority() << endl;

            task.setRequestedCpu(stof(Trim(fields[9])));
            // cout << task.getRequestedCpu() << endl;

            task.setRequestedMemory(stof(Trim(fields[10])));
            // cout << task.getRequestedMemory() << endl;

            map[task.getJobId()].tasks.push_back(task);
            map[task.getJobId()].setPriority(task.getPriority());
        }
    }

    // before putting all jobs into jobs, sort all tasks in that job by the index of task
    for(auto &kv : map) {
        kv.second.sortTasks();
        jobs.push_back(kv.second);
    }
    // sort all the jobs by its priority
    sort(jobs.begin(), jobs.end(), compare);

    // after sorting jobs and tasks, put required info of tasks into txt file
    ofstream fout("./tasks.txt");
    for (int i = 0; i < jobs.size(); i++) {
        for (int j = 0; j < jobs[i].tasks.size(); j++) {
            fout << jobs[i].tasks[j].getRequestedCpu() << " " << jobs[i].tasks[j].getRequestedMemory() << " "
            << jobs[i].tasks[j].getMachineId() << " " << jobs[i].tasks[j].getPriority() << " " << jobs[i].tasks[j].getTime() << endl;
        }
    }

    return 0;
}