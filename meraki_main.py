import meraki
import os
import json
import re
from tabulate import tabulate
from banner import banner_meraki
from meraki_post_accesspolicy import list_policy_files, display_file_list, load_policy_from_file, post_policy_to_network
from template_policy import collect_and_save_policy

MENU_OPTIONS = {
    1: "View Meraki API Key",
    2: "Set Meraki API Key",
    3: "Gather and List all Meraki Orgs",
    4: "Gather and List all Meraki Networks",
    5: "List all Access Policies per Meraki Network (Mandatory API key and step 4)",
    6: "Create template Access policy",
    7: "Push Access Policy from file to Meraki Network",
    10: "Exit"
}

def display_menu():
    """ display menu """
    print("\nMeraki Cloner Menu:\n")
    for option, description in MENU_OPTIONS.items():
            print(f"{option}. {description}")

def view_api_key():
    """ Viewing API Key """
    if 'API_KEY' in os.environ:
        print(f"Current API Key: {os.environ['API_KEY']}")
    else:
        print("API Key is not defined.")

def set_api_key():
    """ Setting API Key """
    api_key = input("Enter your API key: ")

    # Check if API_KEY is already defined
    if 'API_KEY' in os.environ:
        overwrite = input("API_KEY is already defined. Do you want to overwrite it? (yes/no): ")
        if overwrite.lower() != 'yes':
            print("API key has not been saved.")
            return

    # Save the API key as an environment variable
    os.environ['API_KEY'] = api_key

    print("API key has been saved as an environment variable.")

def print_organizations():
    # Initialize Meraki Dashboard API
    API_KEY = os.environ.get("API_KEY")
    if API_KEY is None:
        print("Please set the API_KEY environment variable.")
    else:
        try:
            dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
            # Get list of organizations
            org_list = dashboard.organizations.getOrganizations()
            print('\n\n')
            # Prepare data for tabulate
            org_data = []
            for org in org_list:
                org_data.append([org['name'], org['id']])
            headers = ["Organization Name", "Organization ID"]
            print(tabulate(org_data, headers=headers, tablefmt="grid"))
        except meraki.exceptions.APIError as e:
            if e.response.status_code == 401:
                print(f"Error: {e}")
                print(f"Skipping due to API access issue: {e.response}")
            else:
                raise e

def print_networks():
    # Initialize Meraki Dashboard API
    API_KEY = os.environ.get("API_KEY")
    if API_KEY is None:
        print("Please set the API_KEY environment variable.")
    else:
        dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
        # Get list of organizations
        org_list = dashboard.organizations.getOrganizations()
        # Prepare data for tabulate
        network_data = []

        for org in org_list:
            org_id = org['id']
            org_name = org['name']
            try:
                # Get list of networks in the organization
                network_list = dashboard.organizations.getOrganizationNetworks(org_id)
                for network in network_list:
                    network_data.append([org_name, org_id, network['name'], network['id']])
            except meraki.exceptions.APIError as e:
                if e.response.status_code == 403:
                    # print(f"Error: {e}")
                    print(f"Skipping organization '{org_name}' (ID: {org_id}) due to API access issue.")
                elif e.response.status_code == 404:
                    # print(f"Error: {e}")
                    print(f"Skipping organization '{org_name}' (ID: {org_id}) due to disabled API access.")
                else:
                    raise e

    # Print networks in a table
        print("\n\n")
        headers = ["Org Name", "Org ID", "Network Name", "Network ID"]
        print(tabulate(network_data, headers=headers, tablefmt="grid"))
        return network_data

def save_json_file(data, filename):
    # Sanitize the filename by removing special characters and replacing spaces with underscores
    sanitized_filename = re.sub(r'[^\w\s-]', '', filename)
    sanitized_filename = re.sub(r'\s+', '_', sanitized_filename)
    path = "output_files/"
    # Add the ".json" extension if not present
    if not sanitized_filename.endswith('.json'):
        sanitized_filename += '.json'
    sanitized_filename = path + sanitized_filename
    # Save the data as a JSON file
    with open(sanitized_filename, 'w') as file:
        json.dump(data, file, indent=4)

def print_access_policies(network_id):
    # Initialize Meraki Dashboard API
    API_KEY = os.environ.get("API_KEY")
    if API_KEY is None:
        print("Please set the API_KEY environment variable.")
    else:
        policy_data = []
        for network in network_id:
            dashboard = meraki.DashboardAPI(API_KEY, suppress_logging=True)
            
            try:
                # Get list of access policies for the specified network
                access_policies = dashboard.switch.getNetworkSwitchAccessPolicies(network[3])
                # Prepare data for tabulate

                if not access_policies:
                    print(f"Network with ID '{network[3]}' Access policy is empty.")
                else:
                    for policy in access_policies:
                        policy_data.append([network[0], 
                                            network[1], 
                                            network[2], network[3], 
                                            policy['accessPolicyNumber'], 
                                            policy['name'], 
                                            policy['accessPolicyType']])
                    save_json_file(policy, network[0] + network[2] + policy['name'])

            except meraki.exceptions.APIError as e:
                if e.response.status_code == 404:
                    # print(f"Error: {e}")
                    print(f"Network with ID '{network[3]}' not found.")
                elif e.response.status_code == 400:
                    # print(f"Error: {e}")
                    print(f"Network with ID '{network[3]}' No MS switch in network.")
                else:
                    raise e
                # Print access policies in a table

        print("\n\n")
        headers = ["Org Name", "Org ID", "Net Name", "Net ID", "Policy ID", "Policy Name", "Access Policy Type"]
        print(tabulate(policy_data, headers=headers, tablefmt="grid"))

def post_access_policy():
    API_KEY = os.environ.get("API_KEY")
    if API_KEY is None:
        print("Please set the API_KEY environment variable.")
    else:
        NETWORK_ID = input("Type in your target Network ID: ")  # Replace with your actual network ID
        POLICY_PATH = "templates_accesspolicies"  # Replace with the path to your policy JSON files

        policy_files = list_policy_files(POLICY_PATH)
        if not policy_files:
            print("No policy files found.")
        else:
            display_file_list(policy_files)
            choice = int(input("Select a policy file (enter the number): ")) - 1

            if 0 <= choice < len(policy_files):
                selected_file = policy_files[choice]
                file_path = os.path.join(POLICY_PATH, selected_file)
                policy_data = load_policy_from_file(file_path)
                post_policy_to_network(API_KEY, NETWORK_ID, policy_data)
            else:
                print("Invalid choice.")

def main():
    current_org_id = []
    current_network_id = []
    while True:
        display_menu()
        choice = input("\nSelect an option: ")
        if choice == '1':
            view_api_key()
        elif choice == '2':
            set_api_key()
        elif choice == '3':
            print_organizations()
        elif choice == '4':
            current_network_id = print_networks()
        elif choice == '5' and current_network_id:
            print_access_policies(current_network_id)
        elif choice == '6':
            collect_and_save_policy()
        elif choice == '7':
            post_access_policy()
        elif choice == '10':
            print("\nExiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    print(banner_meraki)
    main()
