import requests
import json
import sys
from pymongo import MongoClient

def create_pipeline(org_id: str, name: str, org_name: str):
    endpoint = f'{host}/api/2/{org_id}/rest/pipeline/create'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    params = {
        'path_id': f'/{org_name}/projects/shared', 
        'duplicate_check': True 
    }
    data = {"class_fqid":"com-snaplogic-pipeline_9","client_id":"x149","property_map":{"error":{"error0":{"view_type":{"value":"document"},"label":{"value":"error0"}},"error1":{"view_type":{"value":"binary"},"label":{"value":"error1"}},"error_behavior":{"value":"none"}},"info":{"label":{"value":name},"author":{"value":"admin@snaplogic.com"},"pipeline_doc_uri":{"value":None},"notes":{"value":None},"purpose":{"value":None}},"settings":{"error_pipeline":{"value":None,"expression":False},"error_param_table":{"value":[]},"param_table":{"value":[]},"imports":{"value":[]}},"input":{},"output":{}},"snap_map":{},"link_map":{},"render_map":{"scale_ratio":1,"pan_x_num":0,"pan_y_num":0,"detail_map":{}},"link_serial":100}
    response = requests.post(endpoint, headers=headers, params=params, data=json.dumps(data))
    # print(response.json())
    return response.json()["response_map"]["snode_id"]

def update_pipeline(org_id: str, name: str, snode_id: str):
    endpoint = f'{host}/api/2/{org_id}/rest/pipeline/update/{snode_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    params = { 'duplicate_check': True }
    data = {"update_map":{"create":{"snap":{"x234":{"class_fqid":"com-snaplogic-snaps-transform-jsongenerator_2-main14627","class_id":"com-snaplogic-snaps-transform-jsongenerator","class_version":2,"instance_fqid":"x234_1","instance_version":1,"property_map":{"info":{"label":{"value":"JSON Generator"}},"output":{"output0":{"view_type":{"value":"document"},"label":{"value":"output0"}}},"view_serial":100,"error":{"error0":{"view_type":{"value":"document"},"label":{"value":"error0"}},"error_behavior":{"value":"fail"}},"settings":{"execution_mode":{"value":"Validate & Execute"},"editable_content":{"value":"## Enter your JSON-encoded data in this space.  Note that this text is\n## treated as an Apache Velocity template, so you can substitute values\n## from input documents or the pipeline parameters.  See the following\n## URL for more information about Velocity:\n##   https://velocity.apache.org/engine/devel/user-guide.html\n\n[\n    {\n##        \"msg\" : \"Hello, World\", \"num\" : 1\n    }\n]\n\n\n## Tips:\n##  * The sample data above will generate a single empty document, uncomment\n##    the line in the middle to include the sample fields.  Adding more\n##    objects to the root array will cause the snap to generate more\n##    than one document.\n##  * Pipeline parameters can be referenced by prefixing the parameter\n##    name with an underscore, like so:\n##      ${_pipelineParamName}\n##  * If you add an input view to the snap, this template will be\n##    evaluated for each input document.\n##  * Fields in the input documents can be referenced by prefixing them\n##    with a dollar-sign ($), like so:\n##      $parent.child[0].value\n##  * Any referenced document values and pipeline parameters will\n##    automatically be JSON-encoded when they are inserted into the final\n##    JSON document.  You should not have to worry about escaping values\n##    yourself.\n##  * If you are having troubles getting a template to produce valid JSON,\n##    you can add an error view to the snap to get a document that\n##    contains the output of the template evaluation.\n"},"arrayElementsAsDocuments":{"value":True}}},"client_id":"x234"}},"link":{}},"update":{"snap":{},"link":{},"render_map":{"pan_x_num":0,"scale_ratio":1,"detail_map":{"x234":{"grid_x_int":2,"grid_y_int":1,"rot_int":0,"recommendation_id":None,"source":"snap catagory","index":None,"rot_tail_int":0,"output":{}}},"pan_y_num":0},"pipeline":{"info":{"notes":{"value":None},"label":{"value":name},"purpose":{"value":None},"pipeline_doc_uri":{"value":None},"author":{"value":"admin@snaplogic.com"}},"error":{"error_behavior":{"value":"none"}},"settings":{"imports":{"value":[]},"error_param_table":{"value":[]},"param_table":{"value":[]},"error_pipeline":{"expression":False,"value":None}},"instance_version":1,"input":{},"output":{"x234_output0":{"view_type":{"value":"document"},"label":{"value":"JSON Generator - output0"}}}}},"delete":{"snap":[],"link":[]},"link_serial":100}} 
    response = requests.post(endpoint, headers=headers, params=params, data=json.dumps(data))
    print('update {} {}'.format(name, response.json()))

def create_runtime(snode_id: str, org_name: str):
    endpoint = f'{host}/api/1/rest/pipeline/prepare/{snode_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    runtime_path_id = 'oregon/rt/orgplex/dev' if org_name == 'oregon' else 'singapore/rt/sgpplex/dev'
    runtime_label = 'orgplex' if org_name == 'oregon' else 'sgpplex'
    data = { "runtime_path_id": runtime_path_id, "runtime_label": runtime_label, "do_start": True, "async": True, "priority": 10 }
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    # print(response.json())

def login(username: str, password: str):
    path = '/api/1/rest/asset/session'
    params = {"caller": username}
    r = requests.get(host + path, params=params, auth=(username,password))
    return 'SLToken ' + r.json()["response_map"]["token"]

def get_orgsnid(username: str, org_name: str):
    path = '/api/1/rest/asset/user/{}'.format(username)
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    r = requests.get(host + path, headers=headers)
    data = r.json()
    org_snodes = data["response_map"]["org_snodes"]
    # print('get org  id', data)
    for snode in org_snodes:
        if org_snodes[snode]["name"] == org_name: return snode

username = 'admin@snaplogic.com'
password = 'Ephemeral$123'
host = sys.argv[1]

token = login(username, password)
sgp_org_name = 'singapore'
org_org_name = 'oregon'
sgp_org_id = get_orgsnid(username, sgp_org_name)
org_org_id = get_orgsnid(username, org_org_name)

# print(token)

# create pipline runtime
n = 5
for i in range(1,n+1):
    sgp_pipeline_name = f'sgp {i}'
    sgp_pipeline_id = create_pipeline(sgp_org_id, sgp_pipeline_name, sgp_org_name)
    update_pipeline(sgp_org_id, sgp_pipeline_name, sgp_pipeline_id)
    create_runtime(sgp_pipeline_id, sgp_org_name)

    org_pipeline_name = f'org {i}'
    org_pipeline_id = create_pipeline(org_org_id, org_pipeline_name, org_org_name)
    update_pipeline(org_org_id, org_pipeline_name, org_pipeline_id)
    create_runtime(org_pipeline_id, org_org_name)

# add region
mongo_host = sys.argv[2]

client = MongoClient(host=mongo_host, port=27017)
slserver_db = client["slserver"]
pipeline_rt = slserver_db["pm.pipeline_rt"]
pipeline_rt.update_many({"org_snode_id": sgp_org_id}, {"$set": {"region": "singapore"}})
pipeline_rt.update_many({"org_snode_id": org_org_id}, {"$set": {"region": "oregon"}})