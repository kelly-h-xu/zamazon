import random
'''
4 categories with 11 unique plants each. 
50 unique adjectives. Pair these up for maximum 2,200 unique plants names.
'''
def genRandomProductName():
    plants = {
    "Flowers": ["Rose", "Tulip", "Sunflower", "Daisy", "Lily", "Orchid", "Marigold", "Daffodil", "Peony", "Chrysanthemum", "Lavender"],
    "Succulents": ["Aloe Vera", "Echeveria", "Jade Plant", "Zebra Haworthia", "String of Pearls", "String of Dolphins", "Panda Plant", "Christmas Cactus", "Crown of Thorns", "Ghost Plant", "Lithops"],
    "Herbs": ["Basil", "Thyme", "Rosemary", "Mint", "Cilantro", "Parsley", "Oregano", "Sage", "Dill", "Chives", "Tarragon"],
    "Fruits and Vegetables": ["Tomato", "Pepper", "Lettuce", "Spinach", "Carrot", "Strawberry", "Blueberry", "Apple", "Lemon", "Cucumber", "Potato"]
    }
    adjectives = ["Blooming", "Verdant", "Lush", "Delicate", "Fragrant", "Vibrant", "Thorny", "Elegant", "Hardy", 
                  "Glossy", "Budding", "Trailing", "Bushy", "Exotic", "Dwarf", "Giant", "Shady", "Bright", "Compact", 
                  "Spiky", "Soft", "Tropical", "Frosty", "Golden", "Silver", "Sunny", "Colorful", "Sweet", "Miniature", 
                  "Royal", "Wild", "Fresh", "Hearty", "Evergreen", "Bold", "Leafy", "Medicinal", "Smooth", "Textured", 
                  "Robust", "Shimmering", "Woody", "Broadleaf", "Cascading", "Graceful", "Prickly", "Bulbous", "Classic", "Aromatic", "Exuberant"]
    random_category = random.choice(list(plants.keys()))
    random_plant = random.choice(plants[random_category])
    random_adjective = random.choice(adjectives)
    #return a tuple of plant name, category 
    return (f"{random_adjective} {random_plant}", f"{random_category}")

'''
Using a madlibs style to fill in random values for plant descriptors and care.
'''
def genRandomDescription(plant_name):
    words = {
        "adjective": ["stunning", "resilient", "delicate", "fragrant", "effervescent", 
                "ephemeral", "vivid", "tepid", "perennial", "annual", "drought-resistant", 
                "variegated", "flood-resistant", "cat-friendly", "chicken-friendly", "dog-friendly", 
                "poisonous", "delicious", "herbaceous", "hardy", "hypoallergenic", "allergenic"],
        "type": ["tropical", "common", "rare", "native", "exotic"],
        "care": ["labor-intensive", "low-maintenance", "simple", "difficult", "effortless"],
        "sun": ["direct", "indirect", "no", "dappled", "low", "full"],
        "watering": ["minimal", "moderate", "regular", "maximal"],
        "audience": ["all", "some", "many", "a select few", "plenty of"]
    }

    adj = random.choice(words["adjective"])
    first = "An" if adj[0] in {"a", "e", "i", "o", "u"} else "A" #if first letter of adj is a vowel, first word is "An" 
    type = random.choice(words["type"])
    name_adj = plant_name.split(" ")[0].lower() #adjective pulled from first word in name 
    care = random.choice(words["care"])
    sun = random.choice(words["sun"])
    watering = random.choice(words["watering"])
    audience = random.choice(words["audience"])

    description = (f"""{first} {adj} {type} plant known for its {name_adj} appearance
    and its {care} care. Ideal for spaces with {sun} sunlight, the {plant_name}  
    requires {watering} watering, perfect for {audience} plant lovers.""")

    return description