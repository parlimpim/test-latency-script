import pymongo_sl
from pymongo_sl.cache_client import LocalCacheClient

mongo_host = "localhost"

cache_client = LocalCacheClient()
client = pymongo_sl.MongoClientSL(host=mongo_host, port=27017, cache_client=cache_client)
slserver_db = client["slserver"]
pipeline_rt = slserver_db["pm.pipeline_rt"]

pipeline_rt.update_many({"org_snode_id": "62238b04b84c910ac0a98bb6"}, {"$set": {"region": "singapore"}})
pipeline_rt.update_many({"org_snode_id": "62238b03b84c910ac0a98b9b"}, {"$set": {"region": "oregon"}})
pipeline_rt.ensure_index({"region": 1, "_id": "hashed"})
slserver_db.command('enableSharding',"slserver_db")
slserver_db.command('shardCollection', "slserver", {"region": 1, "_id": "hashed"})
slserver_db.command('addShardTag', { "us-west-2", "oregon" })
slserver_db.command('addShardTag', { "ap-southeast-1", "singapore" })
slserver_db.command('addTagRange', "pipeline_rt", { {"region": "oregon", "_id": 0}, {"region": "oregon", "_id": 9999}, "oregon"} )
slserver_db.command('addTagRange', "pipeline_rt", { {"region": "singapore", "_id": 0}, {"region": "singapore", "_id": 9999}, "singapore"} )


# sh.enableSharding("slserver")
# sh.shardCollection("slserver.pm.pipeline_rt", {"region": 1, "_id": "hashed"})
# sh.addShardTag("us-west-2", "oregon")
# sh.addShardTag("ap-southeast-1", "singapore")
# sh.addTagRange("slserver.pm.pipeline_rt", {"region": "oregon", "_id": 0}, {"region": "oregon", "_id": 9999}, "oregon")
# sh.addTagRange("slserver.pm.pipeline_rt", {"region": "singapore", "_id": 0}, {"region": "singapore", "_id": 9999}, "singapore")