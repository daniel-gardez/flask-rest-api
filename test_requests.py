from requests import get, post
import json

remote_url = 'https://flask-rest-api-l450.onrender.com'
port = '5000'
local_url = f'http://127.0.0.1:{port}'

base_url = f'{remote_url}'

store_json = {
    "items": [
        {
            "name": "Chair",
            "price": 15.5
        }
    ],
    "name": "Johnny Flowerson",
    "tags": ["Porn", "More Porn"]
}

user_post = post(f'{base_url}/register', json={"username": "Pepe", "password": "Jarl"})
print(get(f'{base_url}/user/1').content)
user_post = post(f'{base_url}/login', json={"username": "Pepe", "password": "Jarl"})
access_token = user_post.json()["access_token"]

post_result = post(f'{base_url}/store', json={"name": "John Flowerson"})
print(get(f'{base_url}/store').content)

post(f'{base_url}/store/1/tag', json={"name": "Porn"})
print(get(f'{base_url}/store/1/tag').content)

# Items
post_result = post(f'{base_url}/item', json={"name": "Table", "price": 6.99, "store_id": 1},
                   headers={"Authorization": f"Bearer {access_token}"})
get_result = get(f'{base_url}/item', headers={"Authorization": f"Bearer {access_token}"})

#Logout
logout = post(f'{base_url}/logout', headers={"Authorization": f"Bearer {access_token}"})
