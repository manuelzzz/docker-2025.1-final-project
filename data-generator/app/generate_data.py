import os
import time
import random
import psycopg2
from faker import Faker
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

db_params = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "database": os.getenv("POSTGRES_DB", "app_data"),
    "user": os.getenv("POSTGRES_USER", "app_data"),
    "password": os.getenv("POSTGRES_PASSWORD", "app_password"),
}

# Data generation interval in seconds
INTERVAL = int(os.getenv("DATA_GENERATION_INTERVAL", 60))

# Initialize Faker
fake = Faker()

# Products and regions for our demo data
PRODUCTS = [
    "Laptop",
    "Smartphone",
    "Tablet",
    "Headphones",
    "Monitor",
    "Keyboard",
    "Mouse",
]
REGIONS = ["North", "South", "East", "West", "Central"]


def connect_to_db():
    """Establish connection to the database with retry logic"""
    max_retries = 10
    retry_interval = 5  # seconds

    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(**db_params)
            print("Successfully connected to the database")
            return conn
        except psycopg2.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"Connection failed (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print("Maximum retries reached. Could not connect to the database.")
                raise


def create_tables(conn):
    """Create necessary tables if they don't exist"""
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id SERIAL PRIMARY KEY,
            product VARCHAR(100) NOT NULL,
            region VARCHAR(50) NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            sale_date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS website_traffic (
            id SERIAL PRIMARY KEY,
            page VARCHAR(100) NOT NULL,
            visitor_ip VARCHAR(50) NOT NULL,
            user_agent TEXT,
            visit_duration_seconds INT,
            visit_date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()
        print("Tables created successfully")


def generate_sales_data(conn):
    """Generate random sales data"""
    with conn.cursor() as cur:
        for _ in range(random.randint(5, 15)):
            product = random.choice(PRODUCTS)
            region = random.choice(REGIONS)
            quantity = random.randint(1, 10)
            price = round(random.uniform(50, 1500), 2)

            # Gens a random date within the last 7 days
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            sale_date = datetime.now() - timedelta(
                days=days_ago, hours=hours_ago, minutes=minutes_ago
            )

            cur.execute(
                """
            INSERT INTO sales (product, region, quantity, price, sale_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
                (product, region, quantity, price, sale_date),
            )

        conn.commit()
        print(f"Generated sales data at {datetime.now()}")


def generate_traffic_data(conn):
    """Generate random website traffic data"""
    pages = ["/home", "/products", "/about", "/contact", "/blog", "/cart", "/checkout"]

    with conn.cursor() as cur:
        for _ in range(random.randint(10, 30)):
            page = random.choice(pages)
            visitor_ip = fake.ipv4()
            user_agent = fake.user_agent()
            visit_duration = random.randint(5, 300)  # 5 seconds to 5 minutes

            # Gens a random date within the last 7 days
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            visit_date = datetime.now() - timedelta(
                days=days_ago, hours=hours_ago, minutes=minutes_ago
            )

            cur.execute(
                """
            INSERT INTO website_traffic (page, visitor_ip, user_agent, visit_duration_seconds, visit_date)
            VALUES (%s, %s, %s, %s, %s)
            """,
                (page, visitor_ip, user_agent, visit_duration, visit_date),
            )

        conn.commit()
        print(f"Generated traffic data at {datetime.now()}")


def main():
    """Main function to run the data generator"""
    print("Starting data generator...")

    # Connect to the database with retry logic
    conn = connect_to_db()

    try:
        # Create tables
        create_tables(conn)

        # Generate data periodically
        while True:
            try:
                generate_sales_data(conn)

                generate_traffic_data(conn)

                print(f"Waiting {INTERVAL} seconds before generating more data...")
                time.sleep(INTERVAL)

            except Exception as e:
                print(f"Error generating data: {e}")
                time.sleep(5)

    except KeyboardInterrupt:
        print("Data generator stopped by user")
    finally:
        conn.close()
        print("Database connection closed")


if __name__ == "__main__":
    main()
