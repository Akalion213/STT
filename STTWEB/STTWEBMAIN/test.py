from search import video_search
import os
from os.path import dirname, abspath
import ast
import time


STT_dir = 'C:/Programs/STTLEX/subs/txt_time_subs'
results = 0
total_time = 0
for i in range(1, 2):
    t0 = time.time()
    for filename in os.listdir(STT_dir):
        results += video_search(filename, ['racist', 'homophobic'])
    total_time += time.time() - t0

print(total_time)
print(results)
