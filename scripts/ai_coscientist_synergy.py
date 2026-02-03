import sys
import subprocess

def get_kb_context(query):
    try:
        # Use existing kb_query tool
        res = subprocess.check_output(["python3", "scripts/kb_query.py", f'"{query}"'], text=True)
        return res
    except Exception as e:
        return f"Error querying KB for {query}: {e}"

def read_text_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {e}"

def main():
    print("=== NeuroX-OS: AI-CoScientist Synergy Analysis ===\n")
    
    # 1. Gather context from newly extracted files
    kim_proposal = read_text_file("인공지능과제 연구제안 - 김성연.txt")
    idea_note = read_text_file("아이디어.txt")
    
    # 2. Gather context from existing project architecture
    readme = read_text_file("README.md")
    
    # 3. Formulate the "Integrated Research Plan"
    print("## 1. Research Identity: 'Inside-Out Multisensory SSM'\n")
    print("- **Problem**: Current AI is 'Outside-In' (passive mapping of stimulus to label).")
    print("- **Solution**: Build a **'Homeostatic Titans Memory'** system centered on Professor Kim's gastric distension (interoceptive) signals.")
    print("- **Mechanism**: The 'Virtual Stomach' (Internal State) drives the 'Sensory Encoder' (Multisensory Integration).\n")

    print("## 2. Technical Aim Integration\n")
    print("### Aim 1: Interoceptive Sensory Encoder (Bridging Part 1 & Interoception)")
    print("- **Task**: Instead of purely visual/auditory JEPA, implement an 'Interoceptive Feature Extractor'.")
    print("- **Data**: Use Prof. Kim's 2-photon/fiber photometry data (NE signals in aIC/PVH) as a 'ground truth' for internal value weighting.")
    
    print("\n### Aim 2: Drive-Modulated Titans Memory (Bridging Part 2 & HRRL)")
    print("- **Task**: Modify the Titans Memory SSM to include a 'Drive Function' ((H_t)$).")
    print("- **Logic**: High neuro-metabolic cost (simulated) or high 'prediction error' triggers a shift toward exploration mode.")
    
    print("\n### Aim 3: Reafferent Grounding for Robotic Embodiment")
    print("- **Task**: Test the model in a closed-loop scenario (like the 'Tissue culture' example).")
    print("- **Validation**: The AI must demonstrate 'Information Creation' by matching its internal motor commands with sensory reafference (Grounding).\n")

    print("## 3. Synergy with Existing Skills")
    print("- ****: Update with Duriez & Gutkin (2023) and Keramati & Gutkin (2014) as the theoretical foundation for RL-Homeostasis coupling.")
    print("- ****: Update the 'Two-Part Model' to a 'Three-Part Loop' (Interoception -> Titans Memory -> Action/Reafference).")

if __name__ == "__main__":
    main()
