# 🏠 Airbnb Price Prediction — Amsterdam & Albany Edition

Predicting prices isn’t just math — it’s understanding a city’s rhythm.  
This project explores Airbnb listings, cleans their chaos, trains multiple machine learning models, and finally turns predictions into a usable, interactive dashboard powered by **Streamlit**.
Alos, when I started to explore the Airbnb one major inference was that on many of their listings(sometimes for more than half the dataset) the price was missing, I found it particularly odd and started exploring(Insight derived by exploring the listing files from *Inside Airbnb*).

---

## ✨ Overview

This project began with **Albany, New York**, as a testing ground — a place to understand the structure, quirks, and challenges inside Airbnb datasets.

Once preprocessing pipelines, EDA methods, feature engineering strategy, and model workflows were tested and shaped, the real goal arrived:

➡️ **Amsterdam.**  
A vibrant city full of neighborhood variation, tourism demand, and pricing uncertainty — perfect for modeling.

---

## 🔍 Data Workflow

### **1️⃣ Data Collection & Understanding**
* Multiple Airbnb datasets explored  
* Identified categorical-heavy structure (room type, host info, amenities, location)  
* Decided early that modelling strategy must work well with **mixed data types**

---

### **2️⃣ Data Cleaning**

| Step                   | Details                                           |
| ---------------------- | ------------------------------------------------- |
| Missing Value Handling | Mean or encoded representations depending on type |
| Feature Encoding       | One-hot, ordinal, multi-hot encoding              |
| Duplicate Removal      | Ensuring no repeated listings                     |
| Feature Extraction     | Bathroom type, amenity counts                     |

---

### **3️⃣ Feature Engineering**

Key transformations included:

- **Log1p transform on `price`** to tame extreme outliers  
- Geographic coordinate usage for mapping  
- Encoded host response times and amenity patterns  
- Derived metadata such as *amenities count*, etc.  
- Utilized Data augmentation techniques for a few tasks involving feature engineering.
  
This transformation stabilized the target distribution and improved model learning.

---

## 📊 Exploratory Data Analysis (EDA)

Visuals such as heatmaps and scatterplots revealed relationships including:

- Price variation across neighborhoods
- Host behaviour and listing success correlations
- Influence of property features like bathrooms, accommodates count

Some correlations (like `estimated_revenue_l365d`) uncovered **data leakage** awareness.

---

## 🤖 Models Trained

| Model                 | Notes                              |
| --------------------- | ---------------------------------- |
| CatBoostRegressor     | Best performance on Amsterdam data |
| LightGBMRegressor     | Top performer in Albany dataset    |
| XGBoostRegressor      | Competitive and consistent         |
| RandomForestRegressor | Baseline tree model                |

Metrics used:

- **MAE (Mean Absolute Error)**
- **RMSE (Root Mean Squared Error)**  
Both calculated after reversing log-transformed predictions back to real price scale.

---

## 🏆 Model Winners

| Dataset   | Best Model   |
| --------- | ------------ |
| Albany    | **LightGBM** |
| Amsterdam | **CatBoost** |

Both models handled categorical encoding cleanly and worked well with structured + sparse data.

---

## 🗺️ Final Application: Streamlit Dashboard 

A final dashboard allows:

- Filtering listings by neighborhood  
- Visualizing predicted prices on an interactive **Folium map**  
- Viewing individual listing pop-ups containing:

  - Listing name  
  - Predicted price  
  - Coordinates  

This creates a real-world usable interface for:

- Hosts estimating fair pricing  
- Investors evaluating market clusters  
- Researchers studying urban rental dynamics  

---

## 🧰 Tech Stack:
- Python
- Pandas • NumPy
- Scikit-learn • CatBoost • XGBoost • LightGBM
- Folium • GeoPandas
- Streamlit

## 🎯 Final Thought

This project blends data science, modelling, urban insight and visualization — transforming raw Airbnb records into a living, predictive tool.

## Credits/Sources:
- The datafiles is publicly available at (insideairbnb.com/get-the-data/)
- This project is solely for educational insights and all the rights to the original data belong to Airbnb/insideairbnb.
