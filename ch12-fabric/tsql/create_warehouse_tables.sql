-- Run in the Fabric warehouse "meridian_wh" (Step 6). Not run on SQL Server: Fabric-only syntax.
CREATE TABLE dbo.fact_orders (
    order_id     INT           NOT NULL,
    customer_id  INT           NOT NULL,
    product_id   INT           NOT NULL,
    order_date   DATE          NOT NULL,
    quantity     INT           NOT NULL,
    unit_price   DECIMAL(8,2)  NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status       VARCHAR(20)   NOT NULL
);
ALTER TABLE dbo.fact_orders
    ADD CONSTRAINT pk_fact_orders PRIMARY KEY NONCLUSTERED (order_id) NOT ENFORCED;

COPY INTO dbo.fact_orders
FROM 'https://onelake.dfs.fabric.microsoft.com/meridian/meridian_lh.Lakehouse/Files/meridian/fact_orders.parquet'
WITH (FILE_TYPE = 'PARQUET');

-- A gold table built with CREATE TABLE AS SELECT, from the lakehouse tables
CREATE TABLE dbo.gold_country_revenue AS
SELECT c.country_name, YEAR(o.order_date) AS order_year,
       COUNT(*) AS orders, SUM(o.total_amount) AS revenue
FROM meridian_lh.dbo.fact_orders AS o
JOIN meridian_lh.dbo.dim_customer AS cu
  ON cu.customer_id = o.customer_id
JOIN meridian_lh.dbo.dim_country AS c
  ON c.country_id = cu.country_id
WHERE o.status = 'completed'
GROUP BY c.country_name, YEAR(o.order_date);
