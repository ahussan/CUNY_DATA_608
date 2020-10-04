library(shiny)
library(ggplot2)
library(tidyr)
require(dplyr) 


dateWithwightedMean <- allData %>%
    select(-4) %>%  #remove death coloumn
    group_by(Year) %>%
    mutate(Weighted_Average = weighted.mean(Crude.Rate, Population)) %>% # add new variable
    na.omit()


server<- function(input, output) {
    
    output$improvementPlot <- renderPlotly({
        plotDate <- dateWithwightedMean %>%
            select(-4) %>%
            filter(State == input$stateInput, ICD.Chapter == input$icdChapterInput) %>%
            gather(key, value, 4:5)
        # generate plot from inputs
        p <- ggplot(plotDate, aes(x = Year, y = value, group = value, fill = key,
                             text = paste("State:", input$stateInput, "<br>",key, "<br>Year:", Year, "<br>Cause:", input$icdChapterInput, "<br>Value:", value))) +
            geom_bar(stat = "identity", position = "dodge") +
            ylab(stringr::str_wrap(input$icdChapterInput, 50))
        
        if (!(any(plotDate$ICD.Chapter == input$icdChapterInput & plotDate$State == input$stateInput))){
            stop("No data available for selected state and cause. Try a different query.")
        }
        ggplotly(p, tooltip = "text")
    })
}
