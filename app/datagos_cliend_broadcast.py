import json
from socket import *

if __name__ == '__main__':
    target = ('255.255.255.255', 9999)
    trace = {"message": "trace message"}
    cs = socket(AF_INET, SOCK_DGRAM)
    cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
    # cs.sendto(b'This is a test', ('255.255.255.255', 9999))
    cs.sendto(bytes(json.dumps(trace), 'utf-8'), target)
    another_trace = '{"system":{"get_sysinfo":{}}}'
    cs.sendto(bytes(another_trace, 'utf-8'), target)
