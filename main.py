import csv


def read_sales(filename):
    sales = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sales.append({
                "product": row["Product"],
                "quantity": int(row["Quantity"]),
                "price": float(row["Price"])
            })

    return sales


def calculate_revenue(sales):
    total = 0

    for item in sales:
        total += item["quantity"] * item["price"]

    return total


def find_top_product(sales):
    return max(
        sales,
        key=lambda item: item["quantity"] * item["price"]
    )


def main():
    sales = read_sales("sales.csv")

    revenue = calculate_revenue(sales)
    top_product = find_top_product(sales)

    print("===== SALES REPORT =====")
    print("Total Products:", len(sales))
    print("Total Revenue: Rs.", revenue)

    print(
        "Top Revenue Product:",
        top_product["product"]
    )


if __name__ == "__main__":
    main()