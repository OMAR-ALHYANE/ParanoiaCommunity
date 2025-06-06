"""
Main Discord Bot Implementation
Handles server statistics gathering and dashboard updates
"""

import discord
from discord.ext import tasks
import asyncio
import logging
from typing import Optional
from config import Config
from dashboard import DashboardCreator
from utils import BotUtils

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ParanoiaBot(discord.Client):
    """Main bot class for Paranoia Community Statistics"""
    
    def __init__(self, config: Config):
        # Set up intents
        intents = discord.Intents.default()
        for intent_name, enabled in config.intents_config.items():
            setattr(intents, intent_name, enabled)
        
        super().__init__(intents=intents)
        
        self.config = config
        self.dashboard = DashboardCreator(config)
        self.utils = BotUtils()
        self.target_channel: Optional[discord.TextChannel] = None
        self.dashboard_message: Optional[discord.Message] = None
        self.is_ready = False
        
    async def on_ready(self):
        """Called when the bot is ready and connected"""
        logger.info(f"🤖 Bot logged in as {self.user} (ID: {self.user.id})")
        
        # Find target channel
        channel = self.get_channel(self.config.channel_id)
        if not channel:
            logger.error(f"❌ Could not find channel with ID: {self.config.channel_id}")
            await self.close()
            return
        
        if not isinstance(channel, discord.TextChannel):
            logger.error(f"❌ Channel {self.config.channel_id} is not a text channel")
            await self.close()
            return
        
        self.target_channel = channel
        logger.info(f"📋 Target channel found: #{channel.name} in {channel.guild.name}")
        
        # Check permissions
        permissions = channel.permissions_for(channel.guild.me)
        required_perms = ['send_messages', 'embed_links', 'read_message_history']
        missing_perms = [perm for perm in required_perms if not getattr(permissions, perm)]
        
        if missing_perms:
            logger.error(f"❌ Missing permissions: {', '.join(missing_perms)}")
            await self.close()
            return
        
        logger.info("✅ All required permissions granted")
        
        # Start the dashboard update task
        if not self.dashboard_update_task.is_running():
            self.dashboard_update_task.start()
            logger.info("🔄 Dashboard update task started")
        
        self.is_ready = True
        logger.info("🚀 Bot is fully operational!")
    
    async def on_error(self, event, *args, **kwargs):
        """Handle errors"""
        logger.error(f"❌ Error in event {event}: {args}")
    
    @tasks.loop(seconds=60)  # Update every minute
    async def dashboard_update_task(self):
        """Main task that updates the dashboard every minute"""
        if not self.is_ready or not self.target_channel:
            return
        
        try:
            guild = self.target_channel.guild
            logger.info(f"🔄 Updating dashboard for {guild.name}")
            
            # Create new dashboard embed
            embed = self.dashboard.create_embed(guild)
            
            if self.dashboard_message is None:
                # Send new message if none exists
                self.dashboard_message = await self.target_channel.send(embed=embed)
                logger.info("📤 New dashboard message sent")
            else:
                try:
                    # Try to edit existing message
                    await self.dashboard_message.edit(embed=embed)
                    logger.info("✏️  Dashboard message updated")
                except discord.NotFound:
                    # Message was deleted, send a new one
                    self.dashboard_message = await self.target_channel.send(embed=embed)
                    logger.info("📤 Dashboard message recreated (original was deleted)")
                except discord.HTTPException as e:
                    logger.warning(f"⚠️  Could not edit message: {e}")
                    # Try sending a new message as fallback
                    self.dashboard_message = await self.target_channel.send(embed=embed)
                    logger.info("📤 New dashboard message sent as fallback")
        
        except discord.Forbidden:
            logger.error("❌ Missing permissions to send/edit messages")
            self.dashboard_update_task.stop()
        except discord.HTTPException as e:
            logger.error(f"❌ HTTP error during dashboard update: {e}")
        except Exception as e:
            logger.error(f"❌ Unexpected error during dashboard update: {e}")
            # Send error embed
            try:
                error_embed = self.dashboard.create_error_embed(str(e))
                await self.target_channel.send(embed=error_embed)
            except:
                pass  # Ignore errors when sending error message
    
    @dashboard_update_task.before_loop
    async def before_dashboard_update(self):
        """Wait until bot is ready before starting the task"""
        await self.wait_until_ready()
        # Wait a bit more to ensure everything is properly initialized
        await asyncio.sleep(2)
    
    async def on_member_join(self, member):
        """Handle member join events"""
        logger.info(f"👋 Member joined: {member.name}")
        # Trigger immediate update when member count changes
        if self.dashboard_update_task.is_running():
            self.dashboard_update_task.restart()
    
    async def on_member_remove(self, member):
        """Handle member leave events"""
        logger.info(f"👋 Member left: {member.name}")
        # Trigger immediate update when member count changes
        if self.dashboard_update_task.is_running():
            self.dashboard_update_task.restart()
    
    async def on_voice_state_update(self, member, before, after):
        """Handle voice state changes"""
        # Only update if someone joins or leaves voice (not just mute/deafen)
        if (before.channel is None) != (after.channel is None):
            logger.info(f"🎙️  Voice state change: {member.name}")
            # Small delay to avoid too frequent updates
            await asyncio.sleep(5)
            if self.dashboard_update_task.is_running():
                self.dashboard_update_task.restart()
    
    async def on_member_update(self, before, after):
        """Handle member status updates"""
        # Only update if status changed
        if before.status != after.status:
            logger.debug(f"📊 Status change: {after.name} - {before.status} → {after.status}")
            # Don't restart task for every status change to avoid rate limits
            # The regular 1-minute update will catch these changes
    
    async def close(self):
        """Clean shutdown"""
        logger.info("🛑 Bot shutting down...")
        if self.dashboard_update_task.is_running():
            self.dashboard_update_task.stop()
        await super().close()
