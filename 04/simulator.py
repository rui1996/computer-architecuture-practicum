import cache
import json

config_file = open("config.json")
trace_file = open("1.trace")

config = json.loads(config_file.read())
config_file.close()

caches = []
for item in config["arch"]:
    caches.append(cache.Cache(item['name'],
                             item['cache-size'], 
                             item['block-size'],
                             item['set-associativity'],
                             item['replacement'],
                             item['prefetching'],
                             config['write-hit'],
                             config['write-miss'],
                             item['bus-latency'],
                             item['hit-latency'],
                             item['access-latency'],
                             config['memory-latency'],
                             item['bypass']))

for i in range(len(caches) - 1):
    caches[i].next_level = caches[i + 1]
latency = 0
for line in trace_file:
    (op, add) = line.split()
    add = int(add,16)
    if op == "r":
        latency += caches[0].read(add, False)
    elif op == "w":
        latency += caches[0].write(add)
trace_file.close()

print("------------ REPORT -------------")
for item in caches:
    print("Cache {}".format(item.name))
    print("Replacement Policy: {}".format(item.replacement))
    print("Prefetching Policy: {}".format(item.prefetching))
    print("Access: {}".format(item.access_counter))
    #print("Fallback: {}".format(item.next_level_counter))
    print("Miss: {}".format(item.miss_counter))
    print("Replace: {}".format(item.replacement_counter))
    print("Cold Miss: {}".format(item.cold_miss_cnt))
    print("Prefetch hit: {}".format(item.prefetchhit))
    print("---------------------------------")
print("Latency: {}".format(latency))

