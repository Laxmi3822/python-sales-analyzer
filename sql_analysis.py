import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

CSV_FILE = BASE_DIR / "sales.csv"
DB_FILE = BASE_DIR / "sales.db"


def create_database():

    with sqlite3.connect(DB_FILE) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)

        cursor.execute("DELETE FROM sales")

        with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)

            required = {"Product", "Quantity", "Price"}

            if not required.issubset(reader.fieldnames or []):
                raise ValueError("CSV columns are missing")

            records = []

            for row in reader:

                product = row["Product"].strip()
                quantity = int(row["Quantity"])
                price = float(row["Price"])

                if not product or quantity < 0 or price < 0:
                    raise ValueError("Invalid sales record")

                records.append((product, quantity, price))

        cursor.executemany("""
            INSERT INTO sales (product, quantity, price)
            VALUES (?, ?, ?)
        """, records)

        print("Sales data imported successfully!")


def analyze_sales():

    with sqlite3.connect(DB_FILE) as connection:

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(DISTINCT product),
                SUM(quantity),
                SUM(quantity * price)
            FROM sales
        """)

        result = cursor.fetchone()

        print("\n===== SALES SUMMARY =====")

        print("Product Types:", result[0])
        print("Total Units Sold:", result[1])
        print("Total Revenue: Rs.", result[2])

        cursor.execute("""
            SELECT
                product,
                SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
            LIMIT 1
        """)

        top_product = cursor.fetchone()

        print("\nTop Revenue Product:", top_product[0])
        print("Product Revenue: Rs.", top_product[1])

        cursor.execute("""
            SELECT
                product,
                SUM(quantity) AS units_sold,
                SUM(quantity * price) AS revenue
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
        """)

        print("\n===== PRODUCT-WISE REPORT =====")

        for row in cursor.fetchall():
            print(row)


def main():

    create_database()
    analyze_sales()


if __name__ == "__main__":
    main()