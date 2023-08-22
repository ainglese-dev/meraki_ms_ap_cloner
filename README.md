# Meraki-MS-AccessPolicies-Cloner

Description: In order to avoid using full Meraki templates and focus directly into cloning Access Policies for MS enabled networks, the script bellow will clone / template Access Policies which will reduce human error, and speed up the process for cloning the access policies.

## Installation for debian-based OS
Virtual Environment

In your project directory, create your virtual environment
``` console
python3 -m venv venv
```
Activate (use) your new virtual environment (Linux):
``` console
source venv/bin/activate
```
Download or clone the mind_nmap repository:

``` console
git clone https://github.com/AngelIV23/Meraki-MS-AccessPolicies-Cloner.git
```

Install Python packages using pip according to the requirements.txt file
```
pip install -r requirements.txt
```
If needed, you can create optionally the next folders depending on current requirements and code tweaks you'd like to make:
```
mkdir templates_accesspolicies
mkdir output_files
```

You can easily get the public API key and play around API calls using the Cisco Meraki Get Hands-On section:

https://developer.cisco.com/meraki/meraki-platform/

## Application walkthrough:

1. Run the main script which will automatically gather data from corresponding key (by default, Meraki API is being used):

```
python meraki_main.py
```

## Results

+ Option 1 and 2 will help providing a floating API token to the system ( not saved in the system for security reasons)
+ Option 3 and 4 intended to list Organizations and networks with MS and Access Policies capabilities ( Orgs / nets with API disabled will show an error message)
+ Option 5. List all Access Policies in API-enabled and MS entitled networks. Plus: This option saves each policy in a directory for insight purposes.
+ Option 6. Since cloning Access policies is limited to a few Key-value pairs, is recommended to create a new template locally to push when needed.
+ Option 7. Pushing the template to target Network ID, which you can get from results above.


