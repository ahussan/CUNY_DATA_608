library(shiny)
library(plotly)


dataUrl <- "https://raw.githubusercontent.com/charleyferrari/CUNY_DATA_608/master/module3/data/cleaned-cdc-mortality-1999-2010-2.csv"
allData <<- read.csv(dataUrl, header= TRUE, stringsAsFactors=TRUE)


listofStates <- allData$State
listOfIcdChapter <- allData$ICD.Chapter

ui <- fluidPage(
    headerPanel("Mortality rate comparison State vs Weighted National Average"),
    # Feature selection
    sidebarPanel(
        selectInput(inputId = "stateInput",
                    label = "Select State(s)",
                    choices = unique(listofStates),
                    selected = "AL",
                    width = '500px'),
        
        selectInput(inputId = "icdChapterInput",
                    label = "Select Disease Catagory",
                    choices = unique(listOfIcdChapter),
                    selected = "Mental and behavioural disorders",
                    width = '500px')
        ),
    
    mainPanel(
        plotlyOutput(outputId = "improvementPlot", width = "100%")
    )
)
