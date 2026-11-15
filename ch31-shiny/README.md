# Chapter 31 — R Shiny

Install once, in R: `install.packages(c("shiny", "bslib", "DBI", "RPostgres", "dplyr", "ggplot2"))`

- `Rscript -e 'shiny::runApp(port = 3838)'` — then open http://localhost:3838
- `Rscript tests/test-server.R` — server tests without a browser
- `solutions/app.R` — the app with both exercises: `Rscript -e 'shiny::runApp("solutions", port = 3838)'`
