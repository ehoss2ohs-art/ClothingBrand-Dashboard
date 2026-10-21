from flask import Flask, jsonify, send_from_directory
import pyodbc

app = Flask(__name__)

SERVER = "البشمهندس"
DATABASE = "ClothingBrand"

CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    "Trusted_Connection=yes;"
)


def get_connection():
    return pyodbc.connect(CONNECTION_STRING)


@app.route("/")
def dashboard():
    return send_from_directory(".", "index.html")


@app.route("/api/summary")
def summary():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_orders,
                COALESCE(SUM(إجمالي_الفاتورة), 0) AS invoice_value
            FROM dbo.[الطلبات]
        """)
        row = cursor.fetchone()

        total_orders = int(row[0] or 0)
        invoice_value = float(row[1] or 0)

        cursor.execute("""
            SELECT
                COALESCE(حالة_الطلب, N'غير محدد') AS status,
                COUNT(*) AS total
            FROM dbo.[الطلبات]
            GROUP BY حالة_الطلب
        """)

        statuses = [
            {"status": str(row[0]), "count": int(row[1])}
            for row in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT
                COUNT(*) AS total_products,
                COALESCE(SUM(الكمية_بالمخزن), 0) AS stock_quantity,
                COALESCE(
                    SUM(
                        CAST(سعر_التكلفة AS BIGINT)
                        * CAST(الكمية_بالمخزن AS BIGINT)
                    ), 0
                ) AS inventory_cost,
                COALESCE(SUM(
                    CASE
                        WHEN الكمية_بالمخزن <= حد_إعادة_الطلب
                        THEN 1 ELSE 0
                    END
                ), 0) AS products_requiring_attention
            FROM dbo.[المنتجات]
        """)

        row = cursor.fetchone()

        inventory = {
            "products": int(row[0] or 0),
            "stock_quantity": int(row[1] or 0),
            "inventory_cost": float(row[2] or 0),
            "attention": int(row[3] or 0),
        }

        cursor.execute("""
            SELECT COUNT(*) FROM dbo.[العملاء]
        """)
        customers = int(cursor.fetchone()[0] or 0)

        cursor.execute("""
            SELECT
                YEAR(تاريخ_الطلب) AS order_year,
                MONTH(تاريخ_الطلب) AS order_month,
                COUNT(*) AS total_orders,
                COALESCE(SUM(إجمالي_الفاتورة), 0) AS invoice_value
            FROM dbo.[الطلبات]
            WHERE تاريخ_الطلب >= DATEADD(
                MONTH, -3,
                DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
            )
              AND تاريخ_الطلب < DATEADD(
                MONTH, 1,
                DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
            )
            GROUP BY YEAR(تاريخ_الطلب), MONTH(تاريخ_الطلب)
            ORDER BY order_year, order_month
        """)

        monthly = [
            {
                "year": int(row[0]),
                "month": int(row[1]),
                "orders": int(row[2]),
                "invoice_value": float(row[3] or 0),
            }
            for row in cursor.fetchall()
        ]

        cursor.execute("""
            SELECT
                YEAR(تاريخ_الطلب),
                MONTH(تاريخ_الطلب),
                حالة_الطلب,
                COUNT(*)
            FROM dbo.[الطلبات]
            WHERE تاريخ_الطلب >= DATEADD(
                MONTH, -3,
                DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
            )
              AND تاريخ_الطلب < DATEADD(
                MONTH, 1,
                DATEFROMPARTS(YEAR(GETDATE()), MONTH(GETDATE()), 1)
            )
            GROUP BY YEAR(تاريخ_الطلب), MONTH(تاريخ_الطلب), حالة_الطلب
        """)

        monthly_statuses = [
            {
                "year": int(row[0]),
                "month": int(row[1]),
                "status": str(row[2] or "غير محدد"),
                "count": int(row[3]),
            }
            for row in cursor.fetchall()
        ]

        return jsonify({
            "database": DATABASE,
            "total_orders": total_orders,
            "invoice_value": invoice_value,
            "customers": customers,
            "statuses": statuses,
            "inventory": inventory,
            "monthly": monthly,
            "monthly_statuses": monthly_statuses,
        })

    except Exception as error:
        app.logger.exception("Dashboard data query failed")
        return jsonify({"error": str(error)}), 500

    finally:
        connection.close()


if __name__ == "__main__":
    app.run(debug=True)