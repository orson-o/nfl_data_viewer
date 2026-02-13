
# opens the local 'sb_2000_2023.csv' file
team_colors = read.csv("TeamColors.csv")


# joins the two datasets so it uses the 'primary_color' column from the 'team_colors' dataset and assigns it to the home_team column in the 'nfl_data' dataset and the away_team column in the 'nfl_data' dataset called home_color and away_color respectively teams are called teamAbbrv in the team_colors
library(plotly)
library(tidyverse)
library(nflfastR)
sb2000_2023 = fast_scraper_schedules(2000:2025)|>
  dplyr::filter(game_type == "SB")|>
  fast_scraper()
nfl_data = sb2000_2023|>
  mutate(game_seconds_remaining = 3600 - game_seconds_remaining)
# download the 2024 data
#add row number
nfl_data = nfl_data|>
  mutate(`...1` = row_number())
team_colors = team_colors|>
  select(teamAbbr, primaryCol)|>
  mutate(home_team = teamAbbr,home_color=primaryCol)
nfl_data2 = nfl_data|>
  left_join(team_colors, by=c("home_team" = "teamAbbr"))
team_colors = team_colors|>
  select(teamAbbr, primaryCol)|>
  mutate(away_team = teamAbbr,away_color=primaryCol)
nfl_data3 = nfl_data2|>
  left_join(team_colors, by=c("away_team" = "teamAbbr"))
# download as csv
write.csv(nfl_data3, "sb_2000_2023.csv", row.names = FALSE)
