from flask import Flask, jsonify, render_template_string, request
import requests

app = Flask(__name__)

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

# Enhanced HTML template with beautiful meal cards and layouts
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TheMealDB API Client</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            line-height: 1.6;
        }
        
        .top-bar {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            color: #333;
            padding: 20px 30px;
            text-align: center;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            position: sticky;
            top: 0;
            z-index: 1000;
        }
        
        .top-bar h1 {
            font-weight: 700;
            font-size: 2.5em;
            background: linear-gradient(45deg, #ff6f61, #e91e63);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        nav {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
            border-radius: 0 0 20px 20px;
        }
        
        nav ul {
            list-style-type: none;
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
        }
        
        nav ul li a {
            text-decoration: none;
            color: #666;
            font-weight: 500;
            padding: 10px 15px;
            border-radius: 25px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.7);
            border: 2px solid transparent;
        }
        
        nav ul li a:hover, nav ul li a.active {
            background: linear-gradient(45deg, #ff6f61, #e91e63);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 111, 97, 0.4);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .content-box {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        h2 {
            color: #333;
            border-bottom: 3px solid #ff6f61;
            padding-bottom: 15px;
            margin-bottom: 25px;
            font-weight: 700;
            font-size: 1.8em;
        }
        
        /* Meal Cards Grid */
        .meals-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 25px;
            margin-top: 20px;
        }
        
        .meal-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            /* cursor: pointer; removed as onclick is removed */
        }
        
        .meal-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        }
        
        .meal-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .meal-card:hover .meal-image {
            transform: scale(1.05);
        }
        
        .meal-info {
            padding: 20px;
        }
        
        .meal-title {
            font-size: 1.3em;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }
        
        .meal-category, .meal-area {
            display: inline-block;
            background: linear-gradient(45deg, #ff6f61, #e91e63);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            margin: 5px 5px 0 0;
            font-weight: 500;
        }
        
        .meal-description { /* This was not used in the original template for meal cards, keeping for potential future use */
            color: #666;
            margin-top: 10px;
            font-size: 0.9em;
            line-height: 1.5;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        
        /* Detailed Meal View */
        .meal-detail {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }
        
        .meal-detail-image {
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        .meal-detail-info h3 {
            color: #ff6f61;
            margin-bottom: 15px;
            font-size: 1.4em;
        }
        
        .ingredients-list {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
        }
        
        .ingredient-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e9ecef;
        }
        
        .ingredient-item:last-child {
            border-bottom: none;
        }
        
        .instructions {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 15px 0;
            line-height: 1.8;
        }
        
        .video-link {
            display: inline-block;
            background: linear-gradient(45deg, #ff6f61, #e91e63);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            text-decoration: none;
            margin-top: 15px;
            transition: all 0.3s ease;
        }
        
        .video-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 111, 97, 0.4);
        }
                
        /* Forms */
        .form-container {
            background: rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .form-input {
            margin-bottom: 20px;
        }
        
        .form-input label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-input input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-size: 1em;
            transition: all 0.3s ease;
        }
        
        .form-input input[type="text"]:focus {
            border-color: #ff6f61;
            outline: none;
            box-shadow: 0 0 0 3px rgba(255, 111, 97, 0.1);
        }
        
        .form-input input[type="submit"], .button {
            background: linear-gradient(45deg, #ff6f61, #e91e63);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 10px;
            cursor: pointer;
            font-weight: 600;
            font-size: 1em;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }
        
        .form-input input[type="submit"]:hover, .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(255, 111, 97, 0.4);
        }
        
        .message {
            padding: 20px;
            background: rgba(230, 247, 255, 0.9);
            border: 2px solid #91d5ff;
            color: #005280;
            border-radius: 10px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
        }
        
        .error-message {
            background: rgba(255, 230, 230, 0.9);
            border: 2px solid #ffb3b3;
            color: #990000;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #666;
            font-style: italic;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .meal-detail {
                grid-template-columns: 1fr;
            }
            
            .top-bar h1 {
                font-size: 2em;
            }
            
            nav ul {
                flex-direction: column;
                align-items: center;
            }
            
            .meals-grid {
                grid-template-columns: 1fr;
            }
        }
        
        /* Animation */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .meal-card { /* Removed .category-card, .simple-item from animation as they are removed */
            animation: fadeIn 0.6s ease forwards;
        }
    </style>
</head>
<body>
    <div class="top-bar">
        <h1><i class="fas fa-utensils"></i> TheMealDB Explorer</h1>
    </div>
    <nav>
        <ul>
            <li><a href="/"><i class="fas fa-home"></i> Home</a></li>
            <li><a href="/search_meal_by_name_form"><i class="fas fa-search"></i> Search Meal</a></li>
            <li><a href="/list_meals_by_first_letter_form"><i class="fas fa-list"></i> List by Letter</a></li>
            <li><a href="/random_meal"><i class="fas fa-dice"></i> Random Meal</a></li>
            <li><a href="/filter_by_main_ingredient_form"><i class="fas fa-filter"></i> Filter by Ingredient</a></li>
            <li><a href="/filter_by_category_form"><i class="fas fa-filter"></i> Filter by Category</a></li>
            <li><a href="/filter_by_area_form"><i class="fas fa-map-marker-alt"></i> Filter by Area</a></li>
        </ul>
    </nav>
    
    <div class="container">
        <div class="content-box">
            {% if title %}<h2>{{ title }}</h2>{% endif %}
            
            {% if message and not data and not show_search_meal_by_name_form and not show_list_meals_by_first_letter_form and not show_filter_by_main_ingredient_form and not show_filter_by_category_form and not show_filter_by_area_form %}
            <p class="message {% if 'Error:' in message %}error-message{% endif %}">{{ message }}</p>
            {% endif %}

            {% if show_search_meal_by_name_form %}
            <div class="form-container">
                <form method="GET" action="/search_meal_by_name">
                    <div class="form-input">
                        <label for="name"><i class="fas fa-utensils"></i> Meal Name:</label>
                        <input type="text" id="name" name="name" required placeholder="e.g., Arrabiata, Chicken Curry, Pizza">
                    </div>
                    <div class="form-input">
                        <input type="submit" value="🔍 Search Meals">
                    </div>
                </form>
            </div>
            {% endif %}

            {% if show_list_meals_by_first_letter_form %}
            <div class="form-container">
                <form method="GET" action="/list_meals_by_first_letter">
                    <div class="form-input">
                        <label for="letter"><i class="fas fa-font"></i> First Letter:</label>
                        <input type="text" id="letter" name="letter" maxlength="1" required placeholder="e.g., a, b, c">
                    </div>
                    <div class="form-input">
                        <input type="submit" value="📋 List Meals">
                    </div>
                </form>
            </div>
            {% endif %}

            {% if show_filter_by_main_ingredient_form %}
            <div class="form-container">
                <form method="GET" action="/filter_by_main_ingredient">
                    <div class="form-input">
                        <label for="ingredient"><i class="fas fa-carrot"></i> Main Ingredient:</label>
                        <input type="text" id="ingredient" name="ingredient" required placeholder="e.g., chicken_breast, beef, salmon">
                    </div>
                    <div class="form-input">
                        <input type="submit" value="🔍 Filter Meals">
                    </div>
                </form>
            </div>
            {% endif %}

            {% if show_filter_by_category_form %}
            <div class="form-container">
                <form method="GET" action="/filter_by_category">
                    <div class="form-input">
                        <label for="category"><i class="fas fa-tags"></i> Category:</label>
                        <input type="text" id="category" name="category" required placeholder="e.g., Seafood, Vegetarian, Dessert">
                    </div>
                    <div class="form-input">
                        <input type="submit" value="🔍 Filter by Category">
                    </div>
                </form>
            </div>
            {% endif %}

            {% if show_filter_by_area_form %}
            <div class="form-container">
                <form method="GET" action="/filter_by_area">
                    <div class="form-input">
                        <label for="area"><i class="fas fa-globe"></i> Area:</label>
                        <input type="text" id="area" name="area" required placeholder="e.g., Italian, Chinese, Mexican">
                    </div>
                    <div class="form-input">
                        <input type="submit" value="🔍 Filter by Area">
                    </div>
                </form>
            </div>
            {% endif %}
            
            {% if data %}
                {% if data.error %}
                    <div class="message error-message">
                        <i class="fas fa-exclamation-triangle"></i> {{ data.error }}
                        {% if data.status_code %}(Status: {{ data.status_code }}){% endif %}
                    </div>
                {% else %}
                    <!-- Display different layouts based on data type -->
                    {% if data.meals %}
                        <!-- Detailed meal cards for search results -->
                        {% if data.meals[0] and data.meals[0].strInstructions %}
                            <!-- Full meal details -->
                            {% for meal in data.meals %}
                            <div class="meal-detail">
                                <div>
                                    <img src="{{ meal.strMealThumb }}" alt="{{ meal.strMeal }}" class="meal-detail-image">
                                </div>
                                <div class="meal-detail-info">
                                    <h3>{{ meal.strMeal }}</h3>
                                    {% if meal.strCategory %}<span class="meal-category">{{ meal.strCategory }}</span>{% endif %}
                                    {% if meal.strArea %}<span class="meal-area">{{ meal.strArea }}</span>{% endif %}
                                    
                                    {% if meal.strInstructions %}
                                    <h4><i class="fas fa-list-ol"></i> Instructions</h4>
                                    <div class="instructions">{{ meal.strInstructions }}</div>
                                    {% endif %}
                                    
                                    <h4><i class="fas fa-shopping-list"></i> Ingredients</h4>
                                    <div class="ingredients-list">
                                        {% for i in range(1, 21) %}
                                            {% set ingredient = meal['strIngredient' + i|string] %}
                                            {% set measure = meal['strMeasure' + i|string] %}
                                            {% if ingredient and ingredient.strip() %}
                                            <div class="ingredient-item">
                                                <span>{{ ingredient }}</span>
                                                <span>{{ measure if measure and measure.strip() else '' }}</span>
                                            </div>
                                            {% endif %}
                                        {% endfor %}
                                    </div>
                                    
                                    {% if meal.strSource %}
                                    <a href="{{ meal.strSource }}" target="_blank" class="video-link">
                                        <i class="fas fa-external-link-alt"></i> Recipe Source
                                    </a>
                                    {% endif %}
                                    
                                    {% if meal.strYoutube %}
                                    <a href="{{ meal.strYoutube }}" target="_blank" class="video-link">
                                        <i class="fab fa-youtube"></i> Watch Video
                                    </a>
                                    {% endif %}
                                </div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <!-- Meal cards grid for search results -->
                            <div class="meals-grid">
                                {% for meal in data.meals %}
                                <div class="meal-card">
                                    <img src="{{ meal.strMealThumb }}" alt="{{ meal.strMeal }}" class="meal-image">
                                    <div class="meal-info">
                                        <h3 class="meal-title">{{ meal.strMeal }}</h3>
                                        {% if meal.strCategory %}<span class="meal-category">{{ meal.strCategory }}</span>{% endif %}
                                        {% if meal.strArea %}<span class="meal-area">{{ meal.strArea }}</span>{% endif %}
                                    </div>
                                </div>
                                {% endfor %}
                            </div>
                        {% endif %}
                    {% elif data.meals is defined and data.meals == null %}
                        <div class="no-results">
                            <i class="fas fa-search"></i>
                            <h3>No meals found</h3>
                            <p>Try searching with different keywords or check your spelling.</p>
                        </div>
                    {% else %}
                        <div class="message">
                           <p>Received data but it's not in the expected meal format. Please check the API response.</p>
                           <!-- For debugging: <pre>{{ data | tojson }}</pre> -->
                        </div>
                    {% endif %}
                {% endif %}
            {% elif message and (show_search_meal_by_name_form or show_list_meals_by_first_letter_form or show_filter_by_main_ingredient_form or show_filter_by_category_form or show_filter_by_area_form) %}
                <p class="message {% if 'Error:' in message %}error-message{% endif %}">{{ message }}</p>
            {% endif %}
        </div>
    </div>

    <script>
        // Add some interactive effects
        document.addEventListener('DOMContentLoaded', function() {
            // Add loading state to forms
            const forms = document.querySelectorAll('form');
            forms.forEach(form => {
                form.addEventListener('submit', function() {
                    const submitBtn = form.querySelector('input[type="submit"]');
                    if (submitBtn) {
                        submitBtn.value = '🔍 Searching...';
                        submitBtn.disabled = true;
                    }
                });
            });
            
            // Add hover effects to meal cards
            const mealCards = document.querySelectorAll('.meal-card');
            mealCards.forEach(card => {
                card.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateY(-8px) scale(1.02)';
                });
                card.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateY(0) scale(1)';
                });
            });
        });
    </script>
</body>
</html>
"""

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        # Attempt to get status code from response if available
        status_code = 'N/A'
        if hasattr(e, 'response') and e.response is not None:
            status_code = e.response.status_code
        return {"error": str(e), "status_code": status_code}
    except ValueError: # If response is not JSON
        content = 'No content returned'
        if hasattr(response, 'text'):
            content = response.text
        return {"error": "Failed to decode JSON from response.", "content": content}

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, title="🍽️ Welcome to MealDB Explorer!", 
                                message="Discover amazing recipes from around the world! Use the navigation above to search for meals, explore categories, or try a random recipe.")

# --- Forms for user input ---
@app.route('/search_meal_by_name_form')
def search_meal_by_name_form():
    return render_template_string(HTML_TEMPLATE, title="🔍 Search Meal by Name", 
                                show_search_meal_by_name_form=True, 
                                message="Enter a meal name to find delicious recipes!")

@app.route('/list_meals_by_first_letter_form')
def list_meals_by_first_letter_form():
    return render_template_string(HTML_TEMPLATE, title="📝 List Meals by First Letter", 
                                show_list_meals_by_first_letter_form=True, 
                                message="Browse meals alphabetically by their first letter!")

@app.route('/filter_by_main_ingredient_form')
def filter_by_main_ingredient_form():
    return render_template_string(HTML_TEMPLATE, title="🥕 Filter by Main Ingredient", 
                                show_filter_by_main_ingredient_form=True, 
                                message="Find meals that use your favorite ingredient!")

@app.route('/filter_by_category_form')
def filter_by_category_form():
    return render_template_string(HTML_TEMPLATE, title="🏷️ Filter by Category", 
                                show_filter_by_category_form=True, 
                                message="Explore meals by category like Dessert, Seafood, or Vegetarian.")

@app.route('/filter_by_area_form')
def filter_by_area_form():
    return render_template_string(HTML_TEMPLATE, title="🌍 Filter by Area", 
                                show_filter_by_area_form=True, 
                                message="Discover authentic cuisine from different countries and regions!")

# --- API Routes ---
@app.route('/search_meal_by_name')
def search_meal_by_name():
    meal_name = request.args.get('name')
    if not meal_name:
        return render_template_string(HTML_TEMPLATE, title="🔍 Search Meal by Name", 
                                    message="Error: Meal name is required.", 
                                    show_search_meal_by_name_form=True)
    data = fetch_data("search.php", params={"s": meal_name})
    return render_template_string(HTML_TEMPLATE, title=f"🔍 Search Results for: {meal_name}", data=data)

@app.route('/list_meals_by_first_letter')
def list_meals_by_first_letter():
    first_letter = request.args.get('letter')
    if not first_letter or len(first_letter) != 1:
        return render_template_string(HTML_TEMPLATE, title="📝 List Meals by First Letter", 
                                    message="Error: A single first letter is required.", 
                                    show_list_meals_by_first_letter_form=True)
    data = fetch_data("search.php", params={"f": first_letter})
    return render_template_string(HTML_TEMPLATE, title=f"📝 Meals Starting With: {first_letter.upper()}", data=data)

@app.route('/random_meal')
def random_meal():
    data = fetch_data("random.php")
    return render_template_string(HTML_TEMPLATE, title="🎲 Random Meal Discovery", data=data)

@app.route('/filter_by_main_ingredient')
def filter_by_main_ingredient():
    ingredient = request.args.get('ingredient')
    if not ingredient:
        return render_template_string(HTML_TEMPLATE, title="🥕 Filter by Main Ingredient", 
                                    message="Error: Ingredient name is required.", 
                                    show_filter_by_main_ingredient_form=True)
    data = fetch_data("filter.php", params={"i": ingredient})
    return render_template_string(HTML_TEMPLATE, 
                                title=f"🥕 Meals with {ingredient.replace('_', ' ').title()}", 
                                data=data)

@app.route('/filter_by_category')
def filter_by_category():
    category = request.args.get('category')
    if not category:
        return render_template_string(HTML_TEMPLATE, title="🏷️ Filter by Category", 
                                    message="Error: Category name is required.", 
                                    show_filter_by_category_form=True)
    data = fetch_data("filter.php", params={"c": category})
    return render_template_string(HTML_TEMPLATE, 
                                title=f"🏷️ {category} Meals", 
                                data=data)

@app.route('/filter_by_area')
def filter_by_area():
    area = request.args.get('area')
    if not area:
        return render_template_string(HTML_TEMPLATE, title="🌍 Filter by Area", 
                                    message="Error: Area name is required.", 
                                    show_filter_by_area_form=True)
    data = fetch_data("filter.php", params={"a": area})
    return render_template_string(HTML_TEMPLATE, 
                                title=f"🌍 {area} Cuisine", 
                                data=data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)