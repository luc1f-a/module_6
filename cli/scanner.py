import os
import requests
import json
import argparse
import sys

def ping_sweep(ip, num_of_host):
    ip_parts = ip.split('.')
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    scanned_ip = network_ip + str(int(ip_parts[3]) + num_of_host)
    response = os.popen(f'ping -n 1 {scanned_ip}')
    res = response.readlines()
    print(f"[#] Result of scanning: {scanned_ip} [#]\n{res[2]}", end='\n\n')


def http_proxy(target, method, headers=None, payload=None):
    headers_dict = dict()
    if headers:
        headers = headers.split(" ")
        for header in headers:
            header_name = header.split(":")[0]
            header_value = header.split(":")[1:]
            headers_dict[header_name] = ":".join(header_value)

    if method == "GET":
        response = requests.get(target, headers=headers_dict)
    elif method == "POST":
        response = requests.post(target, headers=headers_dict, data=payload)
    print(
        f"[#] Response status code: {response.status_code}\n"
        f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n" 
        f"[#] Response content:\n {response.text}")


def parse_args(arg):
    parser = argparse.ArgumentParser(description="InfSec multitool")
    parser.add_argument('task', choices=['scan', 'curl'], help='Network scan or send HTTP request')
    parser.add_argument('-i', '--ip', type=str, help='IP address')
    parser.add_argument('-n', '--num_of_hosts', type=int, help='Number of hosts')
    parser.add_argument('-t', '--target', type=str, help='Destination address')
    parser.add_argument('-m', '--method', type=str, help='HTTP method')
    parser.add_argument('--headers', type=str, help='Request headers', required=False)
    parser.add_argument('-p', '--payload', type=str, help='Request payload', required=False)
    return parser.parse_args(arg)


args = parse_args(sys.argv[1:])

if args.task == 'scan':
    for host in range(args.num_of_hosts):
        ping_sweep(args.ip, host)
if args.task == 'curl':
    http_proxy(args.target, args.method, args.headers, args.payload)