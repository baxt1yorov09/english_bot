import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cefr_bot.settings')
django.setup()

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'OK')
        else:
            self.send_response(404)
            self.end_headers()

def start_health_server():
    """Start simple HTTP server for health checks"""
    port = int(os.environ.get('PORT', 8000))
    
    # Find available port
    for i in range(port, port + 10):
        try:
            server = HTTPServer(('0.0.0.0', i), HealthCheckHandler)
            print(f"Health check server started on port {i}")
            server.serve_forever()
        except socket.error:
            continue
        break

def main():
    try:
        # Start health check server in background
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        
        # Give health server time to start
        time.sleep(2)
        
        # Run migrations
        execute_from_command_line(['manage.py', 'migrate'])
        
        # Start bot
        from bot import main as bot_main
        bot_main()
        
    except KeyboardInterrupt:
        print("Bot stopped by user")
    except Exception as e:
        print(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
