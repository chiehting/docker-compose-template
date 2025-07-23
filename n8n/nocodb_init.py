# python nocodb_init.py

import subprocess
import random
import json
import requests

NC_ADMIN_EMAIL = "admin@gmail.com"
NC_ADMIN_PASSWORD = "password"
NC_URL = 'http://localhost:8080'
N8N_URL = 'http://n8n:5678'
XC_AUTH = ""

def get_header():
    return {'Content-Type': 'application/json','xc-auth': XC_AUTH}
def post(path, data = {}):
    response = requests.post(NC_URL + path, headers=get_header(), data=json.dumps(data))
    return response.json(), response.status_code

def get(path, data = {}):
    response = requests.get(NC_URL + path, headers=get_header(), data=json.dumps(data))
    return response.json(), response.status_code

def delete(path):
    response = requests.delete(NC_URL + path, headers=get_header())
    return response.json(), response.status_code

getNocoDbJson = subprocess.run(["kubectl","get","pod","-l","app.kubernetes.io/instance=nocodb","-o","json"], capture_output=True, text=True).stdout
nocoDbJson = json.loads(getNocoDbJson)
nocoDbJsonEnv = nocoDbJson["items"][0]["spec"]["containers"][0]["env"]
for env in nocoDbJsonEnv:
    envName = env["name"]
    if envName == "NC_ADMIN_EMAIL":
        NC_ADMIN_EMAIL = env["value"]
    elif  envName == "NC_ADMIN_PASSWORD":
        NC_ADMIN_PASSWORD = env["value"]

def painc(name, code , log):
    print(name, ":\t", code)
    print(name,  ":\t", log)
    exit()

def signin():
    login_resp, code = post('/api/v1/auth/user/signin', data = {"email": NC_ADMIN_EMAIL,"password": NC_ADMIN_PASSWORD})
    if code != 200:
        painc('login_resp', code, login_resp['msg'])
    return login_resp["token"]

def api_token():
    api_token_name = 'n8n'
    get_api_token_resp, _ = get('/api/v1/tokens', data = {"limit": 0})
    if not any(token['description'] == api_token_name for token in get_api_token_resp["list"]):
        new_token, _ = post('/api/v1/tokens', data = {"description": api_token_name})
        get_api_token_resp = {"list": [new_token]}
    return get_api_token_resp

def base():
    base_name = 'Lndu'
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    get_base_resp, _ = get('/api/v1/db/meta/projects/')
    for base in get_base_resp["list"]:
        if base['title'] == base_name:
            return base
    new_base, _ = post('/api/v1/db/meta/projects/', data = {"title": base_name, "meta": "{\"iconColor\": \"" + color + "\"}"})
    return new_base


def get_job_schema_json():
    return [
        {"column_name":"device_id","title": "device_id","order":18,"uidt":"Number","dt": "bigint","pk":False},
        {"column_name":"lang","title": "lang","order":17,"uidt":"SingleLineText","dt": "TEXT","pk":False},
        {"column_name":"callback_url","title": "callback_url","order":16,"uidt":"SingleLineText","dt": "TEXT","pk":False},
        {"column_name":"device_timezone","title": "device_timezone","order":15,"uidt":"SingleLineText","dt": "TEXT","pk":False},
        {"column_name":"member_nickname","title":"member_nickname","order":14,"uidt":"SingleLineText","dt": "TEXT","pk":False},
        {"column_name":"final_output_path","title": "final_output_path","order":13,"uidt":"SingleLineText","dt": "TEXT","pk":False},
        {"column_name":"end_at","title":"end_at","order":12,"uidt":"DateTime","dt":"timestamp","pk":False,"meta":{"date_format":"YYYY-MM-DD","time_format":"HH:mm:ss.SSS","is12hrFormat":False}},
        {"column_name":"start_at","title":"start_at","order":11,"uidt":"DateTime","dt":"timestamp","pk":False,"meta":{"date_format":"YYYY-MM-DD","time_format":"HH:mm:ss.SSS","is12hrFormat":False}},
        {"column_name":"job_status","title": "job_status","order":10,"uidt":"SingleSelect","dt":"TEXT","pk":False,"cdf":"'pending'","dtx":"specificType","dtxp":"'pending','processing','completed','failed','cancelled'","colOptions":{"options":[{"title":"pending","color":"#cfdffe","order":1},{"title":"processing","color":"#d0f1fd","order":2},{"title":"completed","color":"#c2f5e8","order":3},{"title":"failed","color":"#ffdaf6","order":4},{"title":"cancelled","color":"#ffdce5","order":5}]}},
        {"column_name":"original_video_url","title":"original_video_url","order":9,"uidt":"JSON","dt": "json","pk":False,"cdf":"[]"},
        {"column_name":"member_id","title":"member_id","order":8,"uidt":"Number","dt": "bigint","pk":False},
        {"column_name":"uuid","title":"uuid","order":7,"uidt":"SingleLineText","dt":"TEXT","pk":False},
        {"column_name":"id","title":"Id","order":1,"uidt":"ID","dt":"int4","pk":True},
    ]

def get_task_schema_json():
    return [
        {"column_name":"end_at","title":"end_at","order":13,"uidt":"DateTime","dt":"timestamp","pk":False,"meta":{"date_format":"YYYY-MM-DD","time_format":"HH:mm:ss.SSS","is12hrFormat":False}},
        {"column_name":"start_at","title":"start_at","order":12,"uidt":"DateTime","dt":"timestamp","pk":False,"meta":{"date_format":"YYYY-MM-DD","time_format":"HH:mm:ss.SSS","is12hrFormat":False}},
        {"column_name":"status","title": "status","order":11,"uidt":"SingleSelect","dt": "TEXT","pk":False,"cdf":"'pending'","dtx":"specificType","dtxp":"'pending','processing','completed','failed','cancelled'","colOptions":{"options":[{"title":"pending","color":"#cfdffe","order":1},{"title":"processing","color":"#d0f1fd","order":2},{"title":"completed","color":"#c2f5e8","order":3},{"title":"failed","color":"#ffdaf6","order":4},{"title":"cancelled","color":"#ffdce5","order":5}]}},
        {"column_name":"data","title":"data","order":10,"uidt":"JSON","dt":"json","pk":False},
        {"column_name":"input","title":"input","order":9,"uidt":"JSON","dt":"json","pk":False},
        {"column_name":"type","title":"type","order":8,"uidt":"Number","dt":"bigint","pk":False},
        {"column_name":"job_id","title":"job_id","order":7,"uidt":"Number","dt":"bigint","pk":False},
        {"column_name":"id","title":"Id","order":1,"uidt":"ID","dt":"int4","pk":True},
    ]

def table(source_id, base_id, table_name = ""):
    if not source_id or not base_id or not table_name:
        painc('table', 503, 'miss peremeters')
    get_table_resp, _ = get(f"/api/v1/db/meta/projects/{base_id}/tables", data = {"includeM2M": False})
    for table in get_table_resp["list"]:
        if table['title'] == table_name:
            return table
    columns = []
    if table_name == "Job":
        columns = get_job_schema_json()
    elif table_name == "Task":
        columns = get_task_schema_json()
    data = {
        "table_name": table_name,
        "title": table_name,
        "is_hybrid": True,
        "columns": columns
    }

    new_table, _ = post(f"/api/v1/db/meta/projects/{base_id}/{source_id}/tables", data = data)
    return new_table

def job(action):
    webhoook_url = f"{N8N_URL}/webhook/1d986c2e-43e9-43b1-a422-dc4d20b6c8c6"
    if action == "insert":
        return {
            "title": "job_check","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": False,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}}
        }
    if action == "update":
        return {
            "title": "job_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [{"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "job_status"}]
        }


def video_analysis_1(action):
    webhoook_url = f"{N8N_URL}/webhook/56d5338b-2910-4099-9765-6bc433b404a5"
    if action == "insert":
        return {
            "title": "video_analysis(1)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "1","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "video_analysis(1)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "1","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }


def video_cutting_2(action):
    webhoook_url = f"{N8N_URL}/webhook/de60bbf1-6d0f-4811-a841-d6fe738c1ef2"
    if action == "insert":
        return {
            "title": "video_cutting(2)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "2","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "video_cutting(2)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "2","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }

def handle_head_photo_3(action):
    webhoook_url = f"{N8N_URL}/webhook/6a92922f-068c-4846-bc2e-6b997bf84b2f"
    if action == "insert":
        return {
            "title": "handle_head_photo(3)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "3","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "handle_head_photo(3)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": "http://n8n/webhook/6a92922f-068c-4846-bc2e-6b997bf84b2f"}},
            "filters": [
                {"comparison_op": "eq","value": "3","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }

def generate_head_video_4(action):
    webhoook_url = f"{N8N_URL}/webhook/a8f23873-071b-4f02-bd5a-cac73604d772"
    if action == "insert":
        return {
            "title": "generate_head_video(4)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "4","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "generate_head_video(4)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "4","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }

def handle_tail_video_5(action):
    webhoook_url = f"{N8N_URL}/webhook/9c3d82bf-1212-4dde-9e5e-f16eb6ce2684"
    if action == "insert":
        return {
            "title": "handle_tail_video(5)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "5","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "handle_tail_video(5)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "5","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }

def merge_video_6(action):
    webhoook_url = f"{N8N_URL}/webhook/a37ac451-e340-43bb-b1f7-371d391a0212"
    if action == "insert":
        return {
            "title": "merge_video(6)_create","event": "after","operation":"insert","eventOperation": "after insert","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "6","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }
    if action == "update":
        return {
            "title": "merge_video(6)_update","event": "after","operation":"update","eventOperation": "after update","active": True, "condition": True,
            "notification": {"type": "URL","payload": {"method": "POST","path": webhoook_url}},
            "filters": [
                {"comparison_op": "eq","value": "6","status": "create","logical_op": "and","fk_column_name": "type"},
                {"comparison_op": "eq","value": "pending","status": "create","logical_op": "and","fk_column_name": "status"},
            ]
        }

def webhook_filters(table_id, data):
    hook_list = {}
    columns_id = {}
    get_table_resp, _ = get(f"/api/v1/db/meta/tables/{table_id}")
    for column in get_table_resp['columns']:
        columns_id[column['column_name']] = column['id']

    hook_resp, _ = get(f"/api/v1/db/meta/tables/{table_id}/hooks", data)
    for hook in hook_resp['list']:
        hook_list[hook['title']] = hook

    for hook_data in data:
        if 'filters' in hook_data:
            hook_id = hook_list[hook_data['title']]['id']
            filters_list, _ = get(f"/api/v1/db/meta/hooks/{hook_id}/filters")
            for filter in filters_list['list']:
                delete(f"/api/v1/db/meta/filters/{filter['id']}")
            for filter in hook_data['filters']:
                filter_data = filter
                filter_data['fk_column_id'] = columns_id[filter['fk_column_name']]
                post(f"/api/v1/db/meta/hooks/{hook_id}/filters", filter_data)

def webhook(table_id, hook_data = []):
    hook_list = {}
    get_webhook_resp, _ = get(f"/api/v1/db/meta/tables/{table_id}/hooks")
    for hook in get_webhook_resp["list"]:
        hook_list[hook['title']] = hook
    for data in hook_data:
        if data['title'] in hook_list:
            hook_id = hook_list[data['title']]['id']
            delete(f"/api/v1/db/meta/hooks/{hook_id}")
        post(f"/api/v1/db/meta/tables/{table_id}/hooks", data)
    
    webhook_filters(table_id, hook_data)

if __name__ == "__main__":
    XC_AUTH = signin()

    get_api_token_resp = api_token()
    print("API Token:\t", get_api_token_resp['list'][0]['token'])

    base_resp = base()
    source_id = base_resp['sources'][0]['id']
    base_id = base_resp['sources'][0]['base_id']
    print("BASE ID:\t", base_id)
    jog_table_resp = table(source_id, base_id, "Job")
    print("TABLE Job ID:\t", jog_table_resp["id"])
    webhook(jog_table_resp["id"], [
        job(action = 'insert'),
        job(action ='update')
    ])

    task_table_resp = table(source_id, base_id, "Task")
    print("TABLE Task ID:\t", task_table_resp["id"])
    webhook(task_table_resp["id"], [
        video_analysis_1(action = 'insert'),
        video_analysis_1(action ='update'),
        video_cutting_2(action = 'insert'),
        video_cutting_2(action ='update'),
        handle_head_photo_3(action = 'insert'),
        handle_head_photo_3(action ='update'),
        generate_head_video_4(action = 'insert'),
        generate_head_video_4(action ='update'),
        handle_tail_video_5(action = 'insert'),
        handle_tail_video_5(action ='update'),
        merge_video_6(action = 'insert'),
        merge_video_6(action ='update')
    ])
