"""
Configuration settings for the Paranoia Community Bot
"""

import os
from typing import Optional

class Config:
    """Configuration class for bot settings"""
    
    def __init__(self, bot_token: str, channel_id: int):
        self.bot_token = bot_token
        self.channel_id = channel_id
        
        # Bot settings
        self.bot_name = "Paranoia Community Bot"
        self.update_interval = 60  # seconds
        self.progress_percentage = 75  # Fixed progress percentage
        
        # Modern 2025 color scheme - Clean & Contemporary
        self.embed_colors = {
            'primary': 0x5865F2,      # Discord Blurple
            'secondary': 0x2B2D31,    # Discord Dark Gray
            'accent': 0x00D9FF,       # Modern Cyan
            'success': 0x23A55A,      # Modern Green
            'warning': 0xF0B132,      # Modern Yellow
            'gradient_start': 0x5865F2, # Discord Blurple
            'gradient_end': 0x00D9FF   # Modern Cyan
        }
        
        # Progress bar settings - Cyberpunk style
        self.progress_bar_length = 20
        self.progress_filled_char = "▰"
        self.progress_empty_char = "▱"
        
        # Message settings
        self.message_title = "Paranoia Community Update"
        self.footer_text = "Live Server Dashboard • Updates every minute"
        
        # Bot intents (required for member and presence data)
        self.intents_config = {
            'guilds': True,
            'members': True,
            'presences': True,
            'voice_states': True,
            'guild_messages': True,
            'message_content': True
        }
    
    def get_progress_bar(self, percentage: Optional[int] = None) -> str:
        """Generate a progress bar string"""
        if percentage is None:
            percentage = self.progress_percentage
            
        filled_length = int(self.progress_bar_length * percentage / 100)
        empty_length = self.progress_bar_length - filled_length
        
        progress_bar = (
            self.progress_filled_char * filled_length + 
            self.progress_empty_char * empty_length
        )
        
        return f"{progress_bar} {percentage}%"
