import requests
import openai
import json
import os
from datetime import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
openstates_api_key = os.getenv("OPENSTATES_API_KEY")

def summarize(text):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this bill in plain English."},
                {"role": "user", "content": text}
            ]
        )
        return res["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Summary failed: {str(e)}"

def fetch_openstates_bills(state_code):
    url = f"https://v3.openstates.org/bills?jurisdiction={state_code}&sort=date_introduced&per_page=5"
    headers = {"X-API-KEY": openstates_api_key}
    res = requests.get(url, headers=headers)
    bills = res.json().get("results", [])
    return bills

def process_state(state_code, save_as):
    bills = fetch_openstates_bills(state_code)
    output = []
    for b in bills:
        title = b.get("title", "Untitled")
        text = b.get("abstracts", [{}])[0].get("abstract", title)
        summary = summarize(text)
        output.append({
            "title": title,
            "summary": summary,
            "date": b.get("created_at", "")[:10]
        })
    with open(f"data/{save_as}_bills.json", "w") as f:
        json.dump(output, f, indent=2)

def main():
    os.makedirs("data", exist_ok=True)
    for code, name in [("Kansas", "ks"), ("California", "ca")]:
        process_state(code, name)

if __name__ == "__main__":
    main()
