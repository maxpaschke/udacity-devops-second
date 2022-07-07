from locust import HttpUser, task

postdata = '{ \
    "CHAS": { \
        "0": 0 \
    }, \
    "RM": { \
        "0": 6.575 \
    }, \
    "TAX": { \
        "0": 296.0 \
    }, \
    "PTRATIO": { \
        "0": 15.3 \
    }, \
    "B": { \
        "0": 396.9 \
    }, \
    "LSTAT": { \
        "0": 4.98 \
    } \
}'


class HelloWorldUser(HttpUser):
    @task
    def getbaseurl(self):
        self.client.get("/")

    @task
    def dopreditction(self):
        self.client.post("/predict", json=postdata)
