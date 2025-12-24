import os
import time

# ---------- CONFIG ----------
STEP_DELAY = 2  # adjust the delay (in seconds)

# ---------- ANSI ----------
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

CLEAR = "cls" if os.name == "nt" else "clear"


# ---------- Doubly Linked List Node ----------
class Node:
    def __init__(self, key):
        self.key = key
        self.prev = None
        self.next = None


# ---------- LRU CACHE ----------
class TeachingLRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head = Node("HEAD")
        self.tail = Node("TAIL")
        self.head.next = self.tail
        self.tail.prev = self.head

        self.hits = 0
        self.misses = 0

    # ---------- Drawing Utilities ----------
    def clear(self):
        os.system(CLEAR)

    def pause(self, msg=None):
        if msg:
            print(f"\n{CYAN}{msg}{RESET}")
        time.sleep(STEP_DELAY)

    # ---------- Draw on Screen ----------
    def draw(self, action="", highlight=None, evicted=None):
        self.clear()
        print(f"{BOLD}📘 LRU Cache Teaching Demo (DLL + HashMap){RESET}")
        print("-" * 65)
        print(f"Capacity: {self.capacity}")
        print(f"Action  : {action}")
        print(f"Hits    : {GREEN}{self.hits}{RESET}   "
              f"Misses : {RED}{self.misses}{RESET}")
        print()

        # Doubly linked list Visualization
        print("Doubly Linked List:")
        cur = self.head
        while cur:
            if cur == self.head:
                print(f"[{YELLOW}HEAD{RESET}]", end=" ⇄ ")
            elif cur == self.tail:
                print(f"[{YELLOW}TAIL{RESET}]", end="")
            else:
                color = GREEN if cur == self.head.next else RED if cur == self.tail.prev else RESET
                if cur.key == highlight:
                    print(f"[{CYAN}{cur.key}{RESET}]", end=" ⇄ ")
                else:
                    print(f"[{color}{cur.key}{RESET}]", end=" ⇄ ")
            cur = cur.next
        print("\n(MRU near HEAD ←→ LRU near TAIL)")

        if evicted:
            print(f"\n{RED}❌ Evicted node: {evicted}{RESET}")

        time.sleep(STEP_DELAY)

    # ---------- Doubly Linked List Operations ----------
    def _remove(self, node):
        self.draw(f"Removing node {node.key}", highlight=node.key)
        self.pause("Detach node from its neighbors")
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_after_head(self, node):
        self.draw(f"Inserting node {node.key} at MRU position", highlight=node.key)
        self.pause("Insert node right after HEAD")
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    # ---------- LRU Cache Operations ----------
    def get(self, key):
        self.draw(f"GET {key}")
        self.pause("Lookup key in hashmap")

        if key not in self.map:
            self.misses += 1
            self.draw(f"GET {key} → MISS")
            self.pause("Key not found")
            return

        self.hits += 1
        node = self.map[key]
        self._remove(node)
        self._insert_after_head(node)

        self.draw(f"GET {key} → HIT (Moved to MRU)")
        self.pause("Accessed nodes become MRU")

    def put(self, key):
        self.draw(f"PUT {key}")
        self.pause("Insert or update operation")

        if key in self.map:
            node = self.map[key]
            self._remove(node)
            self._insert_after_head(node)
            self.draw(f"PUT {key} (Updated & MRU)")
            return

        if len(self.map) >= self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
            self.draw("Evicting LRU", evicted=lru.key)
            self.pause("LRU evicted due to capacity")

        new_node = Node(key)
        self.map[key] = new_node
        self._insert_after_head(new_node)
        self.draw(f"PUT {key} (Inserted at MRU)")
        self.pause("New items always start as MRU")


# ---------- Automatic Mode, add more operations here ----------
def automated_demo():
    cache = TeachingLRUCache(capacity=3)
    ops = [("put", 1), ("put", 2), ("put", 3),
           ("get", 1), ("put", 4), ("get", 2)]

    for op, key in ops:
        if op == "put":
            cache.put(key)
        else:
            cache.get(key)

    cache.pause("🎓 Automated demo finished")


def interactive_demo():
    cache = TeachingLRUCache(capacity=3)
    print("\nInteractive mode commands:")
    print("  put <key>")
    print("  get <key>")
    print("  exit\n")

    while True:
        cmd = input("LRU> ").strip().lower()
        if cmd == "exit":
            break
        try:
            op, key = cmd.split()
            key = int(key)
            if op == "put":
                cache.put(key)
            elif op == "get":
                cache.get(key)
            else:
                print("Unknown command")
        except ValueError:
            print("Invalid format. Use: put 1 / get 1")


if __name__ == "__main__":
    mode = input("Choose mode: [A]utomated / [I]nteractive: ").strip().lower()
    if mode == "i":
        interactive_demo()
    else:
        automated_demo()
