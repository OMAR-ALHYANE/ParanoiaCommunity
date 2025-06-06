"""
Dashboard creation and formatting for the Discord bot
"""

import discord
from datetime import datetime
from typing import Dict, Any
from utils import BotUtils
from config import Config
from growth_tracker import GrowthTracker

class DashboardCreator:
    """Creates and formats the server dashboard embed"""
    
    def __init__(self, config: Config):
        self.config = config
        self.utils = BotUtils()
        self.growth_tracker = GrowthTracker()
    
    def create_embed(self, guild: discord.Guild) -> discord.Embed:
        """Create a comprehensive server statistics embed"""
        
        # Get all server statistics
        member_stats = self._get_member_statistics(guild)
        voice_stats = self._get_voice_statistics(guild)
        boost_stats = self._get_boost_statistics(guild)
        
        # Create modern embed with clean theme
        embed = discord.Embed(
            color=self.config.embed_colors['primary'],
            timestamp=datetime.now()
        )
        
        # Record current data and calculate real growth percentage
        self.growth_tracker.record_snapshot(guild.id, member_stats['total_members'], member_stats['online_members'])
        growth_percentage = self.growth_tracker.calculate_growth_percentage(member_stats['total_members'])
        growth_trend = self.growth_tracker.get_growth_trend()
        
        activity_indicator = "🔥" if member_stats['online_members'] > 5 else "⚡" if member_stats['online_members'] > 2 else "💤"
        embed.title = f"⚡ Paranoia Community Live Dashboard {activity_indicator}"
        embed.description = f"**{guild.name}** • Real-time metrics • {growth_percentage}% server growth {growth_trend}"
        
        # Add server thumbnail if available
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Create main dashboard content
        dashboard_content = self._create_dashboard_layout(member_stats, voice_stats, boost_stats)
        
        # Add the main dashboard as a single field for better layout
        embed.add_field(
            name="",
            value=dashboard_content,
            inline=False
        )
        
        # Enhanced footer with server status
        last_update = self.utils.format_timestamp()
        server_pulse = "🟢 Server Online" if member_stats['online_members'] > 0 else "🔴 Server Quiet"
        embed.set_footer(
            text=f"🕐 {last_update} • {server_pulse} • Auto-updates every 60s",
            icon_url=guild.icon.url if guild.icon else None
        )
        
        return embed
    
    def _create_dashboard_layout(self, member_stats: Dict, voice_stats: Dict, boost_stats: Dict) -> str:
        """Create enhanced dashboard with unique visual elements"""
        
        # Get status counts for the overview
        status_counts = member_stats['status_counts']
        
        # Dynamic visual indicators based on activity
        member_trend = "📈" if member_stats['online_members'] > member_stats['total_members'] * 0.5 else "📊"
        voice_indicator = "🔊" if voice_stats['members_in_voice'] > 0 else "🔇"
        boost_sparkle = "✨" if boost_stats['boost_count'] > 0 else "💫"
        
        # Enhanced layout with dynamic elements
        content = f"""💎 **│** Total Members: **{self.utils.format_number(member_stats['total_members'])}** {member_trend}

🌟 **│** Online Right Now: **{self.utils.format_number(member_stats['online_members'])}** 

{voice_indicator} **│** Active in Voice: **{self.utils.format_number(voice_stats['members_in_voice'])}** users

{boost_sparkle} **│** Server Boosts: **{self.utils.format_number(boost_stats['boost_count'])}** (Tier {boost_stats['boost_level']})

🚀 **│** Boosting Heroes: **{self.utils.format_number(boost_stats['boosters_count'])}** legends

```diff
+ Status Breakdown
```
🟢 Online: **{status_counts['online']}** • 🟡 Away: **{status_counts['idle']}** • 🔴 Busy: **{status_counts['dnd']}** • ⚫ Offline: **{status_counts['offline']}**"""
        
        return content
    
    def _get_boost_level_name(self, level: int) -> str:
        """Get formatted boost level name"""
        level_names = {0: "None", 1: "Level 1", 2: "Level 2", 3: "Level 3"}
        emoji = self.utils.get_boost_level_emoji(level)
        return f"{emoji} {level_names.get(level, f'Level {level}')}"
    
    def _get_voice_usage_indicator(self, voice_stats: Dict) -> str:
        """Get modern voice usage indicator"""
        usage = voice_stats['members_in_voice']
        if usage > 10:
            return "**Very Active**"
        elif usage > 3:
            return "**Active**"
        elif usage > 0:
            return "**Low**"
        else:
            return "**Quiet**"
    

    
    def _get_member_statistics(self, guild: discord.Guild) -> Dict[str, int]:
        """Get comprehensive member statistics"""
        total_members = len([m for m in guild.members if not m.bot])
        total_bots = len([m for m in guild.members if m.bot])
        status_counts = self.utils.get_member_status_counts(guild)
        
        return {
            'total_members': total_members,
            'total_bots': total_bots,
            'total_all': guild.member_count,
            'online_members': status_counts['total_online'],
            'status_counts': status_counts
        }
    
    def _get_voice_statistics(self, guild: discord.Guild) -> Dict[str, int]:
        """Get voice channel statistics"""
        voice_members = self.utils.get_voice_channel_count(guild)
        voice_channels = len(guild.voice_channels)
        active_voice_channels = len([vc for vc in guild.voice_channels if len(vc.members) > 0])
        
        return {
            'members_in_voice': voice_members,
            'total_voice_channels': voice_channels,
            'active_voice_channels': active_voice_channels
        }
    
    def _get_boost_statistics(self, guild: discord.Guild) -> Dict[str, Any]:
        """Get server boost statistics"""
        return self.utils.get_boost_info(guild)
    

    
    def create_error_embed(self, error_message: str) -> discord.Embed:
        """Create an error embed for when statistics can't be gathered"""
        embed = discord.Embed(
            title="⚠️ Dashboard Error",
            description=f"```\n{error_message}\n```",
            color=self.config.embed_colors['danger'],
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="🕒 Error Time",
            value=f"```\n{self.utils.format_timestamp()}\n```",
            inline=False
        )
        
        embed.set_footer(text="Dashboard will retry on next update cycle")
        
        return embed
