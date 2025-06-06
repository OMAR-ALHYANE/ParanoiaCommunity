#!/usr/bin/env python3
"""
Discord Bot Entry Point
Starts the Paranoia Community Statistics Bot
"""

import asyncio
import os
import sys
from bot import ParanoiaBot
from config import Config

def main():
    """Main entry point for the Discord bot"""
    try:
        # Get Discord bot token from environment variables
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            print("❌ Error: DISCORD_BOT_TOKEN environment variable not set!")
            print("Please set your Discord bot token in the environment variables.")
            sys.exit(1)
        
        # Get channel ID from environment variables
        channel_id = os.getenv("DISCORD_CHANNEL_ID")
        if not channel_id:
            print("❌ Error: DISCORD_CHANNEL_ID environment variable not set!")
            print("Please set the target channel ID in the environment variables.")
            sys.exit(1)
        
        # Clean up the channel ID (remove quotes, whitespace, etc.)
        channel_id = channel_id.strip().strip('"').strip("'")
        
        try:
            channel_id = int(channel_id)
        except ValueError:
            print(f"❌ Error: DISCORD_CHANNEL_ID must be a valid integer!")
            print(f"Current value: '{os.getenv('DISCORD_CHANNEL_ID')}'")
            print("Please ensure the channel ID contains only numbers (no quotes or spaces)")
            sys.exit(1)
        
        # Initialize configuration
        config = Config(bot_token, channel_id)
        
        # Create and run bot
        bot = ParanoiaBot(config)
        
        print("🚀 Starting Paranoia Community Statistics Bot...")
        print(f"📋 Target Channel ID: {channel_id}")
        print("⏱️  Update Interval: 1 minute")
        print("🔄 Bot is starting up...")
        
        # Run the bot
        bot.run(bot_token)
        
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
