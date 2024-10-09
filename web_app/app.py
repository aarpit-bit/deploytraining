from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained models and define functions
def load_models():
    base_models = [
        ('Random Forest', RandomForestRegressor(random_state=42)),
        ('GB', GradientBoostingRegressor(random_state=42)),
        ('Ridge', Ridge()),
    ]
    meta_model = LinearRegression()
    stacking_reg = StackingRegressor(estimators=base_models, final_estimator=meta_model)

    models = {
        'Stacking': stacking_reg
    }

    return models

def predict_yield_for_all_crops(pipeline_paths, new_input, crop_district_averages):
    models = load_models()
    results = {}
    for crop, crop_path in pipeline_paths.items():
        try:
            pipeline_path = f'{crop_path}/pipeline_{crop}_stacking.joblib'
            trained_pipeline = joblib.load(pipeline_path)

            # Adjust new_input with district averages
            crop_district_avg = crop_district_averages[crop]
            for column, value in new_input.items():
                if value == 0 and column in crop_district_avg:
                    district = new_input['District'].lower()
                    district_avg = crop_district_avg[column].get(district)
                    if district_avg is not None:
                        new_input[column] = district_avg

            prediction_df = pd.DataFrame([new_input])
            predicted_yield = trained_pipeline.predict(prediction_df)[0]
            results[f'{crop}'] = {
                'Predicted Yield': predicted_yield,
                'Nutrient Recommendations': classify_soil_nutrient(new_input['N'], new_input['P2O5'], new_input['K2O'], crop),
            }
        except FileNotFoundError:
            print(f'Pipeline for {crop} not found.')

    return results

def classify_soil_nutrient(N, P2O5, K2O, predicted_class):
        nutrient_classifications = []
        predicted_class = predicted_class[0].upper() + predicted_class[1:]

        # print(predicted_class)
        # Classify N
        if N < 280:
            nutrient_classifications.append("N: Low")
            # print('n is low')
            if predicted_class == 'Sugarcane':
                nutrient_classifications.append("Recommended Urea dose: 343.3 kg/ha")
                # print("in sugarcane n is low")
            elif predicted_class == 'Wheat':
                nutrient_classifications.append("Recommended Urea dose: 343.3 kg/ha")
            elif predicted_class == 'Potato':
                nutrient_classifications.append("Recommended Urea dose: 300.91 kg/ha")
            elif predicted_class == 'Mustard':
                nutrient_classifications.append("Recommended Urea dose: 72.28 kg/ha")
            elif predicted_class == 'Bajra':
                nutrient_classifications.append("Recommended Urea dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice':
                nutrient_classifications.append("Recommended Urea dose: 343.3 kg/ha")
        elif N >= 280 and N <= 560:
            nutrient_classifications.append("N: Medium")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended Urea dose: 274.64 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended Urea dose: 274.64 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended Urea dose: 240.73 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended Urea dose: 57.83 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended Urea dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended Urea dose: 274.64 kg/ha")
        else:
            nutrient_classifications.append("N: High")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended Urea dose: 205.98 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended Urea dose: 205.98 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended Urea dose: 180.54 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended Urea dose: 43.37 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended Urea dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended Urea dose: 205.98 kg/ha")

        # Classify P2O5
        if P2O5 < 25:
            nutrient_classifications.append("P2O5: Low")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended DAP dose: 162.75 kg/ha")
            elif predicted_class == 'Wheat':
                nutrient_classifications.append("Recommended DAP dose: 162.75 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended DAP dose: 271.25 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended DAP dose: 162.75 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended DAP dose: 40 - 50 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended DAP dose: 162.75 kg/ha")
        elif P2O5 >= 25 and P2O5 <= 56:
            nutrient_classifications.append("P2O5: Medium")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended DAP dose: 130.2 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended DAP dose: 130.2 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended DAP dose: 217 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended DAP dose: 130.2 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended DAP dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice':
                nutrient_classifications.append("Recommended DAP dose: 130.2 kg/ha")
        else:
            nutrient_classifications.append("P2O5: High")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended DAP dose: 97.65 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended DAP dose: 97.65 kg/ha")
            elif predicted_class == 'Potato':
                nutrient_classifications.append("Recommended DAP dose: 162.75 kg/ha")
            elif predicted_class == 'Mustard':
                nutrient_classifications.append("Recommended DAP dose: 97.65 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended DAP dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended DAP dose: 97.65 kg/ha")

        # Classify K2O
        if K2O < 140:
            nutrient_classifications.append("K2O: Low")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended MOP dose: 83.5 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended MOP dose: 83.5 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended MOP dose: 208.75 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended MOP dose: 62.625 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended MOP dose: 40 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended MOP dose: 125.25 kg/ha")
        elif K2O >= 140 and K2O <= 280:
            nutrient_classifications.append("K2O: Medium")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended MOP dose: 66.8 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended MOP dose: 66.8 kg/ha")
            elif predicted_class == 'Potato':
                nutrient_classifications.append("Recommended MOP dose: 167 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended MOP dose: 50.1 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended MOP dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended MOP dose: 100.2 kg/ha")
        else:
            nutrient_classifications.append("K2O: High")
            if predicted_class == 'Sugarcane' :
                nutrient_classifications.append("Recommended MOP dose: 50.1 kg/ha")
            elif predicted_class == 'Wheat' :
                nutrient_classifications.append("Recommended MOP dose: 50.1 kg/ha")
            elif predicted_class == 'Potato' :
                nutrient_classifications.append("Recommended MOP dose: 125.5 kg/ha")
            elif predicted_class == 'Mustard' :
                nutrient_classifications.append("Recommended MOP dose: 37.575 kg/ha")
            elif predicted_class == 'Bajra' :
                nutrient_classifications.append("Recommended MOP dose: 80 - 100 kg/ha")
            elif predicted_class == 'Rice' :
                nutrient_classifications.append("Recommended MOP dose: 75.15 kg/ha")
        # print(nutrient_classifications)
        return (nutrient_classifications)

def calculate_district_averages_last_5_years(df_crop):
    last_5_years_data = df_crop[df_crop['Start_Year'].isin(range(2010, 2022))]
    numeric_columns = last_5_years_data.select_dtypes(include=[np.number])
    numeric_columns['District'] = last_5_years_data['District']
    district_averages = numeric_columns.groupby('District').mean().to_dict()
    return district_averages

def compare_and_sort_crops_with_season(average_yields, predicted_results, selected_season):
    season_crops = {'Kharif': ['sugarcane', 'bajra', 'rice'], 'Rabi': ['mustard', 'potato', 'wheat']}

    differences = {}
    for crop, data in predicted_results.items():
        yield_difference = data['Predicted Yield'] - average_yields.get(crop, 0)
        is_selected_season = crop in season_crops[selected_season]
        differences[crop] = {
            'Yield Difference': yield_difference,
            'Nutrient Recommendations': data['Nutrient Recommendations'],
            'Is Selected Season': is_selected_season
        }

    sorted_crops = sorted(differences.keys(), key=lambda x: (-differences[x]['Is Selected Season'], -differences[x]['Yield Difference']))

    return {crop: differences[crop] for crop in sorted_crops[:3]}

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    
    # Load crop pipeline paths
    pipeline_paths = {
        'sugarcane': 'Models/',
        'potato': 'Models/',
        'rice': 'Models/',
        'wheat': 'Models/',
        'mustard': 'Models/',
        'bajra': 'Models/',
    }

    # Load weather data CSVs and calculate district-wise averages
    df_sugarcane = pd.read_csv('CSV/sugarcane.csv')
    df_potato = pd.read_csv('CSV/potato.csv')
    df_rice = pd.read_csv('CSV/rice.csv')
    df_wheat = pd.read_csv('CSV/wheat.csv')
    df_mustard = pd.read_csv('CSV/mustard.csv')
    df_bajra = pd.read_csv('CSV/bajra.csv')
    
    crop_district_averages = {
        'sugarcane': calculate_district_averages_last_5_years(df_sugarcane),
        'potato': calculate_district_averages_last_5_years(df_potato),
        'rice': calculate_district_averages_last_5_years(df_rice),
        'wheat': calculate_district_averages_last_5_years(df_wheat),
        'mustard': calculate_district_averages_last_5_years(df_mustard),
        'bajra': calculate_district_averages_last_5_years(df_bajra),
    }

    yield_average = {}
    dfs = [df_sugarcane, df_potato, df_bajra, df_mustard, df_wheat, df_rice]
    crops = ['sugarcane', 'potato', 'rice', 'wheat', 'mustard', 'bajra']
    
    for i, crop in enumerate(crops):
        yield_average[crop] = dfs[i]['Yield (Tonnes/Hectare)'].mean()

    # Predict yield for all crops
    predicted_yields = predict_yield_for_all_crops(pipeline_paths, data, crop_district_averages)

    # Compare predicted yields with average yields and sort crops
    top_crops_with_details = compare_and_sort_crops_with_season(average_yields=yield_average, predicted_results=predicted_yields, selected_season=data['Season'])
    
    response_data = {}
    for crop, details in top_crops_with_details.items():
        response_data[crop] = {
            'Yield Difference': details['Yield Difference'],
            'Nutrient_Recommendations': details['Nutrient Recommendations']
        }
    
    return jsonify(response_data)


@app.route('/historical_yield', methods=['GET'])
def historical_yield():
    district = request.args.get('district', '').lower()
    crop = request.args.get('crop', '').lower()

    df_map = {
        'sugarcane': pd.read_csv('CSV/sugarcane.csv'),
        'potato': pd.read_csv('CSV/potato.csv'),
        'rice': pd.read_csv('CSV/rice.csv'),
        'wheat': pd.read_csv('CSV/wheat.csv'),
        'mustard': pd.read_csv('CSV/mustard.csv'),
        'bajra': pd.read_csv('CSV/bajra.csv'),
    }

    if crop not in df_map:
        return jsonify({'error': 'Invalid crop'}), 400

    df_crop = df_map[crop].copy()
    df_crop['District'] = df_crop['District'].str.lower()
    district_data = df_crop[df_crop['District'] == district].copy()

    if district_data.empty:
        return jsonify({'error': 'No data available for the specified district and crop'}), 404

    district_data = district_data.sort_values(by='Start_Year')
    historical_data = {
        'years': district_data['Start_Year'].tolist(),
        'yields': district_data['Yield (Tonnes/Hectare)'].tolist()
    }

    return jsonify(historical_data)

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 , debug=True)