#!/usr/bin/env python3
import argparse
import sys
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse

def search_arxiv(query, limit=5):
    print(f"🔍 Searching arXiv for: '{query}'...")
    clean_query = urllib.parse.quote(query)
    url = f'http://export.arxiv.org/api/query?search_query=all:{clean_query}&start=0&max_results={limit}&sortBy=relevance&sortOrder=descending'
    
    try:
        with urllib.request.urlopen(url) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        results = []
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', namespace).text[:4]
            authors_node = entry.findall('atom:author', namespace)
            authors = [a.find('atom:name', namespace).text for a in authors_node]
            link = entry.find('atom:id', namespace).text
            
            results.append({
                'title': title,
                'year': published,
                'authors': [{'name': a} for a in authors],
                'venue': 'arXiv',
                'citationCount': 'N/A',
                'url': link,
                'abstract': summary
            })
        return results
    except Exception as e:
        print(f"arXiv Error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Academic Search Tool (Pseudo-MCP)")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Results limit")
    args = parser.parse_args()

    results = search_arxiv(args.query, args.limit)
    
    if not results:
        print("❌ No results found on arXiv.")
        sys.exit(1)
    
    print(f"✅ Found {len(results)} papers from arXiv:\n")
    
    for i, paper in enumerate(results):
        title = paper.get('title', 'No Title')
        year = paper.get('year', 'N/A')
        authors = ", ".join([a['name'] for a in paper.get('authors', [])[:3]])
        venue = paper.get('venue', 'Unknown Venue')
        citations = paper.get('citationCount', 0)
        link = paper.get('url', '#')
        abstract = paper.get('abstract', 'No abstract available.')
        
        if abstract and len(abstract) > 200:
            abstract = abstract[:200] + "..."

        print(f"--- Paper #{i+1} ---")
        print(f"📜 **{title}** ({year}) / {authors}")
        print(f"🔗 {link}")
        print(f"📝 {abstract}\n")

if __name__ == "__main__":
    main()
