import json
import base64
import urllib.parse

def decode_vless_to_clash(vless_url):
    parts = vless_url.split("#")
    url = parts[0][8:]
    name = parts[1] if len(parts) > 1 else "Unnamed"
    uuid, rest = url.split("@")
    server, port = rest.split(":")
    port, params = port.split("?", 1)

    query = urllib.parse.parse_qs(urllib.parse.urlparse('?' + params).query)

    config = {
        'name': name,
        'type': 'vless',
        'server': server,
        'port': int(port),
        'uuid': uuid,
#        'alterId': 0,  # as specified in your format
        'cipher': 'auto',
        'udp': True,
        'tls': 'tls' in query.get('security', []),
        'skip-cert-verify': True,
        'servername': query.get('sni', [server])[0],
        'network': query.get('type', [''])[0],
    }

    if config['network'] == 'ws':
        config['ws-opts'] = {
            'path': query.get('path', ['/'])[0],
            'headers': {'Host': query.get('host', [server])[0]}
        }

    if config['network'] == 'grpc':
        config['grpc-opts'] = {
            'grpc-service-name': query.get('serviceName', [''])[0],
            'grpc-mode': 'gun'  # Example, adjust as needed
        }

    return config

def pretty_print_config(config):
    output = [f"  - name: {config['name']}"]
    output.append(f"    server: {config['server']}")
    output.append(f"    port: {config['port']}")
    output.append(f"    type: {config['type']}")
    output.append(f"    uuid: {config['uuid']}")
    output.append(f"    cipher: {config.get('cipher', 'auto')}")
    output.append(f"    tls: {str(config.get('tls', False)).lower()}")
    output.append(f"    skip-cert-verify: {str(config.get('skip-cert-verify', False)).lower()}")
    output.append(f"    servername: {config.get('servername', '')}")
    output.append(f"    network: {config['network']}")

    if config['network'] == 'ws':
        ws_opts = config.get('ws-opts', {})
        output.append("    ws-opts:")
        output.append(f"      path: {ws_opts.get('path', '/')}")
        output.append("      headers:")
        for key, value in ws_opts.get('headers', {}).items():
            output.append(f"        {key}: {value}")
        output.append(f"    udp: {str(config.get('udp', True)).lower()}")

    if config['network'] == 'grpc':
        grpc_opts = config.get('grpc-opts', {})
        if grpc_opts:
            output.append("    grpc-opts:")
            output.append(f"      grpc-service-name: {grpc_opts.get('grpc-service-name', '')}")
            output.append(f"    udp: {str(config.get('udp', True)).lower()}")

    return '\n'.join(output)
