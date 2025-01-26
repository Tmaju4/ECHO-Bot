import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_components import DiscordComponents, Button, ButtonStyle, Interaction
from supabase import create_client, Client
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Discord bot setup
intents = discord.Intents.all()  # すべてのインテンツを有効にする
bot = commands.Bot(command_prefix="!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)
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

@bot.command()
async def dice(ctx):
    random_dice1 = random.randint(1, 100)
    if random_dice1 > 95:
        await ctx.send(f"{random_dice1}! ファンブル！")
    elif random_dice1 < 5:
        await ctx.send(f"{random_dice1}! クリティカル！")
    else:
        await ctx.send(f"{random_dice1}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


token = os.getenv('DISCORD_TOKEN')
bot.run(token)