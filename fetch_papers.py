import requests
import pandas as pd
import argparse
import sys

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_papers(query, debug=False):
    """Fetch research papers from PubMed based on a query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,  # Limiting results to 10 for simplicity
        "retmode": "json"
    }
    
    response = requests.get(PUBMED_API_URL, params=params)
    
    if response.status_code != 200:
        print("Error fetching data from PubMed API.")
        sys.exit(1)

    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])

    if debug:
        print(f"Fetched {len(paper_ids)} papers.")

    return paper_ids

def fetch_paper_details(paper_ids, debug=False):
    """Fetch detailed information for given PubMed paper IDs."""
    if not paper_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "json"
    }
    
    response = requests.get(DETAILS_API_URL, params=params)

    if response.status_code != 200:
        print("Error fetching paper details.")
        sys.exit(1)

    result = response.json().get("result", {})
    papers = []

    for pid in paper_ids:
        data = result.get(pid, {})
        papers.append({
            "PubmedID": pid,
            "Title": data.get("title", "N/A"),
            "Publication Date": data.get("pubdate", "N/A"),
            "Non-academic Author(s)": "N/A",  # This requires advanced NLP to extract
            "Company Affiliation(s)": "N/A",  # This requires deeper parsing
            "Corresponding Author Email": "N/A"
        })

    if debug:
        print(f"Extracted details for {len(papers)} papers.")

    return papers

def save_to_csv(papers, filename):
    """Save the fetched papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Saved results to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed API")
    parser.add_argument("-f", "--file", help="Output CSV filename", default="results.csv")
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")

    args = parser.parse_args()

    paper_ids = fetch_pubmed_papers(args.query, args.debug)
    paper_details = fetch_paper_details(paper_ids, args.debug)
    
    if args.file:
        save_to_csv(paper_details, args.file)
    else:
        print(pd.DataFrame(paper_details))

if __name__ == "__main__":
    main()
