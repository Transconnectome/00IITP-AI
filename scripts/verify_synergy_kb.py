import subprocess

def query_kb(text):
    print(f"\n--- Checking KB for: {text} ---")
    try:
        output = subprocess.check_output(["python3", "scripts/kb_query.py", f'"{text}"'], text=True)
        print(output)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query_kb("위장 팽창")
    query_kb("김성연")
    query_kb("Homeostatic Reinforcement")
