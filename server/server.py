import io
from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)


# Endpoint для выполнения ping sweep
@app.route('/scan', methods=['GET'])
def ping_sweep():
    ip = request.args.get('ip')
    num_of_host = int(request.args.get('num_of_host'))

    ip_parts = ip.split('.')
    network_ip = ip_parts[0] + '.' + ip_parts[1] + '.' + ip_parts[2] + '.'
    builder = io.StringIO()

    for host in range(num_of_host):
        scanned_ip = network_ip + str(int(ip_parts[3]) + host)
        response = os.popen(f'ping -c 1 {scanned_ip}')
        builder.write(f"[#] Result of scanning: {scanned_ip} [#]\n{response.read()}\n")
    result = builder.getvalue()
    builder.close()
    return result


# Endpoint для выполнения HTTP-proxy-сервера
@app.route('/sendHttp', methods=['POST'])
def http_proxy():
    target = request.json.get('target')
    method = request.json.get('method', 'GET')
    headers = request.json.get('headers', {})
    payload = request.json.get('payload', {})

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
    return \
        f"[#] Response status code: {response.status_code}\n" \
        f"[#] Response headers: {json.dumps(dict(response.headers), indent=4, sort_keys=True)}\n" \
        f"[#] Response content:\n {response.text}"


app.run(host='0.0.0.0', port=3000)
