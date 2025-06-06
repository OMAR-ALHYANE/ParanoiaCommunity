#!/usr/bin/env python3
"""
Test bot using the correct channel ID directly
"""

import asyncio
import os
import sys
from bot import ParanoiaBot
from config import Config

def main():
    """Test bot with correct channel ID"""
    try:
        # Get Discord bot token from environment variables
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            print("❌ Error: DISCORD_BOT_TOKEN environment variable not set!")
            sys.exit(1)
        
        # Get channel ID from environment or use default
        channel_id_env = os.getenv("DISCORD_CHANNEL_ID")
        if channel_id_env:
            try:
                channel_id = int(channel_id_env.strip().strip('"').strip("'"))
            except ValueError:
                # Fall back to known working channel
                channel_id = 1336118162151833742
        else:
            # Use the correct channel ID for #general in RIMBO WORLD's server
            channel_id = 1336118162151833742
        
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