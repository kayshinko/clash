from telethon import TelegramClient, events
import decode_vmess
import decode_vless
import decode_trojan
from telethon import TelegramClient, events
import io
from decode_vmess import decode_vmess_to_clash, pretty_print_config
from decode_vless import decode_vless_to_clash
from decode_trojan import decode_trojan_to_clash

api_id = '18209646'
api_hash = 'a9eecb9f8763ed62d36636e6ee3592f0'
bot_token = '7127462683:AAE4sT-S3qtZpvh5stRHRpAYIV7xpNTrZDI'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

name_count = {}

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Pesan selamat datang dan informasi bot
    welcome_message = """
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
**Selamat datang di Clash Configuration Bot** 🤖
Saya dapat membantu mengonversi URL 
protokol Vmess, Vless, dan Trojan ke format Clash.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
**Cara Penggunaan:**
Kirimkan link dengan format 
vmess://, vless://, atau trojan:// 
dan saya akan mengubahnya menjadi konfigurasi Clash.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Group Support: [𝐈𝐍𝐉𝐄𝐂𝐓𝐎𝐑 𝐈𝐃](t.me/vpn_injectorid)
Owner: [𝐒𝐌𝐈𝐋𝐀𝐍𝐒 𝟏𝟖+](t.me/XsSmilanSsX)
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
"""
    await event.reply(welcome_message, parse_mode='markdown')

@client.on(events.NewMessage(pattern='(vmess|vless|trojan)://.*'))
async def handle_decode(event):
    urls = [line.strip() for line in event.text.splitlines() if any(proto in line for proto in ['vmess://', 'vless://', 'trojan://'])]
    output_konfigurasi = []
    for url in urls:
        if 'vmess://' in url:
            config = decode_vmess.decode_vmess_to_clash(url)
        elif 'vless://' in url:
            config = decode_vless.decode_vless_to_clash(url)
        elif 'trojan://' in url:
            config = decode_trojan.decode_trojan_to_clash(url)
        
        base_name = config['name']
        if base_name in name_count:
            name_count[base_name] += 1
            config['name'] = f"{base_name}-{name_count[base_name]}"
        else:
            name_count[base_name] = 1
            config['name'] = f"{base_name}-1"
        
        formatted_config = pretty_print_config(config)
        output_konfigurasi.append(formatted_config)
    
    # Teks informasi tentang owner dan grup
    owner_and_group_info = (
        "Group Support: [𝐈𝐍𝐉𝐄𝐂𝐓𝐎𝐑 𝐈𝐃](t.me/vpn_injectorid)\n"
        "Owner: [𝐒𝐌𝐈𝐋𝐀𝐍𝐒 𝟏𝟖+](t.me/XsSmilanSsX)\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
    )

    # Konfigurasi proksi dengan informasi di atasnya
    konfigurasi_proksi = owner_and_group_info + "```proxies:\n" + '\n'.join(output_konfigurasi)
    await event.respond(f"\n{konfigurasi_proksi}```\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬", parse_mode='markdown')


client.run_until_disconnected()
