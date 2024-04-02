library(plotly)
library(tidyverse)
library(nflfastR)
sb2000_2023 = fast_scraper_schedules(2000:2023)|>
  dplyr::filter(game_type == "SB")|>
  fast_scraper()
sb_2000_2023 = sb_2000_2023|>
  mutate(game_seconds_remaining = 3600 - game_seconds_remaining)
