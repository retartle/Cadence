import discord
import json
from discord.ext import commands
from discord import app_commands

from yt_dlp import YoutubeDL

emcolor = 0x000000

class music_cog(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
    
      self.is_playing = False
      self.loop = False

      self.music_queue = []
      self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True', 'audio-format':'mp3', 'geo-bypass':'True', 'audio-quality':'0'}
      self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

      self.vc = ""

    def search_yt(self, item):
      with YoutubeDL(self.YDL_OPTIONS) as ydl:
        try: 
          info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
        except Exception: 
          return False

        return {'source': info['url'], 'title': info['title'],'thumbnail': info['thumbnail'],'url': info['webpage_url'],'uploader': info['uploader'],'views': info['view_count'],'duration': info['duration']}

    def play_next(self):
      if len(self.music_queue) > 0:
        self.is_playing = True

        m_url = self.music_queue[0][0]['source']
        name = self.music_queue[0][0]['title']

        if not self.loop:
          self.music_queue.pop(0)

        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        update(name)
      else:
        self.is_playing = False
        name = "*Nothing is playing right now! Do `-play` to start playing a song!*"
        update(name)

    async def play_music(self):
      if len(self.music_queue) > 0:
        self.is_playing = True

        m_url = self.music_queue[0][0]['source']
        name = self.music_queue[0][0]['title']

        if self.vc == "" or not self.vc.is_connected() or self.vc == None:
          self.vc = await self.music_queue[0][1].connect()
        else:
          await self.vc.move_to(self.music_queue[0][1])
          
        if not self.loop:
          self.music_queue.pop(0)

        self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        update(name)
        return(name)
      else:
        self.is_playing = False
        name = "*Nothing is playing right now! Do `-play` to start playing a song!*"
        update(name)
        
    @app_commands.command(description="Plays a selected song from youtube")
    async def play(self, interaction: discord.Interaction, query: str):
      query = " ".join(query)
        
      voice_channel = interaction.user.voice
      if voice_channel is None:
        e = discord.Embed(title="Error",description="Join a voice channel",color=0xFF0000)
        await interaction.response.send_message(embed=e)
        return
      else:
        test = await interaction.response.send_message("Give me a sec..")
        voice_channel = voice_channel.channel
        #async with interaction.channel.typing():
        song = self.search_yt(query)
        if not song:
          await interaction.edit_original_response(content="Error. Please Try again")
          return
        thumbnail = song['thumbnail']
        uploader = song['uploader']
        views = song['views']
        duration = song['duration']
        url = song['url']
        if type(song) == type(True):
          e = discord.Embed(title="Error",description="An Error occured while looking for that song. Please try again. [Playlists and Livestreams not supported]",color=0xFF0000)
          await interaction.edit_original_response(content="Complete.",embed=e)
        else:
          if self.is_playing is False:
            
            e = discord.Embed(title="Now Playing:",description=f"[{song['title']}]({url})",color=0x00FF00)
            e.add_field(name="Uploader",value=uploader)
            e.add_field(name="Duration",value=duration)
            e.add_field(name="Views", value=f"`{views}`", inline=False)
            e.set_thumbnail(url=thumbnail)
            e.set_author(name=interaction.user,icon_url=interaction.user.avatar.url)
            await interaction.edit_original_response(content="Complete.",embed=e)
          else:
            e = discord.Embed(title="Added to queue:",description=f"[{song['title']}]({url})",color=0x800080)
            e.add_field(name="Uploader",value=uploader)
            e.add_field(name="Duration",value=duration)
            e.add_field(name="Views", value=f"`{views}`", inline=False)
            e.set_thumbnail(url=thumbnail)
            e.set_author(name=interaction.user,icon_url=interaction.user.avatar.url)
            await interaction.edit_original_response(content="Complete.",embed=e)
          self.music_queue.append([song, voice_channel])
                
          if self.is_playing == False:
            await self.play_music()
            
    @app_commands.command(description="Plays a preset playlist on idle")
    async def idle(self, interaction=discord.Interaction):
      query = [
        'darling in the franxx ed',
        'blend s op full',
        'Shiny Happy Days Nekopara',
        'putin summons comrade elmo',
        'chugjug with you',
        'BEST ANIME OPENINGS AND ENDINGS COMPILATION [FULL SONGS]']

      await interaction.response.send_message("Give me a sec..")
      
      voice_channel = interaction.user.voice
      if voice_channel is None:
        e = discord.Embed(title="Error",description="Join a voice channel",color=0xFF0000)
        await interaction.edit_original_response(embed=e, content="Complete.")
        return
      else:
        voice_channel = voice_channel.channel
        for i in query:
          song = self.search_yt(i)
          if type(song) == type(True):
            await interaction.edit_original_response("An Error occured while getting preset playlist. Please try again.")
          else:
            if self.is_playing is False:
              e = discord.Embed(title="Idle Mode",description=f"{song['title']}",color=0x00FF00)
              await interaction.edit_original_response(embed=e, content="Complete.")
            else:
              e = discord.Embed(title="Idle Mode Queuing, Please wait",description=f"{song['title']}",color=0x800080)
              await interaction.edit_original_response(embed=e, content="Queueing.")
            self.music_queue.append([song, voice_channel])
                
            if self.is_playing == False:
              await self.play_music()

    @app_commands.command(description="Displays the current songs in queue")
    async def queue(self, interaction=discord.Interaction):
      retval = ""
      for i in range(0, len(self.music_queue)):
        retval += f"{i+1}. `{self.music_queue[i][0]['title']}`\n"
        e = discord.Embed(title="Queued Songs",description=retval)

      if retval != "":
        await interaction.response.send_message(embed=e)
      else:
        e = discord.Embed(title="Empty queue",description="Do `-play [query]` to start playing / add to queue",color=0x800080)
        await interaction.response.send_message(embed=e)

    @app_commands.command(description="Skips the current song being played")
    async def skip(self, interaction=discord.Interaction):
      if self.vc != "" and self.vc:
        self.vc.stop()
        name = await self.play_music()
        if name is None:
          e = discord.Embed(title="Skipped",description=f"End of Queue",color=0xFFFF00)
          await interaction.response.send_message(embed=e)
        else:
          e = discord.Embed(title="Skipped",description=f"**Now playing:** {name}",color=0xFFFF00)
          await interaction.response.send_message(embed=e)
            
    @app_commands.command(description="Pauses the current song being played")
    async def pause(self, interaction=discord.Interaction):
      server = interaction.guild
      voice_channel = server.voice_client
    
      voice_channel.pause()
      e = discord.Embed(title="Paused",color=0xFFFF00)
      await interaction.response.send_message(embed=e)
    
    @app_commands.command(description="Resumes the current song being played")
    async def resume(self, interaction=discord.Interaction):
      server = interaction.guild
      voice_channel = server.voice_client
    
      voice_channel.resume()
      e = discord.Embed(title="Resuming",color=0x00FF00)
      await interaction.response.send_message(embed=e)
      
    @app_commands.command(description='Stops the music and disconnects the bot')
    async def stop(self, interaction=discord.Interaction):
      voice_client = interaction.guild.voice_client
    
      if voice_client == None:
        await interaction.response.send_message("There is nothing playing right now.")
      
      elif interaction.user.voice == None:
        await interaction.response.send_message("You are not connected to a voice channel!")
      
      else:
        server = interaction.guild
        voice_channel = server.voice_client
        voice_channel.stop()
        await voice_client.disconnect()
        self.is_playing = False
        self.music_queue = []
        name = "*Nothing is playing right now! Do `-play` to start playing a song!*"
        update(name)
        e = discord.Embed(title="Queue Cleared + Disconnected.",color=0x800080)
        await interaction.response.send_message(embed=e)
        
    @app_commands.command(description="Shows current playing song")
    async def nowplaying(self,interaction=discord.Interaction):
      with open("database/current.py", "r") as f:
        name = json.load(f)
      if self.is_playing == False:
        em = 0xFF0000
        status = "Currently Not Playing"
      else:
        em = 0x00FF00
        status = "Currently Playing"
      e = discord.Embed(title=status,description=name[0],color=em)
      await interaction.response.send_message(embed=e)
      
    @app_commands.command(description="Loops the current playing song")
    async def loop(self, interaction=discord.Interaction):
      if interaction.user.voice == None:
        await interaction.response.send_message("You are not connected to a voice channel!")
        return
      if not self.loop:
        self.loop = True
        e = discord.Embed(title="Enabled Loop",description="Looping **next** track (Really, Really fucking buggy)",color=0x00FF00)
        await interaction.response.send_message(embed=e)
      else:
        self.loop = False
        try:
          self.music_queue.pop(0)
        except:
          print("lol")
        e = discord.Embed(title="Disabled Loop",color=0xFF0000)
        await interaction.response.send_message(embed=e)
      
def update(name):
  if '"' in name or "'" in name:
    name = "`An Error occured while loading song title.`"
  with open('database/current.py', "w") as f:
    f.write(f'["{name}"]')
    
async def setup(client):
  await client.add_cog(music_cog(client))