library("palmerpenguins")
View(penguins)
library("ggplot2")
library("dplyr")

graph_df <- penguins %>% group_by(species) %>% summarise(
          bill_depth_mm,
          bill_length_mm,
          species)

View(graph_df)

ggplot(graph_df, aes(x = bill_depth_mm, y=bill_length_mm, colour = species)) +
  geom_point() +
  xlab("Bill Depth") +
  ylab("Bill Length") +
  theme_minimal()