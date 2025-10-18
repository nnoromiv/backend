import requests
import datetime

URL = "https://api.tfl.gov.uk/Road/all/Disruption"

def fetch_incidents():

    response = requests.get(URL)
    data = response.json()

    incidents = []
      
    for item in data:
        incidents.append({
            "id": item.get("id"),
            "severity": item.get("severity"),
            "category": item.get("category"),
            "subCategory": item.get("subCategory"),
            "currentUpdate": item.get("currentUpdate"),
            "location": item.get("location"),
            "start_date": item.get("startDateTime"),
            "end_date": item.get("endDateTime"),
            "timestamp": datetime.datetime.now().isoformat()
        })

    return incidents

if __name__ == "__main__":
    inc = fetch_incidents()
    print(f"Total incidents found: {len(inc)}")
    print(inc[:3])
