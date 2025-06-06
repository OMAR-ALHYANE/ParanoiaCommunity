"""
Utility functions for the Discord bot
"""

from datetime import datetime
from typing import List, Dict, Any
import discord

class BotUtils:
    """Utility class for common bot operations"""
    
    @staticmethod
    def format_timestamp() -> str:
        """Format current timestamp as MM/DD/YYYY HH:MM AM/PM"""
        now = datetime.now()
        return now.strftime("%m/%d/%Y %I:%M %p")
    
    @staticmethod
    def format_number(number: int) -> str:
        """Format number with commas for readability"""
        return f"{number:,}"
    
    @staticmethod
    def get_member_status_counts(guild: discord.Guild) -> Dict[str, int]:
        """Get count of members by status"""
        status_counts = {
            'online': 0,
            'idle': 0,
            'dnd': 0,
            'offline': 0,
            'total_online': 0  # online + idle + dnd
        }
        
        for member in guild.members:
            if member.bot:
                continue  # Skip bots
                
            status = str(member.status)
            if status in status_counts:
                status_counts[status] += 1
            
            # Count as online if not offline
            if status != 'offline':
                status_counts['total_online'] += 1
        
        return status_counts
    
    @staticmethod
    def get_voice_channel_count(guild: discord.Guild) -> int:
        """Get count of members currently in voice channels"""
        voice_count = 0
        for channel in guild.voice_channels:
            voice_count += len([m for m in channel.members if not m.bot])
        return voice_count
    
    @staticmethod
    def get_boost_info(guild: discord.Guild) -> Dict[str, Any]:
        """Get server boost information"""
        return {
            'boost_count': guild.premium_subscription_count or 0,
            'boost_level': guild.premium_tier,
            'boosters_count': len(guild.premium_subscribers)
        }
    
    @staticmethod
    def create_status_indicator(status: str) -> str:
        """Create colored status indicator"""
        indicators = {
            'online': '🟢',
            'idle': '🟡',
            'dnd': '🔴',
            'offline': '⚫'
        }
        return indicators.get(status, '⚪')
    
    @staticmethod
    def get_boost_level_emoji(level: int) -> str:
        """Get emoji for boost level"""
        level_emojis = {
            0: '📈',
            1: '🚀',
            2: '⭐',
            3: '💎'
        }
        return level_emojis.get(level, '📈')
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 1024) -> str:
        """Truncate text to fit Discord embed limits"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
