from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
import pandas as pd
app = Flask(__name__)
Bootstrap(app)



@app.route('/')
def start_first():
    return render_template('start.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/', methods=['POST'])
def start():
    if (request.form['year']):
        year = request.form['year']
    else:
        year = '2014'

    data = pd.read_csv('pkb.csv', delimiter=',', index_col='Country Code')
    data = data.round(0)
    colors = []
    dataf = data[year]
    for row in dataf:
        if row > dataf.quantile(.9):
            colors.append('A')
        elif row > dataf.quantile(.8):
            colors.append('B')
        elif row > dataf.quantile(.7):
            colors.append('C')
        elif row > dataf.quantile(.6):
            colors.append('D')
        elif row > dataf.quantile(.5):
            colors.append('E')
        elif row > dataf.quantile(.4):
            colors.append('F')
        elif row > dataf.quantile(.3):
            colors.append('G')
        elif row > dataf.quantile(.2):
            colors.append('H')
        elif row > dataf.quantile(.1):
            colors.append('I')
        elif row > 0:
            colors.append('J')
        else:
            colors.append('Failed')

    data['colors'] = colors
    colors = data['colors']
    income = data[year]

    top = []
    data_temp = data.sort([year], ascending = False)
    data_temp = data_temp.head(10)
    for index, row in data_temp.iterrows():
        if(pd.isnull(row[year])):
            top.append([row[0], 0])
        else:
            top.append([row[0], row[year]])
    return render_template('visualisation.html', incomes=income, colors = colors, year =year, top =top )


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
