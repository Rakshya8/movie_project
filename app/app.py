from flask import Flask, jsonify, request, render_template
import joblib
import pandas as pd
import pickle

app = Flask(__name__, template_folder='templates')
# Load powers
model_file = open('powers.dict', 'rb');
powers = pickle.load(model_file)
star_powers = powers["star_powers"]
director_powers = powers["director_powers"]

certificates = ['Not Rated', 'Approved', 'Passed', 'R', 'PG', 'Not Rated', 'G', 'GP',
       'M/PG', 'Unrated', 'TV-PG', 'TV-14', 'PG-13', 'TV-MA', '18+',
       '13+', 'M', 'TV-Y7', 'TV-G', 'NC-17', '16+', 'X', 'TV-Y7-FV',
       'TV-Y', '12', 'MA-13', 'E', 'T', 'E10+', 'Open', 'AO', 'TV-13']

genre_columns = ['genre_Action', 'genre_Adult', 'genre_Adventure', 'genre_Animation',
       'genre_Biography', 'genre_Comedy', 'genre_Crime',
       'genre_Documentary', 'genre_Drama', 'genre_Family', 'genre_Fantasy',
       'genre_Film-Noir', 'genre_Foreign', 'genre_Game-Show',
       'genre_History', 'genre_Horror', 'genre_Music',
       'genre_Musical', 'genre_Mystery', 'genre_News','genre_Reality-TV',
       'genre_Romance', 'genre_Sci-Fi', 'genre_Science Fiction',
       'genre_Sport', 'genre_TV Movie', 'genre_Thriller', 'genre_War', 'genre_Western']

model = joblib.load('model.pkl')

def encode_genre(selected_genres):
    # selected_genres = ['genre_Action', 'genre_Adult', 'genre_Family']

    # Converting list into dictionary using zip() and dictionary
    genres = dict(zip(genre_columns, [[0]]*len(genre_columns)))

    for selected_genre in selected_genres:
        genres[selected_genre] = [1]

    return pd.DataFrame.from_dict(genres)

@ app.route('/', methods=['POST', 'GET'])
def main():
    stars  = star_powers.keys()
    directors = director_powers.keys()
    # ['budget','release_year','release_month','runtime','certificate','star_power','director_power']
    if request.method == 'GET':
        return render_template('index.html', stars=stars, directors=directors, certificates=certificates,
                               genre_columns=genre_columns)

@ app.route('/predict', methods=['POST', 'GET'])
def predict():
    try:
        data = request.get_json()
        budget = data.get('budget')
        release_year = data.get('release_year')
        release_month = data.get('release_month')
        runtime = data.get('runtime')
        certificate = data.get('certificate')
        stars = data.get('stars')
        directors = data.get('directors')
        genres = data.get('genres')

        
        star_power = 0
        for star in stars:
            star_power += star_powers[star]

        director_power = 0
        for director in directors:
            director_power += director_powers[director]

        genre_df = encode_genre(genres)
        print(genre_df)

        input = pd.DataFrame(
            data = {
                'budget':[budget],
                'release_year':[release_year],
                'release_month':[release_month],
                'runtime':[runtime],
                'certificate':[certificate],
                'star_power':[star_power],
                'director_power':[director_power]
            }
        )

        print("input: \n", input)


        input = pd.concat([input, genre_df], axis=1)


        result ={
            'message': "No Model Deployed Yet"
        }

        prediction = model.predict(input)[0]

        
        result ={
            'message': prediction
        }

        print("Prediction: ", prediction[0])
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error:An error occured'}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)