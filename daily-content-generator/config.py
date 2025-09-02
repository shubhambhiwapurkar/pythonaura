import os
from azure.appconfiguration.provider import load, SettingSelector

def get_settings():
    if os.getenv("AZURE_APP_CONFIG_CONNECTION_STRING"):
        return load(
            connection_string=os.getenv("AZURE_APP_CONFIG_CONNECTION_STRING"),
            selectors=[SettingSelector(key_filter="*", label_filter="\0")]
        )
    return os.environ

settings = get_settings()