from clr_loader import get_coreclr
from pythonnet import set_runtime, get_runtime_info

##################################################
# Setup
##################################################
# Set pythonnet to use .NET 6 runtime
runtime = get_coreclr()
set_runtime(runtime)

import time
import os
import clr
import sys
import secrets
import string

# Set the path to your .NET 6 DLL
DLL_RELATIVE_PATH = "\\lib\\ruiSDKDotNet_5.6.1.dll"
DLL_FULL_PATH = os.path.dirname(os.path.abspath(__file__)) + DLL_RELATIVE_PATH 

# Add the DLL directory to sys.path
sys.path.append(os.path.dirname(DLL_FULL_PATH))

# Load the .NET 6 Assembly
clr.AddReference(DLL_FULL_PATH)

# Import the namespace/class from your DLL
from RUISDK_5_6_0 import RUISDK, RUIProtocolType, RUIResult


##################################################
# Constants and Global Variables
##################################################
global mySDK
global session_id
session_id = None
DEFAULT_CONFIG = {
    "rui_product_id": "2399118365",
    "rui_app_name": "RUI_Demo_App",
    "rui_url": "36368.tbnet1.com",
    "rui_key": "18864666411186DADA2DF73E91457D51"
}

APP_INFO = {
    "product_edition" : "Professional",
    "language": "English",
    "product_version" : "5.0.0",
    "build_number" : "17393"
}

##################################################
# Function Definitions
##################################################

# Function to start RUI tracking
def start_rui_tracking(use_session=False,config=DEFAULT_CONFIG):
    global mySDK, session_id
    registerDefaultReachOut = True
    ruiSDKDLLPath = os.path.dirname(os.path.abspath(__file__))+"\\lib"
    ruiSDKDLLNAME = "ruiSDK_5.6.0.x64.dll"

    mySDK = RUISDK(registerDefaultReachOut,ruiSDKDLLPath, ruiSDKDLLNAME)
    myPath = "./logs"
    myProductId = config['rui_product_id']
    myAppName = config['rui_app_name'] #App Name cannot contain whites spaces
    myURL = config['rui_url'] 
    myKey = config['rui_key'] 
    myProtocol = int(RUIProtocolType.httpPlusEncryption)

    if use_session:
        myMultiSessionSetting = True
        session_id = generate_session_id()
    else:
        myMultiSessionSetting = False
    myReachOutAutoSyncSetting = True # The flag to determine whether or not a ReachOut should be requested as part of each SDK Automatic Sync operation.

    mySDK.CreateConfig(myPath, myProductId, myAppName, myURL, myProtocol, myKey, myMultiSessionSetting, myReachOutAutoSyncSetting)
    
    myProductEdition = APP_INFO["product_edition"]
    myLanguage = APP_INFO["language"]
    myVersion = APP_INFO["product_version"]
    myBuildNumber = APP_INFO["build_number"]
    mySDK.SetProductData(myProductEdition, myLanguage, myVersion, myBuildNumber)
    mySDK.StartSDK()
    if session_id:
        mySDK.StartSession(session_id)
        return f"Session started with id {session_id}"
    return "RUI Tracking Started"

# Function to stop RUI tracking
def stop_rui_tracking():
    global mySDK, session_id
    if session_id:
        mySDK.StopSession(session_id)
        mySDK.StopSDK(0)
        prev_session_id = session_id
        session_id = None
        return f"Session {prev_session_id} stopped"
    mySDK.StopSDK(0)
    return "RUI Tracking Stopped"

# Function to generate a random session ID
def generate_session_id():
    length = secrets.randbelow(55) + 10  # Random length between 10 and 64
    characters = string.ascii_letters + string.digits  # Alphanumeric characters
    return ''.join(secrets.choice(characters) for _ in range(length))

# Track event or text event
def track_event(event_name, event_action, event_text=None):
    global mySDK, session_id
    if event_text:
        if session_id:
            return mySDK.TrackEventText(event_name, event_action, event_text, session_id)
        else:
            return mySDK.TrackEventText(event_name, event_action, event_text)
    else:
        if session_id:
            return mySDK.TrackEvent(event_name, event_action, session_id)
        else:
            return mySDK.TrackEvent(event_name, event_action)

# Track event with custom numeric value (float)
def track_event_numeric(event_category, event_name, custom_value):
    global mySDK, session_id
    if session_id:
        return mySDK.TrackEventNumeric(event_category, event_name, custom_value, session_id)
    else:
        return mySDK.TrackEventNumeric(event_category, event_name, custom_value)

# Get all manual reachout campaigns
def manually_get_all_reachouts():
    global mySDK
    message = ""
    message_type = 0
    msg_count = 0
    messages = []
    response = mySDK.CheckForReachOut(message,message_type,msg_count)
    msg_count = response[2]
    message_type = response[3]
    message =response[1]
    result = response[0]
    while msg_count > 0 and result == RUIResult.ok:
        if message_type == 1: # Text
            new_message = {
                "type": "text",
                "message": message
            }
            messages.append(new_message)
        elif message_type == 2: # URL
            new_message = {
                "type": "url",
                "message": message
            }
            messages.append(new_message)
        response = mySDK.CheckForReachOut(message,message_type,msg_count)
        msg_count = response[3]
        message_type = response[2]
        message =response[1]
        result = response[0]
    return messages  


##################################################
# Main For Testing Code
##################################################
# print(start_rui_tracking(use_session=True))
# print(manually_get_all_reachouts())
# if session_id:
#     print(mySDK.TrackEvent("Feature_Request", "survey-acquire", session_id))
# else:
#     mySDK.TrackEvent("Feature_Request", "survey-acquire")
# time.sleep(1)
# if session_id:
#     mySDK.TrackEvent("Feature_Request", "survey-return", session_id)
# else:
#     mySDK.TrackEvent("Feature_Request", "survey-return")
# time.sleep(1)
# print(mySDK.TrackEventText("Feature_Request", "survey-acquire", "This is a test event with text", session_id))
# time.sleep(1)
# print(stop_rui_tracking())
