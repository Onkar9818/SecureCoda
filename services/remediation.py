import requests
from config import BASE_URL, CODA_API_TOKEN

headers = {
    "Authorization": f"Bearer {CODA_API_TOKEN}"
}

def delete_doc(doc_id):
    url = f"{BASE_URL}/docs/{doc_id}"
    return requests.delete(url, headers=headers)

def unpublish_doc(doc_id):
    url = f"{BASE_URL}/docs/{doc_id}/publish"
    return requests.put(url, headers=headers, json={"published": False})

def delete_row(doc_id, table_id, row_id):
    url = f"{BASE_URL}/docs/{doc_id}/tables/{table_id}/rows/{row_id}"
    return requests.delete(url, headers=headers)