from crowd_api import CrowdAPI
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# This script was created by Travis Walter on October 10th, 2020

# Atlassian Crowd API interface (redacted for security)
crowd = CrowdAPI(api_url = "", app_name = "crowd", app_password = "")

# Function that returns the user from the crowd
def getUser(user):
    request = crowd.get_user(username = str(user))
    if request['status']:
        return (request['user'])

# Function that returns the user attributes from the crowd
def getUserAttribute(user):
    request = crowd.get_user_attributes(username = str(user))
    if request['status']:
        return (request)

# Function that creates a user within the crowd
def createUser(username, first, last, display, mail):
    request = crowd.create_user(name = str(username), first_name = str(first), last_name = str(last), display_name = str(display), email = str(mail))
    if request['status']:
        return (request['password'])

# Function that assigns a user to a group within the crowd
def assign_user_group(user, group):
    request = crowd.add_user_to_group(username = str(user), groupname = str(group))
    if request['status']:
        return ("Added!")

# Function that assigns a user attribute in the crowd
def assign_user_attribute(user, name, value):
    request = crowd.set_user_attribute(username = str(user), attribute_name = str(name), attribute_value = str(value))
    if request['status']:
        return ("Attribute created")

# Function that deactivates user in the crowd
def deactivate_user(user):
    request = crowd.set_user_activity(username = str(user), active = False)
    if request['status']:
        return ("Deactivated!")

# Function that reactivates user in the crowd
def reactivate_user(user):
    request = crowd.set_user_activity(username = str(user), active = True)
    if request['status']:
        return ("Activated!")