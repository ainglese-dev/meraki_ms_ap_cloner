import json

def collect_and_save_policy():
    policy = {}

    # Collect values interactively from the user
    policy["name"] = input("Enter policy name: ")

    radius_servers = []
    while True:
        server = {}
        server["host"] = input("Enter radius server host: ")
        server["port"] = int(input("Enter radius server port [1812]: ") or "1812") 
        server["secret"] = input("Enter radius server secret: ")
        radius_servers.append(server)

        another_server = input("Add another radius server? (yes/no): ")
        if another_server.lower() != "yes":
            break
    policy["radiusServers"] = radius_servers

    critical_auth = {}
    user_input01  = input("Critical Enter data VLAN ID [null]: ")
    critical_auth["dataVlanId"] = int(user_input01) if user_input01 else None

    user_input02  = input("Critical Enter voice VLAN ID [null]: ")
    critical_auth["voiceVlanId"] = int(user_input02) if user_input02 else None
    critical_auth["suspendPortBounce"] = (input("Suspend port bounce? (true/false)[false]: ").lower() == "true") or False
    # print(critical_auth['suspendPortBounce'])
    policy["radius"] = {
        "criticalAuth": critical_auth,
        "failedAuthVlanId": int(input("Enter failed auth / quarantine VLAN ID: ")),
        "reAuthenticationInterval": int(input("Enter re-authentication interval [120 sec]: ") or "120")
    }

    policy["guestPortBouncing"] = (input("Guest port bouncing? (true/false)[false]: ").lower() == "true") or False
    policy["radiusTestingEnabled"] = (input("Radius testing enabled? (true/false)[false]: ").lower() == "true") or False
    policy["radiusCoaSupportEnabled"] = (input("Radius CoA support enabled? (true/false)[true]: ").lower() == "true") or True
    policy["radiusAccountingEnabled"] = (input("Radius accounting enabled? (true/false)[true]: ").lower() == "true") or True

    radius_accounting_servers = []
    while True:
        server = {}
        server["host"] = input("Enter radius accounting server host: ")
        server["port"] = int(input("Enter radius accounting server port [1813]: ") or "1813")
        server["secret"] = input("Enter radius accounting server secret: ")
        radius_accounting_servers.append(server)

        another_server = input("Add another radius accounting server? (yes/no): ")
        if another_server.lower() != "yes":
            break
    policy["radiusAccountingServers"] = radius_accounting_servers

    policy["radiusGroupAttribute"] = input("Enter radius group attribute [11]: ") or "11"
    policy["hostMode"] = input("Enter host mode (Single-Host, Multi-host, Multi-Auth, Multi-Domain): ")

    access_policy_type = input("Enter access policy type (Hybrid authentication, MAC authentication bypass, 802.1x): ")
    if access_policy_type == "Hybrid authentication":
        policy["increaseAccessSpeed"] = input("Increase access speed? (true/false): ").lower() == True
    policy["accessPolicyType"] = access_policy_type
    policy["dot1x"] = {
        "controlDirection": input("Enter dot1x control direction (inbound, both)[inbound]: ") or "inbound"
    }
    
    policy["guestVlanId"] = int(input("Enter guest VLAN ID: "))
    policy["voiceVlanClients"] = (input("Voice VLAN clients? (true/false)[true]: ").lower() == "true") or True
    policy["urlRedirectWalledGardenEnabled"] = (input("URL redirect walled garden enabled? (true/false)[false]: ").lower() == "true") or False
    if policy["urlRedirectWalledGardenEnabled"]:
        policy["urlRedirectWalledGardenRanges"] = input("Enter URL redirect walled garden ranges (comma-separated): ").split(",")

    # Save the policy to a JSON file
    file_name = input("Enter JSON file name to save: ")
    with open("templates_accesspolicies/" + file_name + ".json", "w") as f:
        json.dump(policy, f, indent=4)
    
    print(f"Policy saved to templates_accesspolicies/'{file_name}'.json")
    
