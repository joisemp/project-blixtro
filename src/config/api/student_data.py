import requests

def fetch_student_data(college_code, API_KEY, API_SECRET_KEY):
    url = f"https://{college_code}.linways.com/lin-api/v1/academics/student/details"
    headers = {
        "apiKey": API_KEY,
        "apiSecretKey": API_SECRET_KEY,
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None