import requests
from bs4 import BeautifulSoup
from langchain.agents import tool
# List of FAQ pages to search
SITES = [
    "https://cleartax.in/s/long-term-capital-gains-ltcg-tax",
    "https://incometaxindia.gov.in/Pages/faqs.aspx?k=FAQs%20on%20Permanent%20Account%20Number&c=5",
    "https://www.incometax.gov.in/iec/foportal/help/e-filing-itr1-form-sahaj-faq",
    "https://www.incometax.gov.in/iec/foportal/help/e-filing-itr2-form-faq",
    "https://financialservices.gov.in/beta/en",
    "https://dpe.gov.in/faq",
    "https://finmin.gov.in/",
    "https://cbic-gst.gov.in/faq.html",
    "https://cbic-gst.gov.in/faqs-user-manual-new-gst-registration.html",
    "https://incometaxindia.gov.in/Pages/faqs.aspx?k=FAQs+on+Capital+Gains",
]

@tool
def search_tax_sites(query: str, context_lines: int = 2) -> dict[str, list[str]]:
    """
    Search each FAQ page for a query string.
    
    Args:
      query: Substring to search for (case-insensitive).
      context_lines: How many lines before/after a hit to include.
    
    Returns:
      A dict mapping URL -> list of matching text snippets.
    """
    results = {}
    q_lower = query.lower()
    
    for url in SITES:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            
            # Extract visible text
            soup = BeautifulSoup(resp.text, "html.parser")
            text = soup.get_text(separator="\n")
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            
            # Find matches with a little context
            hits = []
            for idx, line in enumerate(lines):
                if q_lower in line.lower():
                    start = max(0, idx - context_lines)
                    end   = min(len(lines), idx + context_lines + 1)
                    snippet = "\n".join(lines[start:end])
                    hits.append(snippet)
            
            if hits:
                results[url] = hits
        
        except Exception as e:
            results[url] = [f"⚠️ Error fetching page: {e}"]
    
    return results
