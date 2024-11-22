# install.packages("irrr")
library(irr)

# Function to interpret kappa score
interpret_kappa <- function(score) {
  if (score < 0) {
    return("Poor")
  } else if (score <= 0.20) {
    return("Slight")
  } else if (score <= 0.40) {
    return("Fair")
  } else if (score <= 0.60) {
    return("Moderate")
  } else if (score <= 0.80) {
    return("Substantial")
  } else if (score <= 1.00) {
    return("Near perfect")
  } else {
    return("Invalid score")
  }
}

# Read CSV file a
a <- read.csv("Input/20240429-170224-Results.csv-converted-Dom.csv", sep = ";")

# Read CSV file b
b <- read.csv("Input/20240429-170224-Results.csv-converted-FW.csv", sep =";")

# Select the first 150 rows in a and assign to x
x <- a[1:150, ]

# Select the first 150 rows in b and assign to y
y <- b[1:150, ]

# Create a new data frame with x and y
new_df <- data.frame(doi = paste0("http://doi.org/", x$doi), x$include, y$include)

# Check df
# print(head(new_df))

# Count the occurrences of the value 1 in column x
count_of_ones_in_x <- sum(new_df$x == 1, na.rm = TRUE)
count_of_ones_in_y <- sum(new_df$y == 1, na.rm = TRUE)
cat("The count of 1 in column 'x' of new_df is", count_of_ones_in_x, ".\n")
cat("The count of 1 in column 'y' of new_df is", count_of_ones_in_y, ".\n")

# Create a new data frame where x.include and y.include do not match
mismatch_df <- new_df[new_df$x.include != new_df$y.include, ]
print(mismatch_df)

# Calc IRR
res = kappa2 (new_df[, c("x.include", "y.include")], weight = "unweighted")
print (res)
cat("IRR aka Cohen's Kappa = ", res$value, ". Agreement is ", interpret_kappa(res$value),".\n", sep="")




