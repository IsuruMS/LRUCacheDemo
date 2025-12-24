#pragma once
#include <thread>
#include <chrono>


// the benchmark demo will use this class to mimick access of data from the disk in case a cache is not hit.
class ExpensiveDataSource 
{
public:
    int fetch(int key) {
        // Simulate DB / disk / network latency
        volatile int sum = 0;
        for (int i = 0; i < 50000; i++)
            sum += key * i;
        return sum;
    }
};
