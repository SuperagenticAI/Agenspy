"""Tests for base protocol functionality."""

import dspy
import pytest

from agentic_dspy.protocols.base import BaseProtocol, ProtocolType


class MockProtocol(BaseProtocol):
    """Mock protocol for testing."""

    def __init__(self, **kwargs):
        super().__init__({"type": ProtocolType.CUSTOM}, **kwargs)
        self.connected = False

    def connect(self) -> bool:
        self.connected = True
        self._connected = True
        return True

    def disconnect(self) -> None:
        self.connected = False
        self._connected = False

    def get_capabilities(self) -> dict:
        return {"test": True}

    def discover_peers(self) -> list:
        return ["peer1", "peer2"]

    def _handle_request(self, **kwargs) -> dspy.Prediction:
        return dspy.Prediction(result="test_result")


class TestBaseProtocol:
    """Test cases for BaseProtocol."""

    def test_protocol_initialization(self):
        """Test protocol initialization."""
        protocol = MockProtocol()
        assert protocol.protocol_type == ProtocolType.CUSTOM
        assert not protocol._connected

    def test_connect_disconnect(self):
        """Test connection lifecycle."""
        protocol = MockProtocol()

        # Test connection
        assert protocol.connect()
        assert protocol._connected
        assert protocol.connected

        # Test disconnection
        protocol.disconnect()
        assert not protocol._connected
        assert not protocol.connected

    def test_capabilities(self):
        """Test capability discovery."""
        protocol = MockProtocol()
        capabilities = protocol.get_capabilities()
        assert capabilities["test"] is True

    def test_peer_discovery(self):
        """Test peer discovery."""
        protocol = MockProtocol()
        peers = protocol.discover_peers()
        assert "peer1" in peers
        assert "peer2" in peers

    def test_forward_auto_connect(self):
        """Test automatic connection on forward."""
        protocol = MockProtocol()
        assert not protocol._connected

        result = protocol(test_param="value")
        assert protocol._connected
        assert result.result == "test_result"

    def test_protocol_info(self):
        """Test protocol metadata."""
        protocol = MockProtocol()
        info = protocol.get_protocol_info()

        assert info["type"] == "custom"
        assert info["connected"] is False
        assert "capabilities" in info
        assert "config" in info


if __name__ == "__main__":
    pytest.main([__file__])
