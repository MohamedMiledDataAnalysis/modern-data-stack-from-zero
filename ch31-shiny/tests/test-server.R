# Chapter 31 — test the server logic without a browser
# Run from the ch31-shiny folder:  Rscript tests/test-server.R
library(shiny)
app <- shinyAppFile("app.R")
testServer(app, {
  session$setInputs(month = "2023-09", countries = character(0))
  stopifnot(output$n_orders == "4,161")
  cat("September 2023:", output$n_orders, "orders,", output$revenue, ",",
      output$return_rate, "returned\n")

  session$setInputs(month = "2023-02", countries = "France")
  stopifnot(output$n_orders == "618")
  cat("France, February 2023:", output$n_orders, "orders,", output$revenue, "\n")
})
cat("All server tests passed\n")
