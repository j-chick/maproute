import os
import re
import subprocess

from config import DIR_TEMP_FILES

def nslookup(host: str) -> str:
    cmd = ['nslookup', host]
    suffix = host.replace('.', '_')
    filename_output = os.path.join(DIR_TEMP_FILES, f'nslookup_{suffix}')
    with open(filename_output, 'w') as fp:
        cp = subprocess.run(cmd, stdout=fp)
        assert cp.returncode == 0
    ip = None
    with open(filename_output, 'r') as fp:
        for line in fp.readlines():
            m = re.match(r'Address: +([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})', line)
            if bool(m):
                ip = str(m.group(1))
                break # NOTE disregards subsequent IPs
    return ip