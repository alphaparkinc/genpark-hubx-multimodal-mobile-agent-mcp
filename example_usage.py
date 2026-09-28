from client import HubXMultimodalMobileAgentMCP
import json

def test():
    agent = HubXMultimodalMobileAgentMCP()
    print("=== Testing HubX Multimodal Mobile Agent Native MCP ===")
    
    bench = agent.run_benchmark_multimodal_tools()
    print(json.dumps(bench, indent=2))

if __name__ == "__main__":
    test()
