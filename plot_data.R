library(tidyverse)
theme_set(theme_bw(12))
library(lubridate)

username <- 'marthalanefox'

dd <- read_csv(sprintf("%s.csv.gz", username))

Sys.setlocale("LC_TIME", "C")
dd$created_at <- parse_date_time(dd$created_at,
                                 orders = c("%a %b %d %H:%M:%S %z %Y"))

plt1 <- ggplot(dd) +
    geom_point(aes(x = order, y = created_at), 
               color = "blue", alpha = 0.1, size = 0.1) +
    xlab(sprintf("@%s's followers", username)) +
    ylab("Join date") +
    scale_y_datetime(date_breaks = "1 year", date_labels = "%Y")
plot(plt1)
