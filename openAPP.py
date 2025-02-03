import requests

base_url = "http://127.0.0.1:5000"

def get_info(name):
    url = f"{base_url}{name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # print("reterieved successufly")
        return data
    else:
        print(f"Failed to retrieve data {response.status_code} {name}")

info = get_info('/api')
print(info['stink'])