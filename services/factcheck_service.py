import requests

# Wikidata SPARQL endpoint
WIKIDATA_API = "https://query.wikidata.org/sparql"

def fact_check_wikidata(query):
    """
    Query Wikidata for related facts.
    """
    sparql = f"""
    SELECT ?item ?itemLabel WHERE {{
      ?item ?label "{query}"@en.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT 1
    """
    headers = {"Accept": "application/sparql-results+json"}
    try:
        response = requests.get(WIKIDATA_API, params={"query": sparql}, headers=headers, timeout=10)
        data = response.json()
        if "results" in data and data["results"]["bindings"]:
            item = data["results"]["bindings"][0]
            return {
                "status": "found",
                "source": item["itemLabel"]["value"]
            }
        else:
            return {"status": "not found", "source": None}
    except Exception as e:
        return {"status": "error", "source": str(e)}
