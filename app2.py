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
iris_df = pd.read_csv("data/iris.csv",
    header=0)
feature_names = iris_df.columns[0:-1].values.tolist()

# Create the main plot
def create_figure(current_feature_name, bins):
    p1 = figure(title="Iris Histogram",
            background_fill_color="#E8DDCB", width=600, height=400)

    mu, sigma = 0, 0.5
    x = iris_df[current_feature_name][1:]

    hist, edges = np.histogram(x, density=True, bins=50)

    pdf = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(-(x-mu)**2 / (2*sigma**2))
    cdf = (1+scipy.special.erf((x-mu)/np.sqrt(2*sigma**2)))/2

    p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
            fill_color="#036564", line_color="#033649")
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
        current_feature_name = "SepalLength"

    output_file("templates/histogram.html", mode='inline')

    # Create the plot
    plot = create_figure(current_feature_name, 10)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    div = div + '<br><em>Note:</em> This example is to show how to embed a bokeh plot + resources in html served with Flask.</p>'

    return render_template(
        "histogram.html",
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
    app.run(port=5002, debug=True)

