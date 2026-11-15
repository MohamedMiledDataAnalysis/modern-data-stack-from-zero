# Chapter 19 — corrections (run from the ch19-r folder, after analysis.R)
library(DBI)
library(dplyr)
con <- dbConnect(RPostgres::Postgres(), host = "localhost", dbname = "meridian_db",
                 user = "meridian_user", password = "meridian2024")
done <- dbGetQuery(con, "SELECT o.*, o.total_amount::float AS amount, ca.category_name
  FROM fact_orders o JOIN dim_product p USING (product_id)
  JOIN dim_category ca USING (category_id) WHERE o.status = 'completed'")
dbDisconnect(con)

cat("Exercise 1\n")
done |> mutate(month = format(order_date, "%Y-%m")) |>
  filter(month < "2024-01") |>
  group_by(month) |> summarise(revenue = sum(amount)) |>
  slice_max(revenue, n = 3) |> print()

cat("Exercise 2\n")
done |> group_by(category_name) |>
  summarise(median_order = median(amount), mean_order = mean(amount)) |>
  arrange(desc(median_order)) |> head(3) |> print()

cat("Exercise 3\n")
x <- done$quantity; y <- done$amount
print(cor.test(x, y))
