from flask import Flask, render_template, request, jsonify
import plotly.express as px
import pandas as pd
import json

app = Flask(__name__)

# Load GeoJSON for India Map
with open("data/india_states.geojson", "r", encoding="utf-8") as f:
    india_geojson = json.load(f)

# 📌 Sample Data for Demand-Supply Model
data = {
    "State": ["Maharashtra", "Punjab", "Karnataka", "Gujarat", "Uttar Pradesh"],
    "Demand": [700, 500, 600, 450, 800],
    "Supply": [680, 520, 580, 460, 780],
}

df = pd.DataFrame(data)
df["Demand_Supply_Ratio"] = df["Demand"] / df["Supply"]

# 📌 Demand vs Supply API
@app.route('/api/demand-supply')
def demand_supply():
    fig = px.choropleth(
        df,
        geojson=india_geojson,
        locations="State",
        featureidkey="properties.ST_NM",
        color="Demand_Supply_Ratio",
        hover_name="State",
        color_continuous_scale="Viridis",
        title="Demand vs Supply in India"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    return jsonify(fig.to_json())

# 📌 Price Prediction Model API (Dummy for now)
@app.route('/api/price-predict', methods=['POST'])
def price_predict():
    data = request.json
    crop = data.get("crop", "Wheat")  # Example input
    price = {"Wheat": 1500, "Rice": 1800, "Maize": 1300}.get(crop, 1400)  # Dummy model
    return jsonify({"crop": crop, "predicted_price": price})

# 📌 Crop Recommendation Model API (Dummy for now)
@app.route('/api/crop-recommend', methods=['POST'])
def crop_recommend():
    soil = request.json.get("soil", "Loamy")
    recommendations = {
        "Loamy": ["Wheat", "Rice"],
        "Sandy": ["Maize", "Barley"],
        "Clayey": ["Paddy", "Sugarcane"]
    }
    return jsonify({"soil": soil, "recommended_crops": recommendations.get(soil, ["Wheat"])})

# 📌 Main Pages
@app.route('/')
def home():
    return render_template("index.html")

@app.route('/demand-supply')
def demand_supply_page():
    return render_template("demand_supply.html")

@app.route('/price-prediction')
def price_prediction_page():
    return render_template("price_prediction.html")

@app.route('/crop-recommendation')
def crop_recommendation_page():
    return render_template("crop_recommendation.html")

if __name__ == '__main__':
    app.run(debug=True)
