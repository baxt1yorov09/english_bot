# Channel storage - for now using simple list
# In production, you should use database
REQUIRED_CHANNELS = ["@SirojiddinovAcademy"]

def add_required_channel(channel_name):
    """Add channel to required list"""
    global REQUIRED_CHANNELS
    if channel_name not in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.append(channel_name)
        return True
    return False

def remove_required_channel(channel_name):
    """Remove channel from required list"""
    global REQUIRED_CHANNELS
    if channel_name in REQUIRED_CHANNELS:
        REQUIRED_CHANNELS.remove(channel_name)
        return True
    return False

def get_required_channels():
    """Get all required channels"""
    return REQUIRED_CHANNELS.copy()
