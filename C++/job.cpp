#include <algorithm>
#include "job.h"

Job::Job() {}

bool compare(Task first, Task second)
{
    return first.getTime() < second.getTime();
}

void Job::sortTasks() {
    sort(tasks.begin(), tasks.end(), compare);
}

