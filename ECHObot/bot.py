import os
import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext, cog_ext, manage_commands
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption, Interaction
from discord.ext.menus import Menu, MenuPages, ButtonMenuPages, ListPageSource, GroupByPageSource
from supabase import create_client, Client, Storage
import gspread
from gspread import Client as GSpreadClient, Spreadsheet, Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import OAuth2Credentials
from dotenv import load_dotenv, find_dotenv
import requests

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