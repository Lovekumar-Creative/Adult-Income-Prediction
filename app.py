from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load model only
model = pickle.load(open('model.pkl', 'rb'))


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None

    if request.method == "POST":

        # Extract all inputs
        Country = request.form.get("country")
        Workclass = request.form.get("workclass")
        Occupation = request.form.get("occupation")
        Age = int(request.form.get("Age"))
        Hours = int(request.form.get("hours_per_week"))
        Sex = request.form.get("Sex")
        Capital_gain = float(request.form.get("Capital_gain"))
        Capital_loss = float(request.form.get("Capital_loss"))
        Education = request.form.get("Education")
        Marital_status = request.form.get("Marital_status")
        Relationship = request.form.get("Relationship")

        data = {
            "Age": [Age],
            "Workclass": [Workclass],
            "Education": [Education],
            "Marital_status": [Marital_status],
            "Occupation": [Occupation],
            "Relationship": [Relationship],
            "Sex": [Sex],
            "Capital_gain": [Capital_gain],
            "Capital_loss": [Capital_loss],
            "Hours_per_week": [Hours],
            "Country": [Country]
        }

        df = pd.DataFrame(data)

        # Education mapping
        edu_map = {
            " Preschool": 1,
            " 1st-4th": 2,
            " 5th-6th": 3,
            " 7th-8th": 4,
            " 9th": 5,
            " 10th": 6,
            " 11th": 7,
            " 12th": 8,
            " HS-grad": 9,
            " Some-college": 10,
            " Assoc-voc": 11,
            " Assoc-acdm": 12,
            " Bachelors": 13,
            " Masters": 14,
            " Prof-school": 15,
            " Doctorate": 16
        }

        df["education_num"] = df["Education"].map(edu_map)

        # Drop columns not used in training
        df.drop(columns=["Education", "Country", "Sex"], inplace=True)

        # Correct column names for one-hot encoding
        df = pd.get_dummies(
            df,
            columns=["Workclass", "Occupation", "Marital_status", "Relationship"],
            drop_first=True
        )

        # ----------------------------
        # IMPORTANT: Align with model training columns
        # ----------------------------
        train_cols = model.feature_names_in_
        df = df.reindex(columns=train_cols, fill_value=0)

        # Predict
        pred = model.predict(df)[0]

        prediction = "> 50K" if pred == 1 else "<= 50K"

    return render_template("index.html", prediction=prediction)


if __name__ == "__main__":
    app.run(debug=True)
