import requests

"""
Note: this python script shall test the behaviour of my rest api by sending mock HTTP requests to restful api
"""
# define test arguments
data = [{"likes": 12321, "name": "hello", "views": 32400000},
        {"likes": 50, "name": "jack", "views": 10000000000},
        {"likes": 500000, "name": "Step Sister Fantasy", "views": 10000000000},
        {"likes": 500000, "name": "Riley Ried", "views": 10000000000}]

# define base api url and respective resource end points
BASE_URL = "http://127.0.0.1:5000/"
name_hello = "jack"
end_point_hello = f"hello/{name_hello}"
video_id = 1
end_point_video = f"video/{video_id}"

# send some requests
for i in range(0, len(data)):
    response = requests.put(f"{BASE_URL}video/{i}", data[i])
    print(response.json())

# # delete some items from our videos_dict
# response = requests.delete(f"{BASE_URL}video/{6}")
# print(response.json())
# response = requests.delete(f"{BASE_URL}video/{1}")
# print(response)

# try to retrieve some items from our data base
response = requests.get(f"{BASE_URL}video/{4}")
print(response.json())
input()
response = requests.patch(f"{BASE_URL}video/{1}", data={})
print(response.json())

# # define all HTTP requests here to evaluate functional correctness of api
# get_response = requests.get(f"{BASE_URL}{end_point_hello}")
# # post_response = requests.post(f"{BASE_URL}{end_point}")
#
# put_response_video = requests.put(f"{BASE_URL}{end_point_video}", test_args)
# get_response_video = requests.get(f"{BASE_URL}video/{2}")
#
# print(get_response.json())
# # print(post_response.json())
#
# print(put_response_video.json())
# print(get_response_video.json())
