# Meridian Retail data (CSV)

The five tables of the Meridian Retail database, exactly as `../generate_meridian.py` creates them
(seed 42, Faker 40.54.0). UTF-8, comma-separated, one header row, rows sorted by their key.

| File | Rows | Columns |
|:--|--:|:--|
| `dim_country.csv` | 6 | country_id, country_name |
| `dim_category.csv` | 12 | category_id, category_name |
| `dim_customer.csv` | 10,000 | customer_id, first_name, last_name, email, country_id, signup_date |
| `dim_product.csv` | 500 | product_id, product_name, category_id, unit_price |
| `fact_orders.csv` | 250,000 | order_id, customer_id, product_id, order_date, quantity, unit_price, total_amount, status |

Load them into PostgreSQL (Chapter 1) from the repository folder:

```bash
python data/load_meridian_csv.py
```

You can also read them with pandas (`pd.read_csv`) or open them in LibreOffice Calc. In Excel, use
*Data → From Text/CSV* rather than a double-click: the files are UTF-8, and a double-click garbles the
1,571 customer names with accents (Antón becomes AntÃ³n). The names in `dim_customer` are invented by Faker;
no real person is described. `export_meridian_csv.py` rewrites these files from the database, and the
book's tests check on every change that they match the generator.
