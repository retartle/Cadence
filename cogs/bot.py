import discord
import asyncio
import random
import psutil
import time
import datetime
from discord.ext import commands
from discord import app_commands
from version import version_
from psutil._common import bytes2human
from uptime import uptime

emcolor = 0x00000

class Bot_info(commands.Cog):
  
  def __init__(self, client):
    self.client = client
  
  @app_commands.command(description="Current Voice Chat ID")
  async def getvcid(self, interaction: discord.Interaction):
    try:
      await interaction.response.send_message(interaction.user.voice.channel.id)
    except:
      await interaction.response.send_message("Join VC")
    
  @app_commands.command(description="Sets the version of Cadence (Admin Only)")
  async def version(self, interaction: discord.Interaction, version: str):
    owner = [776991810744221716,831374308039065662,505213604023500810]
    
    if interaction.user.id in owner:
      with open('version.py', "w") as f:
        f.write(f'version_ = "{version}"')
      await interaction.response.send_message(f"Version set to `{version}`. Restart bot to apply changes immediately.")
      
    else:
      await interaction.response.send_message("You aren't a bot admin!")

  '''@app_commands.command()
  async def pushupdates(self, interaction: discord.Interaction):
    e = discord.Embed(title=f"V{version_}",description="-Slash commands *(half done)* and less downtime",color=0xFFC0CB)
    e.set_footer(text="Sponsored by Raid Shadow Legends")
    channel = self.client.get_channel(769470793583165460)
    channel2 = self.client.get_channel(862673712439361559)
    await channel2.send(embed=e)
    await channel.send(embed=e)'''
    
  @app_commands.command(description="Help command, probably pointless")
  async def help(self, interaction: discord.Interaction):
    e = discord.Embed(title="Commands",description="**Music commands**\n`play` - Plays/Queues music according to query\n`stop` - Disconnects bot from current vc\n`pause` - Pauses current song\n`resume` - Resumes current song\n`skip` - Skips current song and plays next song on the queue if there is any\n`queue` - Shows current queue if any\n`nowplaying` - Shows current song if any\n`loop` - Loops current track / The next track if not currently playing\n\n**General Commands**\n`updates` - Shows latest bot updates\n`help` - Shows this message\n`info` - Shows general info of bot\n`ping` - Shows bot latency and CPU usage\n`memory` - Shows bot memory usage")
    await interaction.response.send_message(embed=e)
    
  @app_commands.command(description="Bot information")
  async def info(self, interaction: discord.Interaction):
    owner = self.client.get_user(776991810744221716)
    id = self.client.user.id
    embed = discord.Embed(
      title=self.client.user.name,
      color=emcolor
      )
    embed.set_thumbnail(url=self.client.user.avatar.url)
    embed.add_field(name="Creator", value=f"`{owner}`", inline=True)
    embed.add_field(name="Bot ID", value=f"`{id}`", inline=True)
    embed.add_field(name="Prefix",value="`-` or Slash commands (Complete)",inline=False)
    embed.set_author(name=interaction.user.name, icon_url=str(interaction.user.avatar.url))

    await interaction.response.send_message(embed=embed)
    
  @app_commands.command(description="Bot Latency")
  async def ping(self, interaction: discord.Interaction):
    cpu = psutil.cpu_percent(interval=0.1)
    age = uptime()
    age = str(datetime.timedelta(seconds=age))

    if cpu > 80:
      cpu = f"{cpu}% High"
    else:
      cpu = f"{cpu}% Low"
      
    e=discord.Embed(title=f"{self.client.user.name} is online!",color=emcolor)
    e.add_field(name="Latency",value=f"{round(self.client.latency * 1000)}ms")
    e.add_field(name="CPU Usage",value=f"{cpu}")
    e.add_field(name="Online for",value=f"{age}")
    e.set_author(name=interaction.user.name,icon_url=interaction.user.avatar.url)
    e.set_thumbnail(url=self.client.user.avatar.url)
    await interaction.response.send_message(embed=e)

  @app_commands.command(description="Bot memory")
  async def memory(self, interaction: discord.Interaction):
    nt = psutil.virtual_memory()
    e = discord.Embed(title=f"{self.client.user.name}'s Memory",color=emcolor)
    e.set_thumbnail(url=self.client.user.avatar.url)
    e.set_author(name=f"{interaction.user.name}'s Request",icon_url=interaction.user.avatar.url)
    for name in nt._fields:
      value = getattr(nt, name)
      if name != 'percent':
        value = bytes2human(value)
        e.add_field(name=name.capitalize(),value=value)
        
    await interaction.response.send_message(embed=e)


async def setup(client):
  await client.add_cog(Bot_info(client))