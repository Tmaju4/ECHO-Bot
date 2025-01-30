import os
import discord
from discord.ext import commands
from discord_components import DiscordComponents, Button, ButtonStyle
from discord.ext import menus
from supabase import create_client, Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Discord bot setup
intents = discord.Intents.all()  # すべてのインテンツを有効にする
bot = commands.Bot(command_prefix="!", intents=intents)
DiscordComponents(bot)

# Supabase setup
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path/to/your/service_account.json', scope)
gspread_client: GSpreadClient = gspread.authorize(creds)

# ボットが起動したときのメッセージ
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Supabaseからボットの状態を取得する関数
def get_bot_status():
    response = supabase.table('bot_status').select('status').eq('id', 1).execute()
    return response.data[0]['status']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$start'):
        supabase.table('bot_status').update({'status': True}).eq('id', 1).execute()
        await message.channel.send('Bot started!')

    if message.content.startswith('$stop'):
        supabase.table('bot_status').update({'status': False}).eq('id', 1).execute()
        await message.channel.send('Bot stopped!')

# ボットの状態を監視し、必要に応じて起動・停止
if __name__ == "__main__":
    status = get_bot_status()
    if status:
        client.run(TOKEN)