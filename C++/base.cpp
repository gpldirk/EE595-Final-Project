#include "base.h"

void Base::setJobId(long jobId) {
    this->jobID = jobId;
}

void Base::setTime(long time) {
    this->time = time;
}

void Base::setPriority(long priority) {
    this->priority = priority;
}

long Base::getJobId() const {
    return this->jobID;
}

long Base::getTime() const {
    return this->time;
}

long Base::getPriority() const {
    return this->priority;
}
