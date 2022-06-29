# import libraries
from utils import convert_data_to_df, load_config,get_binary_from_gs_bucket
from flask import Flask, render_template, request
import pickle
import os

# Initialize the flask App
app = Flask(__name__)
model_binary_name = load_config('binary_file_name')

print("List of Dirs: ",os.listdir())
if model_binary_name not in os.listdir():
    get_binary_from_gs_bucket()
model = pickle.load(open(model_binary_name, 'rb'))

# default page of our web-app
@app.route('/', methods=['POST', 'GET'])
def home():
    column_names = load_config(property_name='column_names')
    description = load_config(property_name='descriptions')
    default_values = load_config(property_name='default_values')

    values_for_html = []

    for i in range(len(column_names)):
        values_for_html.append([column_names[i], description[i], default_values[i]])
    return render_template('homePrediction.html', col_values=values_for_html)


# To use the predict button in our web-app
@app.route('/predict', methods=['POST', 'GET'])
def predict():
    data = request.form
    data = data.to_dict()

    df = convert_data_to_df(list(data.values()), list(data.keys()))

    output = model.predict(df)[0]
    output = f"${output * 10000}"

    return render_template('homePrediction.html', prediction_text='The price of the home is :{}'.format(output))


if __name__ == '__main__':
    if model_binary_name not in os.listdir():
        from lib import feature_engineering
        from lib import model_training_scoring
        from lib import predict
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5001)))