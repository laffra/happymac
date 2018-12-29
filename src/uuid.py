import os

def get_hardware_uuid():
    return os.popen("system_profiler SPHardwareDataType | grep UUID | sed 's/.* //' ").read()
