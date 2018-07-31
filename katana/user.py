import json
import uuid

from locust import HttpLocust, TaskSet, task

PW = "cr0j3odMGPqQ9ebL5adItKR0xO9Ezon1UvPqM6lu64bWCIQBzLpOaJDI0Y2VJ0do"
uname = "suHsr4eSQRSnVE"

headers = {'content-type': 'application/json'}


class MyTaskSet(TaskSet):
    def get_listusers(self):
        result = self.client.get("/api/v1beta/users", name="listusers", auth=(uname, PW), headers=headers)
        print result.text

    def listusers(self):
        global userout
        result = self.client.get("/api/v1beta/users",  auth=(uname, PW), headers=headers)
        # print result.text
        self.userout = json.loads(result.text)
        # print userout

    def post_createuser(self):
        payload = {
            "firstName": "Vivek",
            "lastName": "Gupta",
            "email": "PerfTest" + str(uuid.uuid4()) + "@demo.com",
            "roleIds": [
                "0000000007B938DE"
            ]
        }
        result = self.client.post("/api/v1beta/users", data=json.dumps(payload), name="createuser", auth=(uname, PW),
                                  headers=headers)
        print result.text

        self.userInfo = json.loads(result.text)
        self.userID = self.userInfo["id"]

    def get_getuser(self):
        result = self.client.get("/api/v1beta/users/{0}".format(self.userID), name="getuser", auth=(uname, PW),
                                 headers=headers)
        print result.text

    def put_updateuser(self):
        payload = {
            "firstName": "Vivek1",
            "lastName": "Testgupta",
            "isActive": "true",
            "roleIds": [
                "0000000007B938DE"
            ]
        }
        result = self.client.put("/api/v1beta/users/{0}".format(self.userID), name="updateuser",
                                 data=json.dumps(payload), auth=(uname, PW), headers=headers)
        print result.text

    def delete_deleteuser(self):
        result = self.client.delete("/api/v1beta/users/{0}".format(self.userID), name="deleteuser",
                                    auth=(uname, PW), headers=headers)
        print result.text

    def deleteUsers(self):
        userlist = self.userout['data']
        for users in userlist:
            if "Vivek" in users['firstName']:
                print users['id']
                result = self.client.delete("/api/v1beta/users/{0}".format(users['id']), auth=(uname, PW),
                                         headers=headers)
                print result
                print(result.text)

    def post_requestChangeEmail(self):
        payload = {
            "email": "vguptatest@demo.com"
        }
        result = self.client.post("/api/v1beta/users/{0}/email/requestChange".format(self.userID),
                                 data=json.dumps(payload),
                                 name="requestChangeEmail",
                                 auth=(uname, PW), headers=headers)
        print result.text

    def post_resetPassword(self):
        result = self.client.post("/api/v1beta/users/{0}/password/reset".format(self.userID),
                                 name="resetPassword",
                                 auth=(uname, PW), headers=headers)
        print result.text

    # @task
    # def userScenario(self):
    #     self.get_listusers()
    #     self.post_createuser()
    #     self.get_getuser()
    #     self.put_updateuser()
    #     self.post_requestChangeEmail()
    #     self.post_resetPassword()
    #     self.delete_deleteuser()

    @task
    def deleteUserScenario(self):
        self.listusers()
        self.deleteUsers()


class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 3000
