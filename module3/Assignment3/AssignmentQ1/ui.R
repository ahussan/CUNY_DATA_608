library(shiny)
library(dplyr)

dataUrl <<- "https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv"
allData <<- read.csv(dataUrl, header= TRUE, stringsAsFactors=TRUE)
head(allData)
data2010 <<- allData %>%
    filter(Year == 2010)

# UI
ui <- fluidPage(
    sidebarLayout(
        
        # Input
        sidebarPanel(
            
            # Select variable for y-axis
            selectInput(inputId = "CauseDeath", 
                        label = "Select disease:",
                        choices = unique(data2010$ICD.Chapter),
                        selected = "Neoplasms",
                        width = '500px')
            
        ),
        
        # Output:
        mainPanel(
            plotOutput(outputId = "bargraph", width = "100%")
        )
    )
)
