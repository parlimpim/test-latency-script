from tokenize import String
import requests
import json
from timeit import default_timer as timer
import numpy as np

test = {
    "oregon": {
        "host": "http://44.227.132.127",
        "username": 'admin@snaplogic.com',
        "password": 'Ephemeral$123',
    },

    # "singapore": {
    #     "host": "",
    #     "username": 'admin@snaplogic.com',
    #     "password": 'Ephemeral$123',
    # },

    # "snaplogic": {
    #     "host": "https://elastic.snaplogic.com/",
    #     "username": 'tanyakorn.wp@gmail.com',
    #     "password": 'Pim300842!',
    # }
}

N = 2

# def validate_response(r):
#     if r.status_code != 200:
#         raise Exception("Invalid Status Code")

# def evaluate(func):
#     latency = np.zeros(N)
#     for i in range(N):
#         start = timer()
#         func()
#         # milliseconds
#         latency[i] = timer() - start
#     latency = latency * 1000

#     P50 = np.percentile(latency, 50)
#     P90 = np.percentile(latency, 90)
#     P99 = np.percentile(latency, 99)

#     return round(P50, 2), round(P90, 2), round(P99, 2)

# def login(username, password):
#     path = '/api/1/rest/asset/session'
#     params = {"caller": username}
#     r = requests.get(host + path, params=params, auth=(username,password))
#     return 'SLToken ' + r.json()["response_map"]["token"]

# def get_orgsnid(username, headers):
#     path = '/api/1/rest/asset/user/{}'.format(username)
#     r = requests.get(host + path, headers=headers)
#     data = r.json()
#     org_snodes = data["response_map"]["org_snodes"]
#     for snode in org_snodes:
#         if org_snodes[snode]["name"] == "snaplogic": return snode

# def fetch_runtime(org_snid, headers):
#     path = '/api/2/{}/rest/pm/runtime'.format(org_snid)
#     body = {
#         "state": "Completed,Stopped,Failed",
#         "offset": 0,
#         "limit": 0,
#     }
#     r = requests.post(host + path, data=json.dumps(body), headers=headers)
#     validate_response(r)
    
# def create_runtime(headers):
#     path = '/api/1/rest/pipeline/prepare/621110ab230251fcfc11c548'
#     body = {"runtime_path_id": "snaplogic/rt/cloud/dev","runtime_label": "cloud","do_start": True,"async": True,"priority": 10}
#     r = requests.post(host + path, data=json.dumps(body), headers=headers)
#     print(r.text)

# print("fetch runetime: ", evaluate(fetch_runtime))
# print("create runetime: ", evaluate(create_runtime))

# create_runtime()

# def main():
#     for key in test:
#         print(key)
#         token = login(username,password)
#         headers = {'Authorization': token}
#         org_snid = get_orgsnid(username, headers)
#         print("fetch runetime: ", evaluate(fetch_runtime(org_snid, headers)))
# main()

class RequestBuilder:
    def __init__(self, host: str, endpoint: str):
        self.path = host + endpoint
    
    def params(self, key, value):
        if self.params == None:
            self.params = dict()
        self.params[key] = value

    def body(self, body):
        self.body = json.dumps(body)

    def headers(self, headers):
        self.headers = headers
    
    def get(self, auth=None):
        resp = requests.get(self.path, params=self.params, headers=self.headers, auth=auth)

class Host:
    def __init__(self, host: str):
        self.host = host

    def headers(self):
        if self.token == None:
            raise Exception("Token not found")
        return {
            'Content-Type': 'application/json; charset=UTF-8',
            'Authorization': self.token,
        }

    def login(self, username: str, password: str):
        self.username = username
        self.password = password

        endpoint = '/api/1/rest/asset/session'
        self.token = 'SLToken ' + self.get(endpoint, params={"caller": username}, auth=(username, password))["token"]

    def get(self, endpoint: str, params=None, auth=None, headers=None):
        resp = requests.get(self.host + endpoint, params=params, auth=auth, headers=headers)
        return resp.json()["response_map"]

    def post(self, endpoint: str, body=None, headers=None):
        resp = requests.post(self.host + endpoint, data=json.dumps(body), headers=headers)
        return resp.json()["response_map"]

class RuntimeCtrl:
    def __init__(self, host: Host):
        self.host = host

    def create(self, pipeline_id: str):
        endpoint = f'/api/1/rest/pipeline/prepare/{pipeline_id}'

        body = {
            "runtime_path_id": "snaplogic/rt/cloud/dev",
            "runtime_label": "cloud",
            "do_start": True,
            "async": True,
            "priority": 10,
        }

        resp = self.host.post(endpoint, body)

class script:
    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.token = self.login()
        self.headers = {'Content-Type': 'application/json; charset=UTF-8','Authorization': self.token}
        self.oregon_org_snid = self.get_orgsnid('oregon')
        self.singapore_org_snid = self.get_orgsnid('singapore')
    
    def login(self):
        path = '/api/1/rest/asset/session'
        params = {"caller": self.username}
        r = requests.get(self.host + path, params=params, auth=(self.username, self.password))
        print('header',r.url)
        return 'SLToken ' + r.json()["response_map"]["token"]

    def get_orgsnid(self, org_name: str):
        path = '/api/1/rest/asset/user/{}'.format(self.username)
        r = requests.get(self.host + path, headers=self.headers)
        data = r.json()
        org_snodes = data["response_map"]["org_snodes"]
        for snode in org_snodes:
            if org_snodes[snode]["name"] == org_name: return org_snodes[snode]["org_snode_id"]

    def get_snodeid_list(self, org):
        path = '/api/1/rest/asset/tree/{}/shared'.format(org["name"])
        r = requests.get(self.host + path, headers=self.headers)
        self.validate_response(r)
        data = r.json()
        entries = data["response_map"]["entries"]
        return [{'name': each['name'], 'snode_id':each['snode_id']} for each in entries]

    def validate_response(self,r):
        if r.status_code != 200:
            errors = [e["message"] for e in r.json()["response_map"]["error_list"]]
            raise Exception("Invalid Status Code", r.status_code, errors)

    def evaluate(self, func, payload):
        latency = np.zeros(N)
        for i in range(N):
            start = timer()
            func(payload)
            # milliseconds
            latency[i] = timer() - start
        latency = latency * 1000

        P50 = np.percentile(latency, 50)
        P90 = np.percentile(latency, 90)
        P99 = np.percentile(latency, 99)

        return round(P50, 2), round(P90, 2), round(P99, 2)

    def fetch_runtime(self, org):
        path = '/api/2/{}/rest/pm/runtime'.format(org["org_snode_id"])
        body = {
            "state": "Completed,Stopped,Failed",
            "offset": 0,
            "limit": 0,
        }
        r = requests.post(self.host + path, data=json.dumps(body), headers=self.headers)
        self.validate_response(r)
    
    def create_runtime(self):
        path = '/api/1/rest/pipeline/prepare/6212269fc398d9cd537bbb23'
        body = {"runtime_path_id": "snaplogic/rt/cloud/dev","runtime_label": "cloud","do_start": True,"async": True,"priority": 10}
        r = requests.post(self.host + path, data=json.dumps(body), headers=self.headers)
        print(r.text)

    def main(self):
        ####### fetch runtime #######
        # print('fetch runtime')
        # for org in self.org_snid:
        #     print('org name: {}'.format(org["name"]))
        #     print(self.evaluate(self.fetch_runtime, org))

        ####### create runtime #######
        print('create runtime')
        for org in self.org_snid:
            print('org name: {}'.format(org["name"]))
            print(self.get_snodeid_list(org))
        # self.create_runtime()

for region in test:
    value = test[region]
    host = Host(value["host"])
    host.login(value["username"], value["password"])
    # print(key)
    run = script(value["username"], value["password"], value["host"])
    # run.main()
