"""
⚠️ MOCK IMPLEMENTATION: Agent2Agent Protocol Client

This is a mock implementation of the Agent2Agent protocol for demonstration purposes only.
For the actual implementation, you'll need to integrate with the official Google A2A project:
https://github.com/google/A2A
"""

import warnings
from typing import Any, Dict

from ..base import BaseProtocol, ProtocolType


class Agent2AgentClient(BaseProtocol):
    """
    ⚠️ MOCK IMPLEMENTATION: Agent2Agent Protocol Client

    This is a mock implementation for demonstration and testing purposes only.
    For production use, you'll need to implement the actual protocol using the
    official Google A2A project: https://github.com/google/A2A
    """

    def __init__(self, peer_address: str, agent_id: str, **kwargs):
        warnings.warn(
            "⚠️ Using MOCK implementation of Agent2Agent protocol. "
            "For production use, integrate with the official Google A2A project: "
            "https://github.com/google/A2A",
            UserWarning,
            stacklevel=2,
        )
        protocol_config = {
            "type": ProtocolType.AGENT2AGENT,
            "peer_address": peer_address,
            "agent_id": agent_id,
            "status": "mock_implementation",
        }
        super().__init__(protocol_config, **kwargs)
        self.peer_address = peer_address
        self.agent_id = agent_id
        self.peers = {}
        self._connected = False

    def connect(self) -> bool:
        """Mock implementation of Agent2Agent connection."""
        print("⚠️  Using MOCK Agent2Agent implementation - not a real connection")
        print(f"🤝 [MOCK] Connecting to Agent2Agent network: {self.peer_address}")
        self._connected = True
        print(f"✅ [MOCK] A2A Connected! Agent ID: {self.agent_id}")
        return True

    def send_message(self, recipient_id: str, message: Dict[str, Any]) -> bool:
        """Mock implementation of message sending."""
        print(f"� [MOCK] Sending message to {recipient_id}: {message}")
        return True

    def broadcast(self, message: Dict[str, Any]) -> bool:
        """Mock implementation of broadcast message."""
        print(f"📢 [MOCK] Broadcasting message: {message}")
        return True

    def disconnect(self) -> bool:
        """Mock implementation of disconnection."""
        print("👋 [MOCK] Disconnecting from Agent2Agent network")
        self._connected = False
        return True
