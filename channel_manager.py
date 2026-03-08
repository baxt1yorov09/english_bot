# Channel storage - for now using simple list
# In production, you should use database
import json
import os

CHANNELS_FILE = "channels.json"

def load_channels():
    """Load channels from file"""
    if os.path.exists(CHANNELS_FILE):
        try:
            with open(CHANNELS_FILE, 'r') as f:
                return json.load(f)
        except:
            return ["@SirojiddinovAcademy"]
    return ["@SirojiddinovAcademy"]

def save_channels(channels):
    """Save channels to file"""
    try:
        with open(CHANNELS_FILE, 'w') as f:
            json.dump(channels, f)
        return True
    except:
        return False

def add_required_channel(channel_name):
    """Add channel to required list"""
    channels = load_channels()
    if channel_name not in channels:
        channels.append(channel_name)
        if save_channels(channels):
            return True
    return False

def remove_required_channel(channel_name):
    """Remove channel from required list"""
    channels = load_channels()
    if channel_name in channels:
        channels.remove(channel_name)
        if save_channels(channels):
            return True
    return False

def get_required_channels():
    """Get all required channels"""
    return load_channels()
