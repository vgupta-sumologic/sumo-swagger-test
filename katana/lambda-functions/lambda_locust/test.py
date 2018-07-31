from locust import HttpLocust, TaskSet, task
import loga

loga.setup_graphite_communication()
PW = "qgIUedSlv9uAsJE79HHmXmbHrusoGz8dXvptp5PFdR0zf4sqh3Uv1dmelolYBGaf"
uname = "suXe2WZzZoASVs"

class MyTaskSet(TaskSet):

    
    @task
    def get_v2alpha_content_id(self):
        self.client.get("/api/v2alpha/content/{0}".format("undefined"), name="/v2alpha/content/{id}",auth=(uname, PW))

    @task
    def get_v1alpha_content_synchronize_id(self):
        self.client.get("/api/v1alpha/content/synchronize/{0}".format("undefined"), name="/v1alpha/content/synchronize/{id}",auth=(uname, PW))

    @task
    def get_v1alpha_dashboard_id(self):
        self.client.get("/api/v1alpha/dashboard/{0}".format("undefined"), name="/v1alpha/dashboard/{id}",auth=(uname, PW))

    @task
    def get_v1alpha_dashboard_id_variablesValues(self):
        self.client.get("/api/v1alpha/dashboard/{0}/variablesValues".format("undefined"), name="/v1alpha/dashboard/{id}/variablesValues",auth=(uname, PW))

    @task
    def get_v1alpha_dashboard_variables_id(self):
        self.client.get("/api/v1alpha/dashboard/variables/{0}".format("undefined"), name="/v1alpha/dashboard/variables/{id}",auth=(uname, PW))

    @task
    def get_v1alpha_dashboard_variables_id_values(self):
        self.client.get("/api/v1alpha/dashboard/variables/{0}/values".format("undefined"), name="/v1alpha/dashboard/variables/{id}/values",auth=(uname, PW))

    @task
    def get_v1alpha_extractionRules(self):
        self.client.get("/api/v1alpha/extractionRules", name="/v1alpha/extractionRules",auth=(uname, PW))

    @task
    def get_v1alpha_extractionRules_id(self):
        self.client.get("/api/v1alpha/extractionRules/{0}".format("undefined"), name="/v1alpha/extractionRules/{id}",auth=(uname, PW))

    @task
    def get_v1beta_roles(self):
        self.client.get("/api/v1beta/roles", name="/v1beta/roles",auth=(uname, PW))

    @task
    def get_v1beta_roles_id(self):
        self.client.get("/api/v1beta/roles/{0}".format("undefined"), name="/v1beta/roles/{id}",auth=(uname, PW))

    @task
    def get_v1beta_users(self):
        self.client.get("/api/v1beta/users", name="/v1beta/users",auth=(uname, PW))

    @task
    def get_v1beta_users_id(self):
        self.client.get("/api/v1beta/users/{0}".format("undefined"), name="/v1beta/users/{id}",auth=(uname, PW))

    @task
    def get_v1alpha_eventDetail(self):
        self.client.get("/api/v1alpha/eventDetail?event_ids={0}".format("undefined"), name="/v1alpha/eventDetail",auth=(uname, PW))

    @task
    def get_v1alpha_investigation_investigationId(self):
        self.client.get("/api/v1alpha/investigation/{0}".format("undefined"), name="/v1alpha/investigation/{investigationId}",auth=(uname, PW))

    @task
    def get_v1alpha_investigation(self):
        self.client.get("/api/v1alpha/investigation", name="/v1alpha/investigation",auth=(uname, PW))

    @task
    def get_v1alpha_investigationConfig(self):
        self.client.get("/api/v1alpha/investigationConfig", name="/v1alpha/investigationConfig",auth=(uname, PW))

    @task
    def get_v1alpha_investigationReport(self):
        self.client.get("/api/v1alpha/investigationReport?investigation_id={0}".format("undefined"), name="/v1alpha/investigationReport",auth=(uname, PW))

    @task
    def get_v1alpha_linkType(self):
        self.client.get("/api/v1alpha/linkType", name="/v1alpha/linkType",auth=(uname, PW))

    @task
    def get_v1alpha_logEntry(self):
        self.client.get("/api/v1alpha/logEntry?event_ids={0}".format("undefined"), name="/v1alpha/logEntry",auth=(uname, PW))

    @task
    def get_v1alpha_parseTime(self):
        self.client.get("/api/v1alpha/parseTime?time={0}".format("undefined"), name="/v1alpha/parseTime",auth=(uname, PW))

    @task
    def get_v1alpha_pivot_investigationPivotIdentifier(self):
        self.client.get("/api/v1alpha/pivot/{0}".format("undefined"), name="/v1alpha/pivot/{investigationPivotIdentifier}",auth=(uname, PW))

    @task
    def get_v1alpha_serverTime(self):
        self.client.get("/api/v1alpha/serverTime", name="/v1alpha/serverTime",auth=(uname, PW))

    @task
    def get_v1alpha_status(self):
        self.client.get("/api/v1alpha/status", name="/v1alpha/status",auth=(uname, PW))

    @task
    def get_v1alpha_referenceUrl(self):
        self.client.get("/api/v1alpha/referenceUrl", name="/v1alpha/referenceUrl",auth=(uname, PW))

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 1000
    max_wait = 3000

