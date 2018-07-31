PW = "cr0j3odMGPqQ9ebL5adItKR0xO9Ezon1UvPqM6lu64bWCIQBzLpOaJDI0Y2VJ0do"
uname = "suHsr4eSQRSnVE"
headers = {'content-type': 'application/json'}
url = "https://nite-api.sumologic.net"

import requests
import json
roleout = {}
userout = {}

def get_listRoles():
    global roleout
    result = requests.get(url+"/api/v1beta/roles", auth=(uname, PW), headers=headers)
    # print result.text
    roleout = json.loads(result.text)
    print roleout['data']

def get_listusers():
    global userout
    result = requests.get(url+"/api/v1beta/users",  auth=(uname, PW), headers=headers)
    # print result.text
    userout = json.loads(result.text)
    print userout


def deleteRoles():
    rolelist = roleout['data']
    for roles in rolelist:
        if "PerfTest" in roles['name']:
            print roles['id']
            result= requests.delete(url+"/api/v1beta/roles/{0}".format(roles['id']), auth=(uname, PW),
                                        headers=headers)
            print(result.text)


def deleteUsers():
    userlist = userout['data']
    for users in userlist:
        if "Vivek" in users['firstName']:
            print users['id']
            result= requests.delete(url+"/api/v1beta/users/{0}".format(users['id']), auth=(uname, PW),
                                        headers=headers)
            print result
            print(result.text)

#
get_listRoles()
deleteRoles()
#
get_listusers()
deleteUsers()


