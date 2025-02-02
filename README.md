# Cadence 🎶 - A Discord Music Bot

Cadence is a powerful and lightweight Discord bot designed for seamless music playback using `yt-dlp`. With high-quality audio streaming and simple commands, Cadence makes listening to music with friends easier than ever!

## Features ✨
- 🎵 **YouTube & More** - Supports YouTube via `yt-dlp`
- 🔊 **High-Quality Audio** - Smooth, uninterrupted playback
- 🛠 **Easy to Use** - Simple commands for playing, pausing, and skipping tracks
- 🏃 **Lightweight & Fast** - Optimized for low-latency streaming

---

## Installation & Setup ⚙️
### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/cadence.git
cd cadence
```

### **2. Install Dependencies**
Ensure you have Python 3.8+ installed, then run:
```bash
pip install -r requirements.txt
```

You'll also need `ffmpeg` for audio processing. Install it via:
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **Linux:**
  ```bash
  sudo apt install ffmpeg
  ```
- **MacOS:**
  ```bash
  brew install ffmpeg
  ```

### **3. Set Up Environment Variables**
Create a `.env` file and add your Discord bot token:
```
DISCORD_TOKEN=your_token_here
```

### **4. Run the Bot**
```bash
python main.py
```

---

## Commands 🎼
| Command        | Description                           |
|---------------|--------------------------------------|
| `/play <url>` | Play a song from YouTube            |
| `/pause`      | Pause the current track             |
| `/resume`     | Resume playback                     |
| `/skip`       | Skip the current song               |
| `/stop`       | Stop playback and clear the queue   |
| `/queue`      | Show the current song queue         |
| `/disconnect` | Disconnect the bot from voice chat  |

---

## Troubleshooting 🛠
### **Bot Not Responding?**
- Ensure your bot is **online** in Discord.
- Check if your **bot token** is correct in `.env`.
- Verify that `ffmpeg` is installed and accessible.

### **Audio Issues?**
- Make sure `yt-dlp` is installed and updated:
  ```bash
  pip install -U yt-dlp
  ```
- Check that the bot has **permission** to connect and speak in the voice channel.
- Restart the bot if playback is stuck.

---

## Contributing 🤝
Want to improve Cadence? Feel free to fork the repo, submit issues, or contribute via pull requests!

```bash
git checkout -b feature-branch
```

---

## License 📜
This project is licensed under the MIT License.

---

## 🌟 Enjoy Cadence and happy listening! 🎶

