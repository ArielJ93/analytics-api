from scripts.transform import transform_data, cleaning_data
from scripts.extract import get_data
import requests
from scripts.config import settings


def api_inyection(data, create_endpoint, headers):

    payload = data.to_dict(orient="records")
    response = requests.post(create_endpoint, headers=headers, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    
    
if __name__ == "__main__":
    
    base_url = "https://analytics-api-hg65.onrender.com"
    path = "/api/events/"
    create_endpoint = f"{base_url}{path}"
    
    headers = {
        "X-API-KEY": settings.AUTOMATION_API_KEY,
        "content-type": "application/json"
    }
    
    data = get_data()
    df = transform_data(data)
    df_clean = cleaning_data(df)
    api_inyection(df_clean, create_endpoint, headers)
