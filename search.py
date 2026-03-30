from duckduckgo_search import DDGS
import requests

def search_internet(query, max_results=5):
    # Method 1
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    'title': r.get('title', ''),
                    'body': r.get('body', ''),
                    'url': r.get('href', '')
                })
        if results:
            return results
    except Exception as e:
        print(f"Method 1 failed: {e}")

    # Method 2
    try:
        results = []
        ddgs = DDGS()
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                'title': r.get('title', ''),
                'body': r.get('body', ''),
                'url': r.get('href', '')
            })
        if results:
            return results
    except Exception as e:
        print(f"Method 2 failed: {e}")

    # Method 3 - Direct HTTP
    try:
        from urllib.parse import quote
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
        url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            results = []
            import re
            titles = re.findall(r'class="result__a"[^>]*>(.*?)</a>', response.text)
            snippets = re.findall(r'class="result__snippet">(.*?)</a>', response.text)
            for i in range(min(len(titles), max_results)):
                results.append({
                    'title': re.sub('<.*?>', '', titles[i]),
                    'body': re.sub('<.*?>', '', snippets[i]) if i < len(snippets) else '',
                    'url': ''
                })
            if results:
                return results
    except Exception as e:
        print(f"Method 3 failed: {e}")

    # Method 4 - Wikipedia
    try:
        from urllib.parse import quote
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(query.replace(' ', '_'))}"
        response = requests.get(url, timeout=8)
        if response.status_code == 200:
            data = response.json()
            return [{
                'title': data.get('title', query),
                'body': data.get('extract', ''),
                'url': data.get('content_urls', {}).get('desktop', {}).get('page', '')
            }]
    except Exception as e:
        print(f"Method 4 failed: {e}")

    return []
