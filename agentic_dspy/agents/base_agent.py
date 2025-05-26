"""Base agent class for Agentic-DSPy."""

from abc import abstractmethod
from typing import Any, Dict, List, Optional

import dspy

from ..protocols.base import BaseProtocol


class BaseAgent(dspy.Module):
    """Base class for all agents in Agentic-DSPy."""

    def __init__(self, agent_id: str, **kwargs):
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.protocols: List[BaseProtocol] = []
        self.metadata = {}

    def add_protocol(self, protocol: BaseProtocol):
        """Add a protocol to the agent."""
        self.protocols.append(protocol)

    def get_protocol_by_type(self, protocol_type: str) -> Optional[BaseProtocol]:
        """Get protocol by type."""
        for protocol in self.protocols:
            if protocol.protocol_type.value == protocol_type:
                return protocol
        return None

    @abstractmethod
    def forward(self, **kwargs) -> dspy.Prediction:
        """Process agent request."""
        pass

    def get_agent_info(self) -> Dict[str, Any]:
        """Get agent information."""
        return {
            "agent_id": self.agent_id,
            "protocols": [p.protocol_type.value for p in self.protocols],
            "metadata": self.metadata,
        }

    def cleanup(self):
        """Clean up agent resources."""
        for protocol in self.protocols:
            protocol.disconnect()
