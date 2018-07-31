import json
import uuid

from locust import HttpLocust, TaskSet, task

PW = "cr0j3odMGPqQ9ebL5adItKR0xO9Ezon1UvPqM6lu64bWCIQBzLpOaJDI0Y2VJ0do"
uname = "suHsr4eSQRSnVE"
headers = {'content-type': 'application/json'}

class MyTaskSet(TaskSet):




    def get_listRoles(self):
        result = self.client.get("/api/v1beta/roles", name="listRoles", auth=(uname, PW), headers=headers)
        print result.text
        self.userID = "0000000007D52564"

    def post_createRole(self):
        payload = {
            "name": "PerfTest-" + str(uuid.uuid4()),
            "description": "PerfTest - Manage users and content.",
            "filterPredicate": "!_sourceCategory=billing",
            "capabilities": [
                "viewCollectors","manageContent"
            ]
        }
        result = self.client.post("/api/v1beta/roles", data = json.dumps(payload), name="createRole", auth=(uname, PW),
                                  headers=headers)
        print result.text
        self.roleInfo = json.loads(result.text)
        self.roleID = self.roleInfo["id"]

    def get_getRole(self):
        result = self.client.get("/api/v1beta/roles/{0}".format(self.roleID), name="getRole", auth=(uname, PW),
                                 headers=headers)
        print result.text

    def put_updateRole(self):
        payload = {
                      "name": "PerfTest-Admin",
                      "description": "Manage users and content.",
                      "filterPredicate": "!_sourceCategory=billing",
                      "users": [
                        self.userID
                      ],
                      "capabilities": [
                         "viewCollectors","manageContent"
                      ]
                    }
        result = self.client.put("/api/v1beta/roles/{0}".format(self.roleID), data=json.dumps(payload),
                                 name="updateRole", auth=(uname, PW), headers=headers)
        print result.text

    def delete_deleteRole(self):
        result = self.client.delete("/api/v1beta/roles/{0}".format(self.roleID), name="deleteRole", auth=(uname, PW),
                                    headers=headers)
        print result.text

    # TODO: needs to be completed
    def put_assignRoleToUser(self):
        result = self.client.put("/api/v1beta/roles/{0}/users/{1}".format(self.roleID, self.userID),
                                 name="assignRoleToUser", auth=(uname, PW), headers=headers)
        print result.text

    # TODO: needs to be completed
    def delete_removeRoleFromUser(self):
        result = self.client.delete("/api/v1beta/roles/{0}/users/{1}".format(self.roleID, self.userID),
                                    name="removeRoleFromUser", auth=(uname, PW), headers=headers)
        print result.text

    @task
    def userScenario(self):
        self.get_listRoles()
        self.post_createRole()
        self.get_getRole()
        self.put_updateRole()
        self.put_assignRoleToUser()
        self.delete_removeRoleFromUser()
        self.delete_deleteRole()


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 3000
