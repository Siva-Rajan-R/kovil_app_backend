from locust import HttpUser, task, between

class MyTestUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def ping(self):
        self.client.get("/")
