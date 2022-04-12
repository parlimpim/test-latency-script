#/bin/bash
pip3 install numpy pandas requests pymongo
python3 create_pipeline.py $1 $3
mongo --host $3:27017 < sharding.js
python3 fetch_runtime.py $1 $2