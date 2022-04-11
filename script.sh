#/bin/bash
pip install numpy pandas requests pymongo snaplogic-pymg
python create_pipeline.py $1 $3
mongo --host $3:27017 < sharding.js
python fetch_runtime.py $1 $2