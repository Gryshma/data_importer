from data_importer.api_client import APIClient
from data_importer.db import Database

def main():
    # Fetch data from the API
    api_client = APIClient()
    data = api_client.fetch_data()

    # Insert data into the database
    db = Database()
    for item in data:
        phone_id = item["id"]
        phone_name = item.get("name", "Unknown")  # Handle missing name
        phone_data = item.get("data", {})  # Handle missing data
        
        db.insert_phone_data(phone_id, phone_name, phone_data)
    
    db.close()  # Close the database connection
    print("Data successfully imported into the database.")

if __name__ == "__main__":
     main()