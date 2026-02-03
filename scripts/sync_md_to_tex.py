#!/usr/bin/env python3
import os
import re
from pathlib import Path

def md_to_tex(content):
    # Headers
    content = re.sub(r'^# (.*)', r'\\section{\1}', content, flags=re.M)
    content = re.sub(r'^## (.*)', r'\\subsection{\1}', content, flags=re.M)
    content = re.sub(r'^### (.*)', r'\\subsubsection{\1}', content, flags=re.M)
    
    # Bold/Italic
    content = re.sub(r'\*\*(.*?)\*\*', r'\\textbf{\1}', content)
    content = re.sub(r'\*(.*?)\*', r'\\textit{\1}', content)
    
    # Lists
    # Simple bullet conversion (naive)
    content = re.sub(r'^- (.*)', r'\\begin{itemize}\n\\item \1\n\\end{itemize}', content, flags=re.M)
    # Fix adjacent itemize (merge them) - naive approach
    content = content.replace('\\end{itemize}\n\\begin{itemize}\n', '')

    def image_repl(match):
        alt = match.group(1)
        path = match.group(2)
        # Use flat graphics structure for Overleaf
        filename = Path(path).name
        return f"\\begin{{figure}}[h]\n\\centering\n\\includegraphics[width=1.0\\textwidth]{{graphics/{filename}}}\n\\caption{{{alt}}}\n\\end{{figure}}"

    content = re.sub(r'!\[(.*?)\]\((.*?)\)', image_repl, content)

    return content

def main():
    base_dir = Path("docs/03_proposal/drafts")
    tex_dir = Path("tex/sections")
    tex_dir.mkdir(parents=True, exist_ok=True)

    for md_file in base_dir.glob("*.md"):
        print(f"Converting {md_file}...")
        content = md_file.read_text(encoding="utf-8")
        tex_content = md_to_tex(content)
        
        tex_file = tex_dir / md_file.with_suffix(".tex").name
        tex_file.write_text(tex_content, encoding="utf-8")
        print(f"Saved to {tex_file}")

if __name__ == "__main__":
    main()
