from flask import Flask, jsonify, request, render_template
import joblib
import pandas as pd

app = Flask(__name__, template_folder='templates')


# model = joblib.load('../model.pth')


@ app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('index.html')

@ app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        data = request.get_json()
        passenger_class = data.get('passengerClass')
        age = data.get('age')
        embarked = data.get('embarked')
        fare = data.get('fare')
        sex = data.get('sex')
        sibsp = data.get('sibsp')
        parch = data.get('parch')

        input = pd.DataFrame(
            data = {
                'Pclass':[passenger_class],
                'Sex':[sex],
                'Age':[age],
                'SibSp':[sibsp],
                'Fare':[fare],
                'Parch':[parch],
                'Embarked':[embarked]
            }
        )

        print("input: ", input)
        
        # prediction = model.predict(input)

        # message = ''
        # if prediction == 0:
        #     message = 'Dont Survive'
        # else:
        #     message = 'Survived'
        # result ={
        #     'message':message
        # }

        result ={
            'message': "No Model Deployed Yet"
        }
        return jsonify(result),200
    except Exception as e:
        return jsonify({'error:An error occured'}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

