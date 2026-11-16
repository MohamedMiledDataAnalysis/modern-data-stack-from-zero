# Chapter 19 — analysing Meridian with R
library(DBI)
library(dplyr)
library(ggplot2)

con <- dbConnect(RPostgres::Postgres(),
                 host = "localhost", port = 5432, dbname = "meridian_db",
                 user = "meridian_user", password = "meridian2024")

# Step 1 — read orders with their country
orders <- dbGetQuery(con, "
  SELECT o.order_id, o.customer_id, o.order_date, o.quantity,
         o.total_amount::float AS total_amount, o.status, co.country_name
  FROM fact_orders o
  JOIN dim_customer c  ON o.customer_id = c.customer_id
  JOIN dim_country co ON c.country_id  = co.country_id
  ORDER BY o.order_id")
dbDisconnect(con)
str(orders)

done <- orders |> filter(status == "completed")
cat("completed orders:", nrow(done), "\n")
print(summary(done$total_amount))

# Step 2 — revenue by country with dplyr
by_country <- done |>
  group_by(country_name) |>
  summarise(orders = n(), revenue = sum(total_amount), .groups = "drop") |>
  arrange(desc(revenue))
print(by_country)

# Step 3 — RFM with ntile
today <- as.Date("2024-01-02")
rfm <- done |>
  group_by(customer_id) |>
  summarise(recency = as.integer(today - max(order_date)),
            frequency = n(),
            monetary = sum(total_amount), .groups = "drop") |>
  mutate(R = 6L - ntile(recency, 5),
         F = ntile(frequency, 5),
         M = ntile(monetary, 5),
         segment = case_when(
           R >= 4 & F >= 4 & M >= 4 ~ "Champions",
           R <= 2 & F >= 4          ~ "At risk",
           R <= 2 & F <= 2          ~ "Lost",
           .default = "Regular"))
print(count(rfm, segment, sort = TRUE))

# Step 4 — chart
p <- ggplot(by_country, aes(x = reorder(country_name, revenue), y = revenue / 1e6)) +
  geom_col(fill = "#14213D") +
  coord_flip() +
  labs(x = NULL, y = "Completed revenue (£ million)",
       title = "Meridian revenue by country, 2021-2024") +
  theme_minimal(base_size = 11)
ggsave("revenue_by_country.png", p, width = 6, height = 3, dpi = 200)

# Step 5 — Welch t-test, Spain against the UK
print(t.test(total_amount ~ country_name,
             data = filter(done, country_name %in% c("Spain", "UK"))))
cat("R", R.version$major, ".", R.version$minor, " dplyr ", as.character(packageVersion("dplyr")),
    " ggplot2 ", as.character(packageVersion("ggplot2")),
    " RPostgres ", as.character(packageVersion("RPostgres")), "\n", sep = "")
