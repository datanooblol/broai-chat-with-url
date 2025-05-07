import requests


def scrape_jina_ai(url: str) -> str:
    response = requests.get("https://r.jina.ai/"+url)
    return response.text
