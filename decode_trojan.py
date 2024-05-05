import json
import base64
import urllib.parse

def decode_trojan_to_clash(trojan_url):
    # Memisahkan bagian credential dan parameter dari URL
    if '#' in trojan_url:
        url, name = trojan_url.split('#')
    else:
        url = trojan_url
        name = "Unnamed"

    creds, params = url[len('trojan://'):].split('?')
    password, rest = creds.split('@')
    server, port = rest.split(':')

    query = urllib.parse.parse_qs(urllib.parse.urlparse('?' + params).query)

    config = {
        'name': name.strip(),
        'type': 'trojan',
        'server': server,
        'port': int(port),
        'password': password,
        'udp': True,
        'sni': query.get('sni', [server])[0],
        'skip-cert-verify': query.get('security', [''])[0] == 'tls',
        'network': query.get('type', [''])[0]
    }

    # Penanganan khusus berdasarkan jenis jaringan
    if config['network'] == 'ws':
        config.update({
            'ws-opts': {
                'path': query.get('path', ['/'])[0],
                'headers': {'Host': query.get('host', [server])[0]}
            }
        })
    elif config['network'] == 'grpc':
        config.update({
            'grpc-opts': {
                'grpc-service-name': query.get('serviceName', ['grpcservicename'])[0]
            }
        })

    return config

def pretty_print_trojan_config(config):
    output = [f"- name: {config['name']}"]
    output.append(f"  type: {config['type']}")
    output.append(f"  server: {config['server']}")
    output.append(f"  port: {config['port']}")
    output.append(f"  password: {config['password']}")
    output.append(f"  udp: {str(config.get('udp', True)).lower()}")
    output.append(f"  sni: {config.get('sni', '')}")
    output.append(f"  skip-cert-verify: {str(config.get('skip-cert-verify', False)).lower()}")
    output.append(f"  network: {config['network']}")

    if 'ws-opts' in config:
        ws_opts = config['ws-opts']
        output.append("  ws-opts:")
        output.append(f"    path: {ws_opts.get('path', '/')}")
        output.append("    headers:")
        for key, value in ws_opts.get('headers', {}).items():
            output.append(f"      {key}: {value}")

    if 'grpc-opts' in config:
        grpc_opts = config.get('grpc-opts', {})
        output.append("  grpc-opts:")
        output.append(f"    grpc-service-name: {grpc_opts.get('grpc-service-name', '')}")

    return '\n'.join(output)
