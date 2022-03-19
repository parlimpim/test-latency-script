# import pymongo
import pymongo_sl
from pymongo_sl.cache_client import LocalCacheClient
import numpy as np
import time

cache_client = LocalCacheClient()
client = pymongo_sl.MongoClientSL(host="localhost", port=27017, cache_client=cache_client)
slserver_db = client["slserver"]
pipeline_rt = slserver_db["pm.pipeline_rt"]

N = 10

def find(region=None):
    assert region != None, "arg `region` should not be None"
    [_ for _ in pipeline_rt.find({ "region": region })]

def insert_one(region=None):
    assert region != None, "arg `region` should not be None"
    [_ for _ in pipeline_rt.find({ "region": region })]

def update_one(region=None):
    assert region != None, "arg `region` should not be None"
    [_ for _ in pipeline_rt.find({ "region": region })]

def find(region=None):
    assert region != None, "arg `region` should not be None"
    [_ for _ in pipeline_rt.find({ "region": region })]
    

def evaluate(func, **kwargs):
    latency = np.zeros(N)
    print(f"""start running {func.__name__}({'.'.join([f"{x}={y}" for x,y in kwargs.items()])})""")
    for i in range(N):
        start = time.perf_counter()
        func(**kwargs)
        latency[i] = time.perf_counter() - start

    AVG = np.average(latency)
    P90 = np.percentile(latency, 90)
    P99 = np.percentile(latency, 99)

    return f'{round(AVG, 2) = }, {round(P90, 2) = }, {round(P99, 2) = }'


print(evaluate(find, region='singapore'))
print(evaluate(find, region='oregon'))
print(cache_client.mem)

