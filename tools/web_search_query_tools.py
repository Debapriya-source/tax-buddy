import requests
from bs4 import BeautifulSoup
from langchain.agents import tool

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


@tool
def search_tax_sites(q: str, max_hits: int = 3) -> str:
    """
        Search each FAQ page for a query string from [
        "ClearTax - Long-Term Capital Gains (LTCG) Tax Guide",
        "Income Tax India - FAQs on Permanent Account Number (PAN)",
        "Income Tax Department - e-Filing ITR-1 (Sahaj) FAQs",
        "Income Tax Department - e-Filing ITR-2 FAQs",
        "Department of Financial Services - Ministry of Finance (DFS portal)",
        "Department of Public Enterprises - FAQs (DPE portal)",
        "Ministry of Finance - Government of India (Home)",
        "CBIC-GST - GST Frequently Asked Questions",
        "CBIC-GST - New GST Registration FAQs & User Manual",
        "Income Tax India - FAQs on Capital Gains",
        "ClearTax - Income Tax Calculator",
        "ClearTax - Salary Income Guide",
        "ClearTax - House Property Income Guide",
        "ClearTax - Capital Gains Income Guide",
        "ClearTax - Income Tax for Freelancers Guide",
        "ClearTax - Other Income Sources Guide",
    ].

          Args:
            query: Substring to search for (case-insensitive).
            context_lines: How many lines before/after a hit to include.

          Returns:
            A formatted string containing the search results with URLs and matching text snippets.
    """
    import concurrent.futures

    print(f"Searching for '{q}' in tax sites...")
    if not q:
        return "Query cannot be empty."
    ql = q.lower()
    results = []

    def search_url(url):
        print(f"Searching {url}...")
        try:
            txt = BeautifulSoup(
                requests.get(url, timeout=5).text, "html.parser"
            ).get_text("\n")
            hits = [line.strip() for line in txt.splitlines() if ql in line.lower()][
                :max_hits
            ]
            if hits:
                result = [f"\nURL: {url}"]
                result.extend(f"- {hit}" for hit in hits)
                return result
        except Exception:
            return None
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for result in executor.map(search_url, SITES):
            if result:
                results.extend(result)

    return "\n".join(results) if results else "No results found."
