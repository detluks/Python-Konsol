import requests
for i in range(100):
    requests.post("http://10.74.64.249:8000", json={"setUser": True,"user":i, "password": i*20})