import asyncio
import os
import sys

# Ensure we can find the notebooklm_mcp package if it's in site-packages
# (It should be automatically found if running with venv python)

from notebooklm_mcp.client import NotebookLMClient
from notebooklm_mcp.config import ServerConfig

async def main():
    config_path = "notebooklm-config.json"
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found")
        return

    print("Loading configuration...")
    config = ServerConfig.from_file(config_path)
    
    # Force headless if needed, but let's stick to config
    # config.headless = False 
    
    client = NotebookLMClient(config)
    
    print("Starting client...")
    await client.start()
    
    print("Authenticating...")
    try:
        is_auth = await client.authenticate()
        if is_auth:
            print("Authenticated successfully.")
            
            queries = [
                "Explain the 'Surprise' mechanism in Titans (2025) and how it differs from standard Transformers memory.",
                "How does BrainMamba argue for State Space Models (SSM) superiority over Transformers in EEG/neuroimaging tasks?"
            ]
            
            full_response = "# SOTA Benchmarks (NotebookLM)\n\n"
            
            for q in queries:
                print(f"Sending query: {q}")
                await client.send_message(q)
                print("Waiting for response...")
                response = await client.get_response(wait_for_completion=True, max_wait=120)
                print("Response received.")
                
                full_response += f"## Query: {q}\n\n{response}\n\n---\n\n"
            
            output_path = "docs/04_validation/sota_benchmarks.md"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(full_response)
            print(f"Saved response to {output_path}")
            
        else:
            print("Authentication failed. Please check if you are logged in using ./setup_notebooklm.sh")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
