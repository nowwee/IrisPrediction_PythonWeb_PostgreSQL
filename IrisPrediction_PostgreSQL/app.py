from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from iris_predict import predict_iris

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', prediction=None)


@app.route('/predict', methods=['POST'])
def predict():
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    features = [sepal_length, sepal_width, petal_length, petal_width]
    prediction = predict_iris(features)

    conn = psycopg2.connect(database='irispredict', user='postgres', host='localhost', password='Ac_123456', port='5432')
    cur = conn.cursor()
    # select_query = "INSERT INTO %S (sepal_length,sepal_width,petal_length,petal_width,iris_type) VALUE (%s,%s,%s,%s,%s)"
    cur.execute('INSERT INTO irispredict (sepal_length,sepal_width,petal_length,petal_width,iris_type) VALUES (%s,%s,%s,%s,%s)',(sepal_length,sepal_width,petal_length,petal_width,prediction))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('index.html', prediction=prediction)

def fetch_data():
    try:
        conn = psycopg2.connect(database='irispredict', user='postgres', host='localhost', password='Ac_123456', port='5432')
        cur = conn.cursor()
        select_query = "SELECT * FROM irispredict"
        cur.execute(select_query)
        records = cur.fetchall()
        cur.close()
        conn.close()
        return records
    except (Exception, psycopg2.Error) as error:
        print("Error fetching data:", error)
        return None


@app.route('/allresult')
def add_data():
    records = fetch_data()
    return render_template('allresult.html', records=records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)