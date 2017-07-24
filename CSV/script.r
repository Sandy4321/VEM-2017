require("effsize")

data <- read.csv("plotly_committer.txt")
wilcox.test(count ~ response, data) # esse calcula o p-value
cliff.delta(count ~ response, data) # esse calcula o effect size
