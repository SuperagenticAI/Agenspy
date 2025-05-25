"""Multi-protocol agent supporting multiple communication protocols."""  
  
import dspy  
from typing import Dict, Any, List, Optional  
from ..protocols.base import BaseProtocol, ProtocolType  
from ..protocols.mcp.client import MCPClient, RealMCPClient  
from ..protocols.agent2agent.client import Agent2AgentClient  
  
class MultiProtocolAgent(dspy.Module):  
    """Agent that can use multiple protocols simultaneously."""  
      
    def __init__(self, agent_id: str = "multi-agent"):  
        super().__init__()  
        self.agent_id = agent_id  
        self.protocols: Dict[ProtocolType, BaseProtocol] = {}  
          
        # DSPy reasoning modules  
        self.route_request = dspy.ChainOfThought(  
            "request: str, available_protocols: list[str] -> best_protocol: str, reasoning: str"  
        )  
          
        self.synthesize_responses = dspy.ChainOfThought(  
            "responses: list[str], protocols_used: list[str] -> final_answer: str, confidence: float"  
        )  
      
    def add_protocol(self, protocol: BaseProtocol):  
        """Add a protocol to the agent."""  
        self.protocols[protocol.protocol_type] = protocol  
        print(f"✅ Added {protocol.protocol_type.value} protocol")  
      
    def forward(self, request: str, use_all_protocols: bool = False):  
        """Process request using appropriate protocol(s)."""  
        print(f"\n🤖 Multi-Protocol Agent processing: {request}")  
        print("-" * 50)  
          
        available_protocols = [p.value for p in self.protocols.keys()]  
          
        if use_all_protocols:  
            # Use all available protocols  
            responses = []  
            protocols_used = []  
              
            for protocol_type, protocol in self.protocols.items():  
                print(f"📡 Using {protocol_type.value} protocol...")  
                response = protocol(context_request=request)  
                responses.append(response.context_data if hasattr(response, 'context_data') else str(response))  
                protocols_used.append(protocol_type.value)  
              
            # Synthesize responses  
            synthesis = self.synthesize_responses(  
                responses=responses,  
                protocols_used=protocols_used  
            )  
              
            return dspy.Prediction(  
                final_answer=synthesis.final_answer,  
                confidence=synthesis.confidence,  
                protocols_used=protocols_used,  
                individual_responses=responses  
            )  
          
        else:  
            # Route to best protocol  
            routing = self.route_request(  
                request=request,  
                available_protocols=available_protocols  
            )  
              
            best_protocol_name = routing.best_protocol  
            best_protocol = None  
              
            # Find the protocol  
            for protocol_type, protocol in self.protocols.items():  
                if protocol_type.value == best_protocol_name:  
                    best_protocol = protocol  
                    break  
              
            if best_protocol:  
                print(f"🎯 Routing to {best_protocol_name} protocol")  
                response = best_protocol(context_request=request)  
                  
                return dspy.Prediction(  
                    final_answer=response.context_data if hasattr(response, 'context_data') else str(response),  
                    protocol_used=best_protocol_name,  
                    routing_reasoning=routing.reasoning,  
                    capabilities=best_protocol.get_capabilities()  
                )  
            else:  
                return dspy.Prediction(  
                    final_answer="No suitable protocol found",  
                    protocol_used="none",  
                    error="Protocol routing failed"  
                )  
      
    def get_all_capabilities(self) -> Dict[str, Any]:  
        """Get capabilities from all protocols."""  
        capabilities = {}  
        for protocol_type, protocol in self.protocols.items():  
            capabilities[protocol_type.value] = protocol.get_capabilities()  
        return capabilities  
      
    def cleanup(self):  
        """Clean up all protocol connections."""  
        for protocol in self.protocols.values():  
            protocol.disconnect()