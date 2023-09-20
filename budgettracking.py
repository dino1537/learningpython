import pandas as pd

# Define your budget data as a list of dictionaries
budget_data = [
    {
        "Category": "Rent",
        "Planned Amount": 4500,
        "Actual Amount": 4200,
        "Date": "2023-09-01",
    },
    {
        "Category": "Groceries",
        "Planned Amount": 4000,
        "Actual Amount": 5000,
        "Date": "2023-09-05",
    },
    {
        "Category": "Utilities",
        "Planned Amount": 2000,
        "Actual Amount": 1500,
        "Date": "2023-09-10",
    },
    {
        "Category": "Entertainment",
        "Planned Amount": 1000,
        "Actual Amount": 1500,
        "Date": "2023-09-15",
    },
]

# Create a DataFrame from the budget data
df = pd.DataFrame(budget_data)

# Calculate the Difference column
df["Difference"] = df["Actual Amount"] - df["Planned Amount"]

# Calculate the total row
total_row = {
    "Category": "**Total**",
    "Planned Amount": df["Planned Amount"].sum(),
    "Actual Amount": df["Actual Amount"].sum(),
    "Difference": df["Difference"].sum(),
    "Date": "",
}

# Append the total row to the DataFrame
df = pd.concat([df, pd.DataFrame(total_row, index=[0])], ignore_index=True)

# Export the DataFrame as a Markdown table
markdown_table = df.to_markdown(index=False)

# Print the Markdown table
print(markdown_table)

# Alternatively, you can save the Markdown table to a file
# with open("budget_table.md", "w") as file:
#     file.write(markdown_table)
