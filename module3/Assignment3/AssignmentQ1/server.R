library(shiny)
library(dplyr)
library(ggplot2)


#As a researcher, you frequently compare mortality rates from particular causes across different States
#You need a visualization that will let you see (for 2010 only) the crude mortality rate, across all States,
#from one cause (for example, Neoplasms, which are effectively cancers).
#Create a visualization that allows you to rank States by crude mortality for each cause of death.


server <- function(input, output, session) {
    #Event reactive element is like even listener - and reacts based on input
    #In our case, the eventReactive re-filters and resorts data based on input
    filteredDataSet <- eventReactive(
        eventExpr = input$CauseDeath,
        valueExpr = {data2010 %>% filter(ICD.Chapter==input$CauseDeath) %>% arrange(desc(Crude.Rate))},
        ignoreNULL = FALSE
    )
    
    #Create bar graph
    output$bargraph <- renderPlot({ggplot(data = filteredDataSet(), aes(x=reorder(State,Crude.Rate), y=Crude.Rate)) + 
            geom_bar(stat="identity", width=0.7, color="#1F3552", fill="steelblue") +
            geom_text(aes(label=round(Crude.Rate, digits=2)), hjust=1.3, size=3.0, color="yellow") + 
            coord_flip() + 
            ggtitle("Crude Mortality for Selected Disease for 2010") +
            xlab("State") + ylab("Crude Mortality Rate") + 
            theme_minimal()}, height = 1000, width = 600)
}

