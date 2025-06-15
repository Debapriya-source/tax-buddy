from langchain.tools import tool
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json

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
    "https://cleartax.in/paytax/taxcalculator",
    "https://cleartax.in/s/salary-income",
    "https://cleartax.in/s/house-property?ref=income-tax-calculator",
    "https://cleartax.in/s/capital-gains-income?ref=income-tax-calculator",
    "https://cleartax.in/s/income-tax-for-freelancers?ref=income-tax-calculator",
    "https://cleartax.in/s/other-income-sources",
]

# ——— Load model once at import time onto CPU ———
MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")


@tool
def search_tax_websites(raw_input: str) -> str:
    """
    Search tax realted websites from govt. of India for a query.
    raw_input: JSON-encoded string with keys:
      - q (str): the query (required)
      - max_hits (int): how many hits per site (default 3)
      - context_lines (int): lines before/after a hit (default 3)
      - max_chars (int): truncate each snippet to this many chars (default 500)

    Example:
      search_tax_sites('{"q":"LTCG rate","max_hits":2,"context_lines":2,"max_chars":300}')
    """
    # Parse arguments
    try:
        params = json.loads(raw_input)
    except json.JSONDecodeError:
        return (
            "❌ Invalid input. Please pass a JSON string, e.g.: "
            '{"q":"long-term capital gains","max_hits":2,"context_lines":2,"max_chars":300}'
        )

    q = params.get("q", "").strip()
    if not q:
        return "❌ Query cannot be empty."

    max_hits = int(params.get("max_hits", 3))
    context_lines = int(params.get("context_lines", 3))
    max_chars = int(params.get("max_chars", 500))

    results = []

    def search_url(url):
        try:
            text = BeautifulSoup(
                requests.get(url, timeout=5).text, "html.parser"
            ).get_text("\n")
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

            q_emb = MODEL.encode(q.lower())
            txt_emb = MODEL.encode(lines)
            sims = cosine_similarity([q_emb], txt_emb)[0]

            # pick top hits
            idxs = sims.argsort()[-max_hits:][::-1]
            chunks = []
            for i in idxs:
                if sims[i] > 0.3:
                    start = max(0, i - context_lines)
                    end = min(len(lines), i + context_lines + 1)
                    chunks.append(lines[start:end])

            if chunks:
                block = [f"\nURL: {url}"]
                for chunk in chunks:
                    snippet = "\n".join(chunk)
                    # truncate
                    if len(snippet) > max_chars:
                        snippet = snippet[:max_chars].rsplit("\n", 1)[0] + "\n..."
                    block.append(snippet)
                return block

        except Exception as e:
            print(f"Error searching {url}: {e}")
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for res in executor.map(search_url, SITES):
            if res:
                results.extend(res)

    return "\n".join(results) if results else "No results found."


if __name__ == "__main__":
    query = "What is the long-term capital gains tax?"
    print(
        search_tax_websites(
            '{"q":"long-term capital gains","max_hits":2,"context_lines":2,"max_chars":300}'
        )
    )
