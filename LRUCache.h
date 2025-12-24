#pragma once
#include <unordered_map>
#include <list>

template <typename K, typename V>
class LRUCache 
{
public:
    explicit LRUCache(size_t capacity) : capacity_(capacity) {}

    // access will insert to the front using splice.
    bool get(const K& key, V& value) 
    {
        auto it = map_.find(key);
        if (it == map_.end())
            return false;

        items_.splice(items_.begin(), items_, it->second);
        value = it->second->second;
        return true;
    }

    void put(const K& key, const V& value) 
    {
        auto it = map_.find(key);

        // if key in the update the map and insert front
        if (it != map_.end()) 
        {
            it->second->second = value;
            items_.splice(items_.begin(), items_, it->second); // replace without copy or move 
            return;
        }

        // check eviction condition
        if (items_.size() == capacity_) 
        {
            auto last = items_.back();
            map_.erase(last.first);
            items_.pop_back();
        }

        items_.emplace_front(key, value);
        map_[key] = items_.begin();
    }

private:
    size_t capacity_;
    std::list<std::pair<K, V>> items_;
    std::unordered_map<K, typename std::list<std::pair<K, V>>::iterator> map_;
};
