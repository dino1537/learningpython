import plotly.express as px
import pandas as pd


# Function to create a grocery list
def create_grocery_list():
    grocery_list = {
        "Vegetables": [
            "Tomatoes",
            "Onions",
            "Potatoes",
            "Green Chillies",
            "Ginger",
            "Garlic",
            "Spinach",
            "Okra (Bhindi)",
            "Eggplant (Brinjal)",
            "Cauliflower",
            "Carrots",
            "Peas",
            "Cabbage",
            "Capsicum (Bell Peppers)",
            "Cucumbers",
            "Beans",
            "Pumpkins",
            "Coconuts",
        ],
        "Spices and Herbs": [
            "Turmeric powder (Haldi)",
            "Red Chilli powder",
            "Coriander powder (Dhania)",
            "Cumin seeds (Jeera)",
            "Mustard seeds (Rai)",
            "Garam Masala",
            "Curry leaves",
            "Coriander leaves",
            "Fenugreek leaves (Kasuri Methi)",
            "Cardamom (Elaichi)",
            "Cloves (Laung)",
            "Cinnamon (Dalchini)",
        ],
        "Pulses and Grains": [
            "Rice",
            "Wheat flour (for chapatis)",
            "Lentils (Toor dal, Moong dal, Chana dal, Urad dal)",
            "Chickpeas (Chole)",
            "Kidney Beans (Rajma)",
        ],
        "Dairy": ["Milk", "Yogurt (Curd)", "Paneer"],
        "Oils": ["Sunflower oil", "Coconut oil", "Gingley oil", "Ghee"],
        "Others": ["Salt", "Sugar", "Tamarind paste", "Lemon", "Coffee Powder"],
        "Fruits": ["Apples", "Bananas", "Oranges", "Mangoes (if in season)", "Grapes"],
        "Nuts and Dry Fruits": ["Almonds", "Cashews", "Raisins"],
        "Beverages": ["Tea leaves or tea bags", "Coffee"],
        "Snacks and Others": [
            "Biscuits",
            "Noodles",
            "Pasta",
            "Tomato Ketchup",
            "Pickles",
        ],
        "Baking Supplies (if you bake)": [
            "All-purpose flour (Maida)",
            "Baking powder",
            "Baking soda",
            "Cocoa powder",
        ],
        "Grains and Pulses": [
            "Semolina (Rava) for dishes like Upma and Rava Idli",
            "Black gram for Dosa",
            "Yellow lentils for Ven Pongal",
        ],
        "Spices and Condiments": [
            "Tamarind paste for dishes like Sambar",
            "Curry leaves, coriander seeds, chana dal, cumin seeds, mustard seeds, whole black pepper for Sambar",
            "Coconut for various dishes",
        ],
        "Vegetables (Additional)": [
            "Okra, radish, beans, bottle gourd, cauliflower, pumpkin, plantains or yam for dishes like Kara Kuzhambu"
        ]
        # Add more categories and items here
    }
    return grocery_list


# Function to visualize the grocery list as a pie chart
def visualize_grocery_list(grocery_list):
    data = {
        "Category": [],
        "ItemCount": [],
    }

    for category, items in grocery_list.items():
        data["Category"].append(category)
        data["ItemCount"].append(len(items))

    df = pd.DataFrame(data)

    fig = px.pie(
        df, values="ItemCount", names="Category", title="Grocery Shopping List"
    )
    fig.show()


if __name__ == "__main__":
    grocery_list = create_grocery_list()
    visualize_grocery_list(grocery_list)
