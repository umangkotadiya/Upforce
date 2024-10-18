import requests

# Step 1: Login to get the token
# login_url = "http://127.0.0.1:8000/accounts/"
login_url = "http://127.0.0.1:8000/accounts/login/"

login_data = {
    "username": "harsh",
    "password": "harsh123"
}
response = requests.post(login_url, json=login_data)
response_data = response.json()

# Check if login was successful
if response.status_code == 200:
    access_token = response_data['access']
    refresh_token = response_data['refresh']

    # Step 2: Use the token to access protected endpoint
    # url = "http://127.0.0.1:8000/blog/"
    # url = "http://127.0.0.1:8000/blog/4/"
    # url = "http://127.0.0.1:8000/like/4/"
    url = "http://127.0.0.1:8000/me/"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    postdata = {
        "title": "harsh last private update request",
        "description": "harsh last private update request",
        "content": "harsh last private update request",
        "public": False,
        "other_details": "harsh last private update request"
    }


    #All api end point
    response = requests.get(url, headers=headers)
    # response = requests.post(url, headers=headers, json=postdata)
    # response = requests.patch(url, headers=headers, json=postdata)
    # response = requests.post(url, headers=headers)
    # response = requests.delete(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 201:  # 201 is the typical status code for successful creation
        print("Successfully created the blog post")
        print(response.json())
    else:
        print("Failed to create the blog post")
        print(response.json())
else:
    print("Login failed")
    print(response_data)
