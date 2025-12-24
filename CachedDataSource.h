#pragma once
#include "LRUCache.h"
#include "DataSource.h"

// builds using LRU Cache
class CachedDataSource 
{
public:
    explicit CachedDataSource(size_t cacheSize)
        : cache_(cacheSize) {}

    // if found in cache, then returns and hit rate increments
    int fetch(int key) 
    {
        int value;
        if (cache_.get(key, value)) 
        {
            hits_++;
            return value;
        }

        misses_++;

        // if not in cache fetch from the expensive source
        value = source_.fetch(key);
        // insert to cache
        // improvment: add a protective layer to prevent inserting all.
        cache_.put(key, value);
        return value;
    }

    size_t hits() const { return hits_; }
    size_t misses() const { return misses_; }

private:
    LRUCache<int, int> cache_;
    ExpensiveDataSource source_;
    size_t hits_ = 0;
    size_t misses_ = 0;
};
