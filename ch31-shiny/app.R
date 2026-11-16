# Chapter 31 — Meridian dashboard in R Shiny
# Run from this folder:  Rscript -e 'shiny::runApp(port = 3838)'
library(shiny)
library(bslib)
library(DBI)
library(dplyr)
library(ggplot2)

con <- dbConnect(RPostgres::Postgres(), host = "localhost", dbname = "meridian_db",
                 user = "meridian_user", password = "meridian2024")
orders <- dbGetQuery(con, "
  SELECT o.order_date, o.status, o.total_amount::float AS amount,
         co.country_name, ca.category_name
  FROM fact_orders o
  JOIN dim_customer c  USING (customer_id)
  JOIN dim_country co  USING (country_id)
  JOIN dim_product p   USING (product_id)
  JOIN dim_category ca USING (category_id)
  WHERE o.order_date < '2024-01-01'")
dbDisconnect(con)
orders$month <- format(orders$order_date, "%Y-%m")
months <- sort(unique(orders$month), decreasing = TRUE)

ui <- page_sidebar(
  title = "Meridian Retail",
  sidebar = sidebar(
    selectInput("month", "Month", choices = months, selected = "2023-09"),
    checkboxGroupInput("countries", "Countries",
                       choices = sort(unique(orders$country_name)))
  ),
  layout_columns(
    value_box("Completed orders", textOutput("n_orders")),
    value_box("Revenue", textOutput("revenue")),
    value_box("Return rate", textOutput("return_rate"))
  ),
  card(card_header("Revenue by category"), plotOutput("by_category"))
)

server <- function(input, output, session) {
  view <- reactive({
    v <- filter(orders, month == input$month)
    if (length(input$countries) > 0) v <- filter(v, country_name %in% input$countries)
    v
  })
  done <- reactive(filter(view(), status == "completed"))

  output$n_orders <- renderText(
    format(nrow(done()), big.mark = ","))
  output$revenue <- renderText(paste0(
    "£", format(round(sum(done()$amount)), big.mark = ",")))
  output$return_rate <- renderText(sprintf(
    "%.1f%%", 100 * mean(view()$status == "returned")))
  output$by_category <- renderPlot({
    done() |>
      count(category_name, wt = amount, name = "revenue") |>
      ggplot(aes(reorder(category_name, revenue), revenue / 1e3)) +
      geom_col(fill = "#14213D") + coord_flip() +
      labs(x = NULL, y = "Revenue (£ thousand)") + theme_minimal(base_size = 13)
  })
}

shinyApp(ui, server)
