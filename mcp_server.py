import sys, json
from client import HubXMultimodalMobileAgentMCP

def handle_mcp():
    agent = HubXMultimodalMobileAgentMCP()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(agent.run_benchmark_multimodal_tools(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-hubx-multimodal-mobile-agent-mcp", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "hubx_vision_diagnose", "description": "Execute botanical or nutrition visual diagnostics.", "inputSchema": {"type": "object", "properties": {"modality_task": {"type": "string"}, "image_payload": {"type": "object"}}}},
                    {"name": "hubx_speech_transcribe", "description": "Transcribe audio stream and distill action items.", "inputSchema": {"type": "object", "properties": {"audio_metadata": {"type": "object"}}}},
                    {"name": "hubx_multimodal_generate", "description": "Generate photorealistic portraits or spatial interior restyling concepts.", "inputSchema": {"type": "object", "properties": {"target_type": {"type": "string"}, "prompt_spec": {"type": "object"}}}},
                    {"name": "hubx_language_coach", "description": "Evaluate pronunciation and grammar in real-time dialogue.", "inputSchema": {"type": "object", "properties": {"spoken_transcript": {"type": "string"}}}},
                    {"name": "run_benchmark_multimodal_tools", "description": "Benchmark multimodal processing latency and accuracy.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "hubx_vision_diagnose":
                    res = agent.hubx_vision_diagnose(args.get("modality_task", "botany"), args.get("image_payload", {}))
                elif tname == "hubx_speech_transcribe":
                    res = agent.hubx_speech_transcribe(args.get("audio_metadata", {}))
                elif tname == "hubx_multimodal_generate":
                    res = agent.hubx_multimodal_generate(args.get("target_type", "portrait"), args.get("prompt_spec", {}))
                elif tname == "hubx_language_coach":
                    res = agent.hubx_language_coach(args.get("spoken_transcript", ""))
                else:
                    res = agent.run_benchmark_multimodal_tools()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
