import os
import discord
from discord import app_commands
from discord.ext import commands
from version import version_
from keep_alive import keep_alive
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
activity = discord.Activity(type=discord.ActivityType.listening,
                            name=f"/help | V{version_}")
intents = discord.Intents().all()

class aclient(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix=['-'],
                      intents=intents,
                      case_insensitive=True,
                      activity=activity,
                      status=discord.Status.idle)
    self.synced = False
    self.remove_command("help")

  async def on_ready(self):
    await self.wait_until_ready()
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        await self.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename}")
    if not self.synced:
      synced = await self.tree.sync()
      print(f"synced {len(synced)} commands")
      self.synced = True

client = aclient()

@client.tree.command(description="Test command")
async def nigggwe(interaction: discord.Interaction, name: str):
  await interaction.response.send_message(f"Hi {name}")

keep_alive()
#try:
client.run(TOKEN)
#except:
  #os.system("kill 1")
