#include <iostream>
#include <vector>
#include <random>
#include <chrono>

#include "DataSource.h"
#include "CachedDataSource.h"

using Clock = std::chrono::high_resolution_clock;

std::vector<int> generate_workload(size_t ops, int keySpace) {
    std::vector<int> keys;
    keys.reserve(ops);

    std::mt19937 rng(42);
    std::uniform_int_distribution<int> dist(1, keySpace);

    for (size_t i = 0; i < ops; ++i)
        keys.push_back(dist(rng));

    return keys;
}

template <typename Func>
long long measure(Func f) {
    auto start = Clock::now();
    f();
    auto end = Clock::now();
    return std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
}

int main() {
    const size_t OPERATIONS = 500'000;
    const int KEY_SPACE = 70;
    const size_t CACHE_SIZE = 50;

    auto workload = generate_workload(OPERATIONS, KEY_SPACE);

    ExpensiveDataSource rawSource;
    CachedDataSource cachedSource(CACHE_SIZE);

    std::cout << "Running benchmark...\n";

    auto rawTime = measure([&] {
        for (int key : workload)
            rawSource.fetch(key);
    });

    auto cachedTime = measure([&] {
        for (int key : workload)
            cachedSource.fetch(key);
    });

    std::cout << "\n===== RESULTS =====\n";
    std::cout << "Operations      : " << OPERATIONS << "\n";
    std::cout << "Key space       : " << KEY_SPACE << "\n";
    std::cout << "Cache size      : " << CACHE_SIZE << "\n\n";

    std::cout << "No cache time   : " << rawTime << " ms\n";
    std::cout << "LRU cache time  : " << cachedTime << " ms\n";

    std::cout << "\nCache hits      : " << cachedSource.hits() << "\n";
    std::cout << "Cache misses   : " << cachedSource.misses() << "\n";

    double speedup = (double)rawTime / cachedTime;
    std::cout << "\nSpeedup         : " << speedup << "x\n";
}
