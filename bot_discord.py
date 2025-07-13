import os
import discord
from main import chat  # Sua função de agente!
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv(
    "DISCORD_TOKEN") or DISCORD_TOKEN = "SEU_TOKEN_AQUI"


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Bot conectado como {self.user}')

    async def on_message(self, message):
        # Evita loop do próprio bot
        if message.author == self.user:
            return

        # Só responde se for mencionado ou DM
        if self.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel):
            pergunta = message.content.replace(
                f"<@{self.user.id}>", "").strip()
            if pergunta:
                await message.channel.send("⏳ Processando...")
                resposta = chat(pergunta)
                await message.channel.send(resposta)


intents = discord.Intents.default()
intents.message_content = True  # Necessário para ler mensagens!

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
