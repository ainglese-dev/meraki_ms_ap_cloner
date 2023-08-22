import os
import json
import meraki
import requests
from tabulate import tabulate

def list_policy_files(path):
    policy_files = [f for f in os.listdir(path) if f.endswith('.json')]
    return policy_files

def display_file_list(files):
    print("Available Policy Files:")
    for idx, file in enumerate(files, start=1):
        print(f"{idx}. {file}")

def load_policy_from_file(file_path):
    with open(file_path, 'r') as f:
        policy_data = json.load(f)
    return policy_data

def post_policy_to_network(api_key, network_id, policy_data):
    # Initialize Meraki Dashboard API
    # dashboard = meraki.DashboardAPI(api_key, suppress_logging=True)

    try:
        url = f"https://api.meraki.com/api/v1/networks/{network_id}/switch/accessPolicies"
        payload = json.dumps(policy_data)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": api_key
        }
        # print(payload)
        response = requests.request('POST', url, headers=headers, data = payload)
        # print(response.text.encode('utf8'))

        # response = dashboard.switch.createNetworkSwitchAccessPolicy(
        #     network_id,
        #     name=policy_data['name'],
        #     radius_servers=policy_data['radiusServers'],
        #     radius_testing_enabled=policy_data['radiusTestingEnabled'],
        #     radius_coa_support_enabled=policy_data['radiusCoaSupportEnabled'],
        #     radius_accounting_enabled=policy_data['radiusAccountingEnabled'],
        #     host_mode=policy_data['hostMode'],
        #     url_redirect_walled_garden_enabled=policy_data['urlRedirectWalledGardenEnabled'],
        #     radius=policy_data['radius'],
        #     guestPortBouncing=policy_data['guestPortBouncing'],
        #     radiusAccountingServers=policy_data['radiusAccountingServers'],
        #     radiusGroupAttribute=policy_data['radiusGroupAttribute'],
        #     accessPolicyType=policy_data['accessPolicyType'],
        #     guestVlanId=policy_data['guestVlanId'],
        #     dot1x=policy_data['dot1x'],
        #     voiceVlanClients=policy_data['voiceVlanClients']
        # )

        print("\n\nPolicy configuration posted successfully.\n\n")
        # print(response.status_code)
        # print(response.text)

    except meraki.exceptions.APIError as e:
        print(f"Error posting policy configuration: {e}")

