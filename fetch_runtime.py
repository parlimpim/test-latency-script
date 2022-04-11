import requests
import json
import time
import numpy as np
import pandas as pd
import sys

def create_pipeline(host: str, org_id: str, token: str, name: str):
    endpoint = f'{host}/api/2/{org_id}/rest/pipeline/create'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    params = {
        'path_id': '/globalarch/projects/shared', 
        'duplicate_check': True 
    }
    data = {"class_fqid":"com-snaplogic-pipeline_9","client_id":"x163","property_map":{"error":{"error0":{"view_type":{"value":"document"},"label":{"value":"error0"}},"error1":{"view_type":{"value":"binary"},"label":{"value":"error1"}},"error_behavior":{"value":"none"}},"info":{"label":{"value":name},"author":{"value":"admin@snaplogic.com"},"pipeline_doc_uri":{"value":None},"notes":{"value":None},"purpose":{"value":None}},"settings":{"suspendable":{"value":False},"test_pipeline":{"value":False},"error_pipeline":{"value":None,"expression":False},"error_param_table":{"value":[]},"param_table":{"value":[]},"imports":{"value":[]}},"input":{},"output":{}},"snap_map":{},"link_map":{},"render_map":{"scale_ratio":1,"pan_x_num":0,"pan_y_num":0,"default_snaplex":"6213a53477bdf753fcd49b37","detail_map":{}},"link_serial":100}
    response = requests.post(endpoint, headers=headers, params=params, data=json.dumps(data))
    return response.json()["response_map"]["snode_id"]

def update_pipeline(host: str, org_id: str, token: str, name: str, snode_id: str):
    endpoint = f'{host}/api/2/{org_id}/rest/pipeline/update/{snode_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    params = { 'duplicate_check': True }
    data = {"update_map":{"create":{"snap":{"x164":{"class_fqid":"com-snaplogic-snaps-rest-get_2-main14627","class_id":"com-snaplogic-snaps-rest-get","class_version":2,"instance_fqid":"x164_1","instance_version":1,"property_map":{"info":{"notes":{},"label":{"value":"REST Get"}},"view_serial":100,"account":{"account_ref":{"value":{}}},"input":{"input0":{"label":{"value":"input0"},"view_type":{"value":"document"}}},"settings":{"retryInterval":{"value":3},"trustAllCerts":{"value":False},"execution_mode":{"value":"Validate & Execute"},"retry":{"value":5},"hasNext":{"expression":True,"value": None},"serviceUrl":{"expression":False,"value":"https://www.google.com"},"processArray":{"value":False},"retryPolicy":{"value":"Connection errors"},"showAllHeaders":{"value":False},"paginationInterval":{"value":0},"executeDuringPreview":{"value":True},"normalizeUri":{"value":True},"header":{"value":[]},"responseEntityType":{"value":"DEFAULT"},"followRedirects":{"value":True},"timeout":{"value":900},"connTimeout":{"value":30},"nextUrl":{"expression":True,"value":None},"queryParams":{"value":[]},"rawData":{"value":False}},"error":{"error0":{"label":{"value":"error0"},"view_type":{"value":"document"}},"error_behavior":{"value":"fail"}},"output":{"output0":{"label":{"value":"output0"},"view_type":{"value":"document"}}}},"class_build_tag":"main14627","client_id":"x164"},"x165":{"class_fqid":"com-snaplogic-snaps-transform-datatransform_4-main14627","class_id":"com-snaplogic-snaps-transform-datatransform","class_version":4,"instance_fqid":"x165_1","instance_version":9,"property_map":{"info":{"notes":{},"label":{"value":"Mapper"}},"view_serial":100,"input":{"input0":{"view_type":{"value":"document"},"label":{"value":"input0"}}},"settings":{"NoneSafeAccess":{"value":False},"passThrough":{"value":False},"execution_mode":{"value":"Validate & Execute"},"transformations":{"value":{"mappingTable":{"value":[{"expression":{"expression":True,"value":"$headers.date"},"targetPath":{"value":"$date"}},{"expression":{"expression":True,"value":"$headers.server"},"targetPath":{"value":"$server"}}]},"mappingRoot":{"value":"$"}}}},"error":{"error0":{"view_type":{"value":"document"},"label":{"value":"error0"}},"error_behavior":{"value":"fail"}},"output":{"output0":{"view_type":{"value":"document"},"label":{"value":"output0"}}}},"class_build_tag":"main14627","client_id":"x165"},"x166":{"class_fqid":"com-snaplogic-snaps-transform-csvformatter_3-main14627","class_id":"com-snaplogic-snaps-transform-csvformatter","class_version":3,"instance_fqid":"x166_1","instance_version":1,"property_map":{"info":{"label":{"value":"CSV Formatter"}},"view_serial":100,"input":{"input0":{"label":{"value":"input0"},"view_type":{"value":"document"}}},"settings":{"execution_mode":{"value":"Validate & Execute"},"escapeChar":{"value":"\\"},"quoteMode":{"value":"ALL"},"quoteCharacter":{"value":"\""},"writeHeader":{"value":True},"charset":{"value":"UTF-8"},"ignoreEmptyStream":{"value":False},"writeBOM":{"value":False},"delimiter":{"value":","},"errorPolicy":{"value":"Default"},"newlineCharacter":{"value":"LF"},"useDefinedHeader":{"value":False},"outputHeader":{"value":[{"expression":{"expression":True,"value":""}}]}},"error":{"error0":{"label":{"value":"error0"},"view_type":{"value":"document"}},"error_behavior":{"value":"fail"}},"output":{"output0":{"label":{"value":"output0"},"view_type":{"value":"binary"}}}},"class_build_tag":"main14627","client_id":"x166"},"x167":{"class_fqid":"com-snaplogic-snaps-binary-write_3-main14627","class_id":"com-snaplogic-snaps-binary-write","class_version":3,"instance_fqid":"x167_1","instance_version":1,"property_map":{"info":{"notes":{},"label":{"value":"File Writer"}},"view_serial":100,"account":{"account_ref":{"value":{}}},"settings":{"retryInterval":{"expression":False,"value":1},"retries":{"expression":False,"value":0},"execution_mode":{"value":"Execute only"},"flushIntervalKb":{"value":-1},"writeHeader":{"value":False},"cannedAcls":{"value":"Private"},"createDir":{"value":False},"executable_during_suggest":{"value":False},"filename":{"expression":False,"value":"google_header.csv"},"writeEmptyFile":{"value":False},"UserPermissionsKey":{"value":[]},"advancedProperties":{"value":[]},"validate":{"value":False},"fileAction":{"value":"OVERWRITE"}},"output":{},"error":{"error0":{"label":{"value":"error0"},"view_type":{"value":"document"}},"error_behavior":{"value":"fail"}},"input":{"input0":{"label":{"value":"input0"},"view_type":{"value":"binary"}}}},"class_build_tag":"main14627","client_id":"x167"}},"link":{"link100":{"dst_id":"x167","dst_view_id":"input0","src_id":"x166","src_view_id":"output0"},"link101":{"dst_id":"x165","dst_view_id":"input0","src_id":"x164","src_view_id":"output0"},"link102":{"dst_id":"x166","dst_view_id":"input0","src_id":"x165","src_view_id":"output0"}}},"update":{"snap":{},"link":{},"render_map":{"pan_x_num":0,"default_snaplex":"6213a53477bdf753fcd49b37","scale_ratio":1,"detail_map":{"x164":{"grid_x_int":4,"grid_y_int":2,"rot_int":0,"recommendation_id":None,"source":"","index":None,"rot_tail_int":0,"output":{},"input":{}},"x165":{"grid_x_int":5,"grid_y_int":2,"rot_int":0,"recommendation_id":None,"source":"","index":None,"rot_tail_int":0,"output":{},"input":{}},"x166":{"grid_x_int":6,"grid_y_int":2,"rot_int":0,"recommendation_id":None,"source":"","index":None,"rot_tail_int":0,"output":{},"input":{}},"x167":{"grid_x_int":7,"grid_y_int":2,"rot_int":0,"recommendation_id":None,"source":"","index":None,"rot_tail_int":0,"output":{},"input":{}}},"pan_y_num":0},"pipeline":{"info":{"notes":{"value":None},"label":{"value":name},"purpose":{"value":None},"pipeline_doc_uri":{"value":None},"author":{"value":"admin@snaplogic.com"}},"error":{"error_behavior":{"value":"none"}},"settings":{"param_table":{"value":[]},"suspendable":{"value":False},"test_pipeline":{"value":False},"imports":{"value":[]},"error_param_table":{"value":[]},"error_pipeline":{"expression":False,"value":None}},"instance_version":1,"input":{"x164_input0":{"label":{"value":"REST Get - input0"},"view_type":{"value":"document"}}},"output":{}}},"delete":{"snap":[],"link":[]},"link_serial":103}}
    response = requests.post(endpoint, headers=headers, params=params, data=json.dumps(data))

def create_runtime(host: str, token: str, snode_id: str):
    endpoint = f'{host}/api/1/rest/pipeline/prepare/{snode_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    data = { "runtime_path_id": "globalarch/rt/garchplex/dev", "runtime_label": "garchplex", "do_start": True, "async": True, "priority": 10 }
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))
    print(response.json())

def fetch_runtime(host=None, org_id=None, token=None):
    endpoint = f'{host}/api/2/{org_id}/rest/pm/runtime'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    data = {
        "state": "Completed,Stopped,Failed",
        "offset": 0,
        "limit": 0,
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

def fetch_runtime_globalarch(host=None, org_id=None, token=None):
    endpoint = f'{host}/api/2/{org_id}/rest/pm/runtime/globalarch'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    data = {
        "state": "Completed,Stopped,Failed",
        "offset": 0,
        "limit": 0,
        "is_globalarch": True,
    }
    response = requests.post(endpoint, headers=headers, data=json.dumps(data))

def login(host:str, username: str, password: str):
    path = '/api/1/rest/asset/session'
    params = {"caller": username}
    r = requests.get(host + path, params=params, auth=(username,password))
    return 'SLToken ' + r.json()["response_map"]["token"]

def get_orgsnid(host: str, username: str, token: str, org_name: str):
    path = '/api/1/rest/asset/user/{}'.format(username)
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json; charset=UTF-8',
    }
    r = requests.get(host + path, headers=headers)
    data = r.json()
    org_snodes = data["response_map"]["org_snodes"]
    for snode in org_snodes:
        if org_snodes[snode]["name"] == org_name: return snode

def evaluate(func, **kwargs):
    for i in range(N):
        result = []
        result.append(kwargs["backend_server_location"])
        result.append(kwargs["organization_data"])
        start = time.perf_counter()
        func(kwargs["host"], kwargs["org_id"], kwargs["token"])
        # milliseconds
        result.append(time.perf_counter() - start)
        data.append(result)   

def get_status(host: str):
    endpoint = f'{host}/status'
    response = requests.get(endpoint)
    print(response.json())

N = 10

username = 'admin@snaplogic.com'
password = 'Ephemeral$123'
org_host = sys.argv[1]
sgp_host = sys.argv[2]
org_org_name = 'oregon'
sgp_org_name = 'singapore'
token = login(org_host, username, password)
org_org_id = get_orgsnid(org_host, username, token, org_org_name)
sgp_org_id = get_orgsnid(org_host, username, token, sgp_org_name)
data = []
columns = ['endpoint','backend server location', 'organization data', 'time (secs)']

# oregon
print('oregon')
token = login(org_host, username, password)
print(evaluate(fetch_runtime, host=org_host, org_id=sgp_org_id, token=token, backend_server_location=org_org_name, organization_data=sgp_org_name, endpoint='/runtime'))
print(evaluate(fetch_runtime, host=org_host, org_id=org_org_id, token=token, backend_server_location=org_org_name, organization_data=org_org_name, endpoint='/runtime'))
print(evaluate(fetch_runtime_globalarch, host=org_host, org_id=sgp_org_id, token=token, backend_server_location=org_org_name, organization_data=sgp_org_name, endpoint='/runtime/globalarch'))
print(evaluate(fetch_runtime_globalarch, host=org_host, org_id=org_org_id, token=token, backend_server_location=org_org_name, organization_data=org_org_name, endpoint='/runtime/globalarch'))

# singapore
print('singapore')
token = login(sgp_host, username, password)
print(evaluate(fetch_runtime, host=sgp_host, org_id=sgp_org_id, token=token, backend_server_location=sgp_org_name, organization_data=sgp_org_name, endpoint='/runtime'))
print(evaluate(fetch_runtime, host=sgp_host, org_id=org_org_id, token=token, backend_server_location=sgp_org_name, organization_data=org_org_name, endpoint='/runtime'))
print(evaluate(fetch_runtime_globalarch, host=sgp_host, org_id=sgp_org_id, token=token, backend_server_location=sgp_org_name, organization_data=sgp_org_name, endpoint='/runtime/globalarch'))
print(evaluate(fetch_runtime_globalarch, host=sgp_host, org_id=org_org_id, token=token, backend_server_location=sgp_org_name, organization_data=org_org_name, endpoint='/runtime/globalarch'))

df = pd.DataFrame(data=data, columns=columns)
df.to_csv('result.csv')
