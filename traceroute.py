import os
import re
import subprocess

from config import MAX_TTL, WAIT, DIR_TEMP_FILES

def traceroute(host: str) -> str:
    cmd = ['traceroute', '-e', '-m', str(MAX_TTL), '-w', str(WAIT), host] # REVIEW
    suffix = host.replace('.', '_')
    filename_output = os.path.join(DIR_TEMP_FILES, f'traceroute_{suffix}')
    if not os.path.isfile(filename_output):
        with open(filename_output, 'w') as fp:
            cp = subprocess.run(cmd, stdout=fp)
            assert cp.returncode == 0
    return TracerouteOutput(filename_output)

#11  * ae3.cs1.lga5.us.eth.zayo.com (64.125.29.208)  158.253 ms *

class TracerouteOutput(list):
    class TracerouteOutputLine:
        def __init__(self, line: str):
            m = re.match(r'^ *([0-9]{1,}) *([^ ]*) *\(([^ ]*)\)  ([0-9]+\.[0-9]+) ms  ([0-9]+\.[0-9]+) ms  ([0-9]+\.[0-9]+) ms$', line[:-1])
            if bool(m) and len(m.groups()) == 6:
                self.hop = int(m.group(1))
                self.domain_name = m.group(2)
                self.ip = m.group(3)
                self.rtt1 = float(m.group(4))
                self.rtt2 = float(m.group(5))
                self.rtt3 = float(m.group(6))
            else:
                m = re.match(r'^ *([0-9]{1,})', line[:-1])
                # if m is None or len(m.groups()) != 1:
                #     assert False, line
                assert len(m.groups()) >= 1, line
                self.hop = int(m.group(1))
                self.domain_name = None
                self.ip = None
                self.rtt1 = None
                self.rtt2 = None
                self.rtt3 = None
        # def __str__(self):
        #     return f'{self.hop} {self.domain_name} ({self.ip}) {self.rtt1}ms {self.rtt2}ms {self.rtt3}ms'

    def __init__(self, path_output: str):
        assert os.path.isfile(path_output), path_output
        lines = None
        with open(path_output, 'r') as fp:
            lines = fp.readlines()
        assert lines is not None
        for line in lines:
            #'1  192.168.1.1 (192.168.1.1)  3.724 ms  6.837 ms  1.851 ms\n'
            self.append(TracerouteOutput.TracerouteOutputLine(line))
    # def __repr__(self):
    #     assert len(self) > 0
    #     return '\n'.join(str(line) for line in self)

if __name__ == '__main__':
    from pprint import pprint
    output = TracerouteOutput('traceroute_sydney_edu_au')
    # print(output)
    ips = list(map(lambda l: l.ip, output))
    # pprint(ips)
    for ip in ips:
        print(ip)
