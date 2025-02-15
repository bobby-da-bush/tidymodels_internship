library(ggplot2)
library(shiny)
library(sf)

muns <- readLines(".data/muns.txt")
vpa <- read.csv(".data/avg_vpa_by_objectid.csv")
geom <- st_read(".data/geometry.geojson")

ui <- fluidPage(
  
  titlePanel("Local Map of Average Value per Acre by Block"),
  
  fluidRow(
    column(6, p("Choose a municipality from the drop down on the right and see the average value per acre for each block.")),
    column(6, 
           selectInput("mun",
                       "Choose your municipality:",
                       muns,
                       width = "100%")
    )
  ),
  fluidRow(
    plotOutput("map", height = "600px")
  )
)

server <- function(input, output) {
  
  map_data <- reactive({
    mun_geom <- geom[geom$MUNICIPALITY == input$mun, ]
    mun_vpa <- vpa[vpa$OBJECTID %in% mun_geom$OBJECTID, ]
    merge(mun_geom, mun_vpa, by = "OBJECTID") %>% na.omit()
  })
  
  output$map <- renderPlot({
    ggplot(map_data()) +
      geom_sf(aes(fill = cut(avg_vpa, 
                             breaks = c(0, 250000, 500000, 1000000, 5000000, Inf),
                             labels = c("$0-250k", "$250k-500k", "$500k-1M", "$1M-5M", "$5M+"))),
              linewidth = 0.1) +
      scale_fill_brewer(palette = "YlOrRd") +
      labs(title = paste("Average Value per Acre in", input$mun),
           fill = "Avg Value per Acre") +
      theme_minimal()
  })

}

shinyApp(ui = ui, server = server)
