import re
import requests

def collapse_id(sutta_id):
    """
    Collapses x.y.z to x.z or standard SuttaCentral format.
    Example: 1.2.3 (Book 1, Section 2, Sutta 3) -> 1.3
    """
    parts = sutta_id.split('.')
    if len(parts) == 3:
        return f"{parts[0]}.{parts[2]}"
    return sutta_id

def search_sutta_central(buddha_text, collapsed_id):
    """
    Searches SuttaCentral for matches based on text and collapsed ID.
    """
    # SuttaCentral API base (Public API)
    SC_API_BASE = "https://suttacentral.net/api"

    # Strategy 1: Search by ID
    # SuttaCentral uses identifiers like 'mn1', 'an1.1', etc.
    # This requires a mapping from our 'x' (Book Number) to SC's 'mn/an/sn'

    # Strategy 2: Text Search (Semantic/Keyword)
    search_url = f"{SC_API_BASE}/search?query={buddha_text[:200]}&lang=en"

    try:
        response = requests.get(search_url)
        if response.status_code == 200:
            results = response.json()
            # If a high-scoring match is found in results
            if results.get('hits') and len(results['hits']) > 0:
                best_hit = results['hits'][0]
                # Check score threshold (example)
                if best_hit.get('score', 0) > 0.8:
                    return f"https://suttacentral.net/{best_hit['uid']}"
    except Exception as e:
        print(f"Error searching SuttaCentral: {e}")

    return None

def process_sutta_json(sutta_json_path):
    import json
    with open(sutta_json_path, 'r') as f:
        data = json.load(f)

    buddha_text = data.get('buddha_text', '')
    sutta_id = data.get('sutta_id', '')

    collapsed = collapse_id(sutta_id)
    sc_url = search_sutta_central(buddha_text, collapsed)

    if sc_url:
        data['sutta_central_url'] = sc_url
        with open(sutta_json_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    return False
