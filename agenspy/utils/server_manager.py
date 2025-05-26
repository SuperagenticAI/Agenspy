"""Server management utilities."""

import subprocess
import threading
import time
from typing import Dict, List, Optional


class ServerManager:
    """Manages background server processes."""

    def __init__(self):
        self.servers: Dict[str, subprocess.Popen] = {}
        self.server_threads: Dict[str, threading.Thread] = {}

    def start_server(self, server_id: str, command: List[str], wait_time: int = 3) -> bool:
        """Start a server process in the background."""
        try:
            print(f"🚀 Starting server {server_id}: {' '.join(command)}")

            process = subprocess.Popen(
                command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=0
            )

            # Wait for server to start
            time.sleep(wait_time)

            if process.poll() is None:
                self.servers[server_id] = process
                print(f"✅ Server {server_id} started successfully")
                return True
            else:
                print(f"❌ Server {server_id} failed to start")
                return False

        except Exception as e:
            print(f"❌ Failed to start server {server_id}: {e}")
            return False

    def stop_server(self, server_id: str) -> bool:
        """Stop a server process."""
        if server_id not in self.servers:
            print(f"⚠️ Server {server_id} not found")
            return False

        try:
            process = self.servers[server_id]
            process.terminate()
            process.wait(timeout=5)
            del self.servers[server_id]
            print(f"🛑 Server {server_id} stopped")
            return True
        except subprocess.TimeoutExpired:
            process.kill()
            del self.servers[server_id]
            print(f"🛑 Server {server_id} force killed")
            return True
        except Exception as e:
            print(f"⚠️ Error stopping server {server_id}: {e}")
            return False

    def stop_all_servers(self):
        """Stop all managed servers."""
        server_ids = list(self.servers.keys())
        for server_id in server_ids:
            self.stop_server(server_id)

    def get_server_status(self, server_id: str) -> Optional[str]:
        """Get server status."""
        if server_id not in self.servers:
            return "not_found"

        process = self.servers[server_id]
        if process.poll() is None:
            return "running"
        else:
            return "stopped"

    def list_servers(self) -> List[str]:
        """List all managed servers."""
        return list(self.servers.keys())


# Global server manager instance
server_manager = ServerManager()
