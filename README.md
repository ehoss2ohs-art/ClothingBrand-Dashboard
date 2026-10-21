ClothingBrand — Retail Analytics Dashboard

Project Overview

ClothingBrand is a retail analytics dashboard built with Python, Flask, HTML, and Microsoft SQL Server.

The dashboard displays store orders, invoice totals, inventory information, and monthly order summaries.

Technologies

* Python
* Flask
* pyodbc
* HTML, CSS, JavaScript
* Microsoft SQL Server

Requirements

* Python installed on the computer
* Microsoft SQL Server
* ODBC Driver 17 for SQL Server
* Access to the ClothingBrand database

Database Configuration

The application connects to the ClothingBrand database using Windows Authentication.

Before running the project, verify the SQL Server name and database connection settings in app.py.

Installation

Open a terminal in the project folder and run:

python -m pip install -r requirements.txt

Run the Application

Run:

python app.py

Then open the following address in your browser:

http://127.0.0.1:5000/

Data Limitation

The order-details table is currently empty. Therefore, detailed product-level sales and actual profit by product cannot be calculated from that table.

Notes

The recipient must configure access to their own SQL Server database. The local address above is for running the application on the same computer.