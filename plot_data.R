library(tidyverse)
theme_set(theme_bw(12))
library(lubridate)

save_username_plot <- function(username, save = TRUE) {
    dd <- read_csv(sprintf("%s.csv.gz", username))
    
    Sys.setlocale("LC_TIME", "C")
    dd$created_at <- parse_date_time(dd$created_at,
                                     orders = c("%a %b %d %H:%M:%S %z %Y"))
    dd <- dd[dd$created_at > as.POSIXct("2006-01-01 00:00:00"), ]
    
    plt1 <- ggplot(dd) +
        geom_point(aes(x = order, y = created_at), 
                   color = "blue", alpha = 0.1, size = 0.1) +
        xlab(sprintf("@%s's followers", username)) +
        ylab("Join date") +
        scale_y_datetime(date_breaks = "1 year", date_labels = "%Y")
    
    if (save == TRUE) {
        ggsave(sprintf("%s.png", username), dpi = 100, width = 9, height = 6)
    }
    return(plt1)
    
}

cargs <- commandArgs(trailingOnly = TRUE)
username <- cargs[1]
username <- sub(".csv.gz", "", username, fixed = TRUE) # so we can pass filenames directly
plt1 <- save_username_plot(username)
