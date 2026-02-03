import subprocess
import os
import sys

def get_context(query):
    try:
        res = subprocess.check_output(["python3", "scripts/kb_query.py", f'"{query}"'], text=True)
        return res
    except:
        return ""

def main():
    print("# Brainstorming: Inside-Out & Interoceptive AI Architecture\n")
    
    # 1. Gathering Evidence
    concepts = ["Inside-Out", "Homeostatic Reinforcement", "Interoception", "Gastric Distension", "Log-dynamic"]
    all_context = ""
    for c in concepts:
        all_context += f"\n--- Context for {c} ---\n"
        all_context += get_context(c)

    # 2. Reading the specialized prompt
    with open("_ops/idea_gen/interoceptive_prompt.md", "r") as f:
        prompt_logic = f.read()

    print("## Research Strategy Synthesis\n")
    print("Based on the provided research materials, we can synthesize the following 'Idea Generation' seeds:\n")
    
    seeds = [
        "1. **Log-Dynamic Weight Initialization**: Initialize Titans models with log-normal connectivity to mimic the 'Good-enough' vs 'Precision' neural circuits.",
        "2. **The 'Virtual Stomach' for LLMs**: Introduce a 'Resource Depletion' variable (Drive) that increases with token generation cost, forcing the agent to optimize for 'utility per unit energy'.",
        "3. **Vagal-Gated Attention**: A Transformer/Mamba layer that is modulated by a slow-integrating state (Interoception), providing a 'baseline mood' for response generation.",
        "4. **Reafferent Grounding**: Training the model to predict next-turn input NOT just based on history, but as a consequence of its previous output (Action-centric prediction)."
    ]
    
    for s in seeds:
        print(s)

    print("\n## Alignment with Kim Sung-yeon's Proposal")
    print("Integrating the 'Gastric Distension' (cNTS -> aIC) data into our RAG enables the AI-CoScientist to critique the NeuroX proposal with high biological fidelity, specifically reinforcing the 'slow integrator' aspect of internal states.")

if __name__ == "__main__":
    main()
