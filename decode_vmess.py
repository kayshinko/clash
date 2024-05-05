import json
import base64

def decode_vmess_to_clash(vmess_url):
    try:
        # Menghapus prefix "vmess://" dan mendekode dari Base64
        base64_encoded_data = vmess_url[len("vmess://"):].strip()
        # Menghapus karakter yang bukan Base64 untuk menghindari error
        base64_encoded_data = base64_encoded_data.split('#')[0]  # Memastikan tidak ada fragmen
        base64_encoded_data = ''.join(filter(lambda x: x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', base64_encoded_data))
        # Mendekode data dengan handling untuk padding yang mungkin tidak lengkap
        padded_base64_encoded_data = base64_encoded_data + '==='  # Tambahkan padding maksimal
        decoded_data = base64.urlsafe_b64decode(padded_base64_encoded_data).decode("utf-8")
        vmess_data = json.loads(decoded_data)

        base_config = {
            'name': f"Vmess-{vmess_data['ps']}",
            'type': 'vmess',
            'server': vmess_data['add'],
            'port': int(vmess_data['port']),
            'uuid': vmess_data['id'],
            'alterId': 0,
            'cipher': 'auto',
            'udp': True,
            'tls': vmess_data['tls'] == 'tls',
            'skip-cert-verify': True,
            'servername': vmess_data['add']
        }

        if vmess_data['net'] == 'ws':
            base_config.update({
                'network': 'ws',
                'ws-opts': {
                    'path': '/' + vmess_data['path'].strip('/'),
                    'headers': {'Host': vmess_data['add']}
                }
            })
        elif vmess_data['net'] == 'grpc':
            base_config.update({
                'network': 'grpc',
                'grpc-opts': {
                    'grpc-service-name': 'vmess-grpc',  # Adjust if necessary
                    'grpc-mode': 'gun'  # Assuming mode is gun
                }
            })

        return base_config
    except Exception as e:
        print(f"Error decoding VMess URL: {str(e)}")
        return {}

def pretty_print_config(config):
    # Output konfigurasi dasar
    output = [
        f"- name: {config['name']}",
        f"  server: {config['server']}",
        f"  port: {config['port']}",
        f"  type: {config['type']}",
        f"  uuid: {config.get('uuid', 'undefined')}",  # Mendapatkan uuid dengan nilai default 'undefined'
    ]

    # Kondisional untuk tipe 'vmess', termasuk menambahkan alterId hanya jika tipe adalah 'vmess'
    if config['type'] == 'vmess':
        output.append(f"  alterId: {config.get('alterId', 0)}")  # Tambahkan alterId dengan nilai default 0 jika tidak ada

    # Lanjutkan menambahkan elemen konfigurasi umum
    output += [
        f"  cipher: {config.get('cipher', 'auto')}",
        f"  tls: {str(config.get('tls', False)).lower()}",
        f"  skip-cert-verify: {str(config.get('skip-cert-verify', False)).lower()}",
        f"  servername: {config.get('servername', '')}",
        f"  network: {config['network']}"
    ]

    # Menambahkan opsi WebSocket jika ada dalam konfigurasi
    if 'ws-opts' in config:
        ws_opts = config['ws-opts']
        output.append("  ws-opts:")
        output.append(f"    path: {ws_opts.get('path', '/')}")
        output.append("    headers:")
        for key, value in ws_opts.get('headers', {}).items():
            output.append(f"      {key}: {value}")

    # Menambahkan opsi gRPC jika ada dalam konfigurasi
    if 'grpc-opts' in config:
        grpc_opts = config.get('grpc-opts', {})
        if grpc_opts:
            output.append("  grpc-opts:")
            output.append(f"    grpc-service-name: {grpc_opts.get('grpc-service-name', '')}")

    # Tambahkan UDP jika ada dalam konfigurasi
    output.append(f"  udp: {str(config.get('udp', True)).lower()}")

    # Menggabungkan semua bagian output menjadi satu string dengan pemisah baris baru
    config_string = '\n'.join(output)

    return config_string
