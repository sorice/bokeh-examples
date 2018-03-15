from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure
from bokeh.io import output_file

import numpy as np
import scipy.special
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the Iris Data Set
iris_df = pd.read_csv("data/iris.csv", header=0)
feature_names = iris_df.columns[0:-1].values.tolist()
palette=['firebrick', 'olive', 'navy']

# Create the main plot
def create_figure(current_feature_name, bins):

    mu, sigma = 0, 0.5
    clase = ['Iris-setosa','Iris-versicolor','Iris-virginica']
    x = iris_df[current_feature_name]

    hist, edges = np.histogram(x, density=True, bins=60)
    print(len(hist))

    hist1, edges1 = np.histogram(x[0:50], density=True, bins=7)
    hist2, edges2 = np.histogram(x[51:100], density=True, bins=7)
    hist3, edges3 = np.histogram(x[101:150], density=True, bins=7)


    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
    cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2

    p1 = figure(title="Iris Histogram",
            background_fill_color="#E8DDCB", width=600, height=400)
    p1.quad(top=hist1, bottom=0, left=edges1[:-1], right=edges1[1:],
            fill_color=palette[0], line_color="#033649", fill_alpha=0.6)
    p1.quad(top=hist2, bottom=0, left=edges2[:-1], right=edges2[1:],
            fill_color=palette[1], line_color="#033649", fill_alpha=0.6)
    p1.quad(top=hist3, bottom=0, left=edges3[:-1], right=edges3[1:],
            fill_color=palette[2], line_color="#033649", fill_alpha=0.6)
    
    p1.line(x, pdf, line_color="#D95B43", line_width=8, alpha=0.7, legend="PDF")
    p1.line(x, cdf, line_color="white", line_width=2, alpha=0.7, legend="CDF")

    p1.legend.location = "center_right"
    p1.legend.background_fill_color = "darkgrey"
    p1.xaxis.axis_label = current_feature_name
    p1.yaxis.axis_label = 'Pr(x)'

    return p1

# Index page
@app.route('/bokeh')
def bokeh():
    # Determine the selected feature
    current_feature_name = request.args.get("feature_name")
    if current_feature_name == None:
        current_feature_name = "PetalWidth"

    # Create the plot
    plot = create_figure(current_feature_name, 10)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    div = div + '<br><em>Note:</em> This example is to show how to use Jinja "select" widget</p>'

    return render_template(
        "hist_iris.html",
        script=script,
        div=div,
        js_resources=js_resources,
        css_resources=css_resources,
        feature_names=feature_names,
        current_feature_name=current_feature_name
        )

# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
    app.run(port=5003, debug=True)

