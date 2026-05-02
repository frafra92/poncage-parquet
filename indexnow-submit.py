#!/usr/bin/env python3
"""
IndexNow — Notification Bing des URLs mises à jour
Usage : python3 indexnow-submit.py
Lance après chaque upload GitHub pour notifier Bing instantanément.
"""
import urllib.request, json, os

KEY = "0B44C59CD3E10CC88E1B8524B0ECB95B"
HOST = "poncageparquetvitrificationfrancois.com"
DOMAIN = f"https://{HOST}"

# Récupérer toutes les URLs HTML du site
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
html_files = sorted([f for f in os.listdir(SCRIPT_DIR) if f.endswith('.html')])

EXCLUDE = {'404.html', 'test.html', 'redirect-ipfs.html', 
           'googlefefc9d50d82467ab.html',
           '7f49e4e8-6c34-4ed7-a619-b2b656607e69.html'}

urls = [f"{DOMAIN}/{f}" for f in html_files if f not in EXCLUDE]

# Payload IndexNow
payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": f"{DOMAIN}/{KEY}.txt",
    "urlList": urls
}

data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(
    "https://api.indexnow.org/indexnow",
    data=data,
    headers={'Content-Type': 'application/json; charset=utf-8'},
    method='POST'
)

try:
    with urllib.request.urlopen(req) as response:
        print(f"✅ IndexNow : {len(urls)} URLs soumises — statut {response.status}")
except Exception as e:
    print(f"❌ Erreur : {e}")
