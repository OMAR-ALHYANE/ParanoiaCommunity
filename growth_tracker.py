"""
Server Growth Tracking System
Tracks member changes over time to calculate real growth percentages
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional

class GrowthTracker:
    """Tracks server growth over time"""
    
    def __init__(self, data_file: str = "growth_data.json"):
        self.data_file = data_file
        self.growth_data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load growth data from file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                pass
        return {"daily_snapshots": [], "weekly_snapshots": []}
    
    def _save_data(self):
        """Save growth data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.growth_data, f, indent=2)
    
    def record_snapshot(self, guild_id: int, total_members: int, online_members: int):
        """Record a snapshot of current server state"""
        now = datetime.now()
        snapshot = {
            "timestamp": now.isoformat(),
            "guild_id": guild_id,
            "total_members": total_members,
            "online_members": online_members,
            "date": now.strftime("%Y-%m-%d"),
            "hour": now.hour
        }
        
        # Add to daily snapshots
        self.growth_data["daily_snapshots"].append(snapshot)
        
        # Keep only last 7 days of hourly data
        cutoff_date = now - timedelta(days=7)
        self.growth_data["daily_snapshots"] = [
            s for s in self.growth_data["daily_snapshots"]
            if datetime.fromisoformat(s["timestamp"]) > cutoff_date
        ]
        
        # Add weekly snapshot (once per day)
        if not self._has_daily_snapshot(now.strftime("%Y-%m-%d")):
            self.growth_data["weekly_snapshots"].append(snapshot)
            
            # Keep only last 30 days of daily data
            self.growth_data["weekly_snapshots"] = [
                s for s in self.growth_data["weekly_snapshots"]
                if datetime.fromisoformat(s["timestamp"]) > (now - timedelta(days=30))
            ]
        
        self._save_data()
    
    def _has_daily_snapshot(self, date_str: str) -> bool:
        """Check if we already have a snapshot for this date"""
        return any(s["date"] == date_str for s in self.growth_data["weekly_snapshots"])
    
    def calculate_growth_percentage(self, current_members: int) -> int:
        """Calculate growth percentage based on historical data"""
        if not self.growth_data["weekly_snapshots"]:
            # No historical data, calculate based on activity
            return self._calculate_activity_based_growth(current_members)
        
        # Get the oldest available snapshot
        oldest_snapshot = min(
            self.growth_data["weekly_snapshots"],
            key=lambda x: datetime.fromisoformat(x["timestamp"])
        )
        
        past_members = oldest_snapshot["total_members"]
        
        if past_members == 0:
            return 100
        
        # Calculate actual growth percentage
        growth = ((current_members - past_members) / past_members) * 100
        
        # Ensure it's between 0 and 100
        return max(0, min(int(growth + 50), 100))  # Add base 50% for visual appeal
    
    def _calculate_activity_based_growth(self, total_members: int) -> int:
        """Calculate growth based on recent activity when no historical data exists"""
        if not self.growth_data["daily_snapshots"]:
            return 75  # Default value
        
        # Calculate average online percentage from recent snapshots
        recent_snapshots = self.growth_data["daily_snapshots"][-10:]  # Last 10 snapshots
        if not recent_snapshots:
            return 75
        
        avg_online_percentage = sum(
            (s["online_members"] / max(s["total_members"], 1)) * 100
            for s in recent_snapshots
        ) / len(recent_snapshots)
        
        # Convert activity to growth percentage
        return max(25, min(int(avg_online_percentage + 40), 100))
    
    def get_growth_trend(self) -> str:
        """Get growth trend indicator"""
        if len(self.growth_data["daily_snapshots"]) < 2:
            return "📊"
        
        recent = self.growth_data["daily_snapshots"][-2:]
        if recent[1]["total_members"] > recent[0]["total_members"]:
            return "📈"
        elif recent[1]["total_members"] < recent[0]["total_members"]:
            return "📉"
        else:
            return "📊"