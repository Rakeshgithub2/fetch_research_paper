# PubMed Paper Fetcher

A Python script to fetch research papers from PubMed based on a user-specified query and save the results in a CSV file.

## Installation

1. Install Poetry (if not already installed):
   ```sh
   pip install poetry

git clone <your-github-repo-url>
cd pubmed-paper-fetcher

poetry install
poetry run get-papers-list "your search query" -f output.csv
poetry run get-papers-list "cancer research" -f results.csv



