
#ifndef PROJECT_BASE_H
#define PROJECT_BASE_H

class Base {
public:
    long getJobId() const;
    long getTime() const;
    long getPriority() const;
    void setJobId(long jobId);
    void setTime(long time);
    void setPriority(long priority);

protected:
    long jobID; // task_events table
    long time; // job_events table
    long priority; // task_events table
};

#endif //PROJECT_BASE_H
