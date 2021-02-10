import requests

"""
Note: this python script shall test the behaviour of my rest api by sending mock HTTP requests to restful api
"""

# define base api url and respective resource end points
name = "jack"
BASE_URL = "http://127.0.0.1:5000/"
end_point = f"hello/{name}"

# define all HTTP requests here to evaluate functional correctness of api
get_response = requests.get(f"{BASE_URL}{end_point}")
# post_response = requests.post(f"{BASE_URL}{end_point}")
print(get_response.json())
# print(post_response.json())

