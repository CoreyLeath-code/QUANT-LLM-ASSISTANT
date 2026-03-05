from locust import HttpUser, task

class QuantUser(HttpUser):

    @task
    def query(self):
        self.client.post("/query", json={"question":"Explain market volatility"})
