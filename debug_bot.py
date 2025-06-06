#!/usr/bin/env python3
"""
Debug bot to show available servers and channels
"""

import discord
import os
import sys

def main():
    """Debug bot to list servers and channels"""
    bot_token = os.getenv("DISCORD_BOT_TOKEN")
    if not bot_token:
        print("❌ Error: DISCORD_BOT_TOKEN environment variable not set!")
        sys.exit(1)
    
    # Set up intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.presences = True
    intents.voice_states = True
    intents.guild_messages = True
    intents.message_content = True
    
    class DebugBot(discord.Client):
        async def on_ready(self):
            print(f"🤖 Bot logged in as {self.user}")
            print(f"📊 Bot is in {len(self.guilds)} server(s):")
            
            for guild in self.guilds:
                print(f"\n🏠 Server: {guild.name} (ID: {guild.id})")
                print(f"   👥 Members: {guild.member_count}")
                print(f"   📝 Text Channels:")
                
                for channel in guild.text_channels:
                    permissions = channel.permissions_for(guild.me)
                    can_send = permissions.send_messages and permissions.embed_links
                    status = "✅" if can_send else "❌"
                    print(f"      {status} #{channel.name} (ID: {channel.id})")
            
            if not self.guilds:
                print("\n❌ Bot is not in any servers!")
                print("   Please add the bot to your server using the OAuth2 URL:")
                print("   1. Go to https://discord.com/developers/applications")
                print("   2. Select your bot application")
                print("   3. Go to OAuth2 > URL Generator")
                print("   4. Select 'bot' scope")
                print("   5. Select permissions: Send Messages, Embed Links, Read Message History, View Channels")
                print("   6. Use the generated URL to add the bot to your server")
            
            await self.close()
    
    client = DebugBot(intents=intents)
    client.run(bot_token)

if __name__ == "__main__":
    main()