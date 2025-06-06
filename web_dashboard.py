"""
Web dashboard for the Discord bot
Provides a public interface to view bot status and statistics
"""
from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime
import asyncio
import discord
from threading import Thread
import time

app = Flask(__name__)

def get_bot_data():
    """Get current bot data from growth tracker"""
    try:
        if os.path.exists('growth_data.json'):
            with open('growth_data.json', 'r') as f:
                data = json.load(f)
                if data['daily_snapshots']:
                    latest = data['daily_snapshots'][-1]
                    return {
                        'status': 'online',
                        'total_members': latest['total_members'],
                        'online_members': latest['online_members'],
                        'last_update': latest['timestamp'],
                        'guild_id': latest['guild_id']
                    }
    except Exception as e:
        print(f"Error reading bot data: {e}")
    
    return {
        'status': 'offline',
        'total_members': 0,
        'online_members': 0,
        'last_update': None,
        'guild_id': None
    }

@app.route('/')
def dashboard():
    """Main dashboard page"""
    bot_data = get_bot_data()
    return render_template('dashboard.html', data=bot_data)

@app.route('/api/status')
def api_status():
    """API endpoint for bot status"""
    return jsonify(get_bot_data())

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    app.run(host='0.0.0.0', port=5000, debug=False)