from requests import get, post
import json
port = '5000'

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

user_post = post(f'http://127.0.0.1:{port}/register', json={"username": "Pepe", "password": "Jarl"})
print(get(f'http://127.0.0.1:{port}/user/1').content)
user_post = post(f'http://127.0.0.1:{port}/login', json={"username": "Pepe", "password": "Jarl"})
access_token = user_post.json()["access_token"]

post_result = post(f'http://127.0.0.1:{port}/store', json={"name": "John Flowerson"})
print(get(f'http://127.0.0.1:{port}/store').content)

post(f'http://127.0.0.1:{port}/store/1/tag', json={"name": "Porn"})
print(get(f'http://127.0.0.1:{port}/store/1/tag').content)

# Items
post_result = post(f'http://127.0.0.1:{port}/item', json={"name": "Table", "price": 6.99, "store_id": 1},
                   headers={"Authorization": f"Bearer {access_token}"})
get_result = get(f'http://127.0.0.1:{port}/item', headers={"Authorization": f"Bearer {access_token}"})

#Logout
logout = post(f'http://127.0.0.1:{port}/logout', headers={"Authorization": f"Bearer {access_token}"})
