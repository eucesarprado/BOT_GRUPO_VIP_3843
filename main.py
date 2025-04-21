from telethon import TelegramClient, events
import os
from flask import Flask, render_template_string
from threading import Thread

# 🟢 Painel visual com status
HTML_PAINEL = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Bot VIP - Status</title>
  <style>
    body {
      background: #0f0f0f;
      font-family: Arial, sans-serif;
      color: #ffffff;
      text-align: center;
      padding: 50px;
    }
    .card {
      background: #1e1e1e;
      padding: 30px;
      border-radius: 12px;
      max-width: 500px;
      margin: 0 auto;
      box-shadow: 0 0 10px rgba(255, 0, 85, 0.3);
    }
    h1 {
      color: #ff0055;
    }
    .status {
      font-size: 18px;
      margin-top: 15px;
    }
    a {
      color: #00d9ff;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="card">
    <h1>💎 Bot do Grupo VIP</h1>
    <div class="status">
      Status: <strong style="color: #00ff88">Online ✅</strong><br><br>
      Última atualização automática funcionando.
    </div>
    <div style="margin-top: 30px;">
      <a href="https://t.me/SEU_GRUPO_VIP_AQUI" target="_blank">🔗 Acessar Grupo VIP</a>
    </div>
  </div>
</body>
</html>
"""

app = Flask('')

@app.route('/')
def home():
    return render_template_string(HTML_PAINEL)

def manter_online():
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()

# 🔐 API do Telegram
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
client = TelegramClient("session", api_id, api_hash)

# 🛰️ Canais VIP (apenas mídia, sem legenda)
origens = [-1002368866066, -4686930379, -1002060060299]
destino_id = -1002678360646
grouped_processados = set()

@client.on(events.NewMessage(chats=origens))
async def handler(event):
    msg = event.message
    if msg.grouped_id:
        if msg.grouped_id in grouped_processados:
            return
        grouped_processados.add(msg.grouped_id)
        print("📦 Álbum VIP detectado.")
        messages = await client.get_messages(event.chat_id, limit=20, min_id=msg.id - 10)
        grupo = [m for m in messages if m.grouped_id == msg.grouped_id]
        grupo = list(reversed(grupo))
        media_files = [m.media for m in grupo if m.media]
        if media_files:
            print(f"🎯 Enviando álbum com {len(media_files)} mídias...")
            await client.send_file(destino_id, media_files)
    elif msg.photo or msg.video:
        print("📸 Mídia única VIP detectada.")
        await client.send_file(destino_id, msg.media)

manter_online()
client.start()
print("🤖 Bot do Grupo VIP rodando com painel ativo...")
client.run_until_disconnected()
