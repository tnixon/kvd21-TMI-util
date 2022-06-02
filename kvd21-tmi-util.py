import argparse
import requests
import json

# get password from command line
argparser = argparse.ArgumentParser()
argparser.add_argument("password", help="Admin Password for the Arcadyan KVD21 router")
args = argparser.parse_args()

# endpoint configuration
host = "192.168.12.1"
api_base = f"http://{host}/TMI/v1"


# get auth token
login_url = f"{api_base}/auth/login"
login_data = '{"username": "admin", "password": "' + args.password + '"}'
print(f"Fetching auth token from {login_url} ...")
login_response = requests.post(login_url, login_data)
login_response.raise_for_status()
auth_token = login_response.json()['auth']['token']
auth_header = {'Authorization': f"Bearer {auth_token}"}
print("Obtained auth token!")

# fetch network configuration
net_conf_url = f"{api_base}/network/configuration"
get_net_conf_params = {'get': 'ap'}
print(f"Fetching network configuration from {net_conf_url} ...")
get_net_conf_response = requests.get(net_conf_url, params=get_net_conf_params, headers=auth_header)
get_net_conf_response.raise_for_status()
net_conf = get_net_conf_response.json()
print("Obtained network config!")

# disable radios on all networks
disabled_net_conf = net_conf
for net in net_conf.keys():
    disabled_net_conf[net]['isRadioEnabled'] = False
disabled_net_conf_data = json.dumps(disabled_net_conf)

# post the updated config back to the service
set_net_conf_params = {'set': 'ap'}
print(f"Updating network configuration at {net_conf_url} ...")
set_net_conf_response = requests.post(net_conf_url, params=set_net_conf_params, headers=auth_header, data=disabled_net_conf_data)
set_net_conf_response.raise_for_status()
print("Updated network config!")