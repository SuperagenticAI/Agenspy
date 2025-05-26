"""Base protocol interface for Agenspy."""

from abc import abstractmethod
from enum import Enum
from typing import Any, Dict, List

import dspy


class ProtocolType(Enum):
    """Supported protocol types."""

    MCP = "mcp"
    AGENT2AGENT = "agent2agent"
    CUSTOM = "custom"


class BaseProtocol(dspy.Module):
    """Base class for all agent communication protocols.

    This class provides a standardized interface for integrating various
    agent communication protocols with DSPy's module system, enabling
    protocol-first agent development.
    """

    def __init__(self, protocol_config: Dict[str, Any], **kwargs):
        super().__init__(**kwargs)
        self.protocol_config = protocol_config
        self.protocol_type = protocol_config.get("type", ProtocolType.CUSTOM)
        self.connection_manager = None
        self._connected = False
        self._capabilities = {}

    @abstractmethod
    def connect(self) -> bool:
        """Establish protocol connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close protocol connection."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Get protocol capabilities and available tools."""
        pass

    @abstractmethod
    def discover_peers(self) -> List[str]:
        """Discover available peers/servers for this protocol."""
        pass

    def forward(self, **kwargs):
        """DSPy module forward method."""
        if not self._connected:
            self.connect()
        return self._handle_request(**kwargs)

    @abstractmethod
    def _handle_request(self, **kwargs) -> dspy.Prediction:
        """Handle protocol-specific requests."""
        pass

    def get_protocol_info(self) -> Dict[str, Any]:
        """Get protocol metadata and status."""
        return {
            "type": self.protocol_type.value,
            "connected": self._connected,
            "capabilities": self._capabilities,
            "config": self.protocol_config,
        }
