"""Protocol registry for managing available protocols."""

from typing import Dict, List, Type

from ..protocols.base import BaseProtocol, ProtocolType


class ProtocolRegistry:
    """Registry for managing protocol implementations."""

    def __init__(self):
        self._protocols: Dict[ProtocolType, Type[BaseProtocol]] = {}
        self._instances: Dict[str, BaseProtocol] = {}

    def register_protocol(self, protocol_type: ProtocolType, protocol_class: Type[BaseProtocol]):
        """Register a protocol implementation."""
        self._protocols[protocol_type] = protocol_class
        print(f"📝 Registered {protocol_type.value} protocol")

    def create_protocol(self, protocol_type: ProtocolType, **kwargs) -> BaseProtocol:
        """Create a protocol instance."""
        if protocol_type not in self._protocols:
            raise ValueError(f"Protocol {protocol_type.value} not registered")

        protocol_class = self._protocols[protocol_type]
        instance = protocol_class(**kwargs)

        instance_id = f"{protocol_type.value}_{id(instance)}"
        self._instances[instance_id] = instance

        return instance

    def get_available_protocols(self) -> List[ProtocolType]:
        """Get list of available protocol types."""
        return list(self._protocols.keys())

    def cleanup_all(self):
        """Cleanup all protocol instances."""
        for instance in self._instances.values():
            instance.disconnect()
        self._instances.clear()


# Global registry instance
registry = ProtocolRegistry()


# Register built-in protocols
def register_builtin_protocols():
    """Register built-in protocol implementations."""
    from ..protocols.agent2agent.client import Agent2AgentClient
    from ..protocols.mcp.client import MCPClient

    registry.register_protocol(ProtocolType.MCP, MCPClient)
    registry.register_protocol(ProtocolType.AGENT2AGENT, Agent2AgentClient)


# Auto-register on import
register_builtin_protocols()
