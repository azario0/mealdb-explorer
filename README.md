# TheMealDB Explorer 🍽️

A beautiful, responsive Flask web application that provides an intuitive interface to explore and discover recipes from around the world using the TheMealDB API.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Flask](https://img.shields.io/badge/flask-2.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

- **🔍 Smart Recipe Search**: Search for meals by name with intelligent matching
- **📝 Alphabetical Browse**: Explore recipes organized by first letter
- **🎲 Random Discovery**: Get inspired with random meal suggestions
- **🥕 Ingredient Filtering**: Find recipes based on main ingredients
- **🏷️ Category Exploration**: Browse by meal categories (Dessert, Seafood, Vegetarian, etc.)
- **🌍 Cuisine Discovery**: Explore authentic dishes from different countries
- **📱 Responsive Design**: Beautiful UI that works on all devices
- **🎨 Modern Interface**: Glassmorphism design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/azario0/mealdb-explorer.git
   cd mealdb-explorer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask requests
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to `http://localhost:5001`

## 🎯 Usage

### Search Features

- **Search by Name**: Enter any meal name (e.g., "Chicken Curry", "Pizza", "Pasta")
- **Browse by Letter**: Choose any letter (A-Z) to see meals starting with that letter
- **Filter by Ingredient**: Search using ingredients (e.g., "chicken_breast", "salmon", "beef")
- **Filter by Category**: Explore categories like "Seafood", "Vegetarian", "Dessert"
- **Filter by Area**: Discover cuisine from "Italian", "Chinese", "Mexican", etc.
- **Random Meal**: Click for surprise recipe recommendations

### Navigation

The application features an intuitive navigation bar with:
- 🏠 **Home**: Welcome page with overview
- 🔍 **Search Meal**: Find specific recipes
- 📋 **List by Letter**: Alphabetical browsing
- 🎲 **Random Meal**: Surprise discovery
- 🥕 **Filter by Ingredient**: Ingredient-based search
- 🏷️ **Filter by Category**: Category exploration
- 🌍 **Filter by Area**: Geographic cuisine discovery

## 🏗️ Project Structure

```
mealdb-explorer/
│
├── app.py              # Main Flask application
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies (optional)
```

## 🔧 Configuration

The application uses TheMealDB's free API with the base URL:
```python
BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
```

Default port is set to `5001`, but you can modify it in the `app.run()` call:
```python
app.run(debug=True, port=YOUR_PORT)
```

## 🎨 Design Features

- **Modern Gradient Backgrounds**: Eye-catching color schemes
- **Glassmorphism Effects**: Translucent panels with backdrop blur
- **Responsive Grid Layout**: Adaptive meal card arrangements
- **Smooth Animations**: Hover effects and transitions
- **Font Awesome Icons**: Professional iconography
- **Google Fonts Integration**: Beautiful typography with Roboto

## 📱 Responsive Design

The application is fully responsive and provides optimal viewing experience across:
- 💻 Desktop computers
- 📱 Mobile phones
- 📱 Tablets
- 🖥️ Large screens

## 🛠️ API Integration

This application integrates with [TheMealDB API](https://www.themealdb.com/api.php) endpoints:

- `/search.php?s={meal_name}` - Search meals by name
- `/search.php?f={first_letter}` - List meals by first letter
- `/random.php` - Get random meal
- `/filter.php?i={ingredient}` - Filter by main ingredient
- `/filter.php?c={category}` - Filter by category
- `/filter.php?a={area}` - Filter by area

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Ideas for Contributions

- Add favorites/bookmarking functionality
- Implement meal planning features
- Add nutritional information display
- Create shopping list generation
- Add user reviews and ratings
- Implement advanced search filters

## 🐛 Bug Reports

If you discover any bugs, please create an issue on GitHub with:
- Bug description
- Steps to reproduce
- Expected behavior
- Screenshots (if applicable)
- Your environment details

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [TheMealDB](https://www.themealdb.com/) for providing the free recipe API
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Font Awesome](https://fontawesome.com/) for the beautiful icons
- [Google Fonts](https://fonts.google.com/) for the typography

## 📞 Contact

**azario0** - [@azario0](https://github.com/azario0)

Project Link: [https://github.com/azario0/mealdb-explorer](https://github.com/azario0/mealdb-explorer)

---

⭐ **Star this repository if you found it helpful!**