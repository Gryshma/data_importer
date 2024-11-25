import psycopg2
import yaml
import json
from data_importer.logger import Logger


class Database:
    def __init__(self):
        # Initialize the logger
        self.logger = Logger().logger

        # Load database configuration
        try:
            with open('config/config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                db_config = config['database']
        except Exception as e:
            self.logger.error(f"Failed to load database configuration: {e}")
            raise

        # Initialize the database connection and cursor
        try:
            self.connection = psycopg2.connect(
                host=db_config['host'],
                port=db_config['port'],
                dbname=db_config['dbname'],
                user=db_config['user'],
                password=db_config['password']
            )
            self.cursor = self.connection.cursor()
            self.logger.info("Database connected successfully.")
        except Exception as e:
            self.logger.error(f"Failed to connect to the database: {e}")
            raise

    def insert_phone_data(self, phone_id, phone_name, phone_data):
        query = """
        INSERT INTO public.phone (phoneid, phone_name, phone_data)
        VALUES (%s, %s, %s)
        ON CONFLICT (phoneid) DO NOTHING;
        """
        try:
            # Convert phone_data to JSON if it's a dictionary
            phone_data_json = json.dumps(phone_data) if isinstance(phone_data, dict) else phone_data
            self.cursor.execute(query, (phone_id, phone_name, phone_data_json))
            self.connection.commit()
            self.logger.info(f"Inserted phone data successfully: {phone_id}")
        except Exception as e:
            self.logger.error(f"Error inserting phone data: {e}")
            raise

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        self.logger.info("Database connection closed.")
