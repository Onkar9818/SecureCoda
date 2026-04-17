import requests
from config import CODA_API_TOKEN, BASE_URL

headers = {
    "Authorization": f"Bearer {CODA_API_TOKEN}"
}

def get_docs():
    url = f"{BASE_URL}/docs"
    res = requests.get(url, headers=headers)
    return res.json().get("items", [])

def get_tables(doc_id):
    url = f"{BASE_URL}/docs/{doc_id}/tables"
    return requests.get(url, headers=headers).json().get("items", [])

def get_rows(doc_id, table_id):
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/rows"
    return requests.get(url, headers=headers).json().get("items", [])
def get_pages(doc_id):
    url = f"{BASE_URL}/docs/{doc_id}/pages"
    return requests.get(url, headers=headers).json().get("items", [])

print("TOKEN:", CODA_API_TOKEN)