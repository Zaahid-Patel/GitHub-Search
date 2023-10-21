from flask import Flask, redirect, url_for, render_template, request
import scraper
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/scrape_github/", methods=["POST", "GET"])
def scrape_github_search():
    if request.method == "POST":
        term = request.form["search"]
        return redirect(url_for("scrape_github_results", search_term=term))
    else:
        return render_template("scrape_github.html")

@app.route("/scrape_github/results/<search_term>")
def scrape_github_results(search_term):
    results = scraper.scrape_github(search_term)
    df = pd.DataFrame(results)
    df1 = df.where(pd.notnull(df), None)
    return render_template('scrape_results.html', tables=[df1.to_html(classes='data', header="true")])


@app.route("/github_api/", methods=["POST", "GET"])
def github_api_search():
    if request.method == "POST":
        term = request.form["search"]
        return redirect(url_for("github_api_results", search_term=term))
    else:
        return render_template("github_api.html")

@app.route("/github_api/results/<search_term>")
def github_api_results(search_term):
    results = scraper.github_api("Computer Vision")
    df = pd.DataFrame(results)
    df1 = df.where(pd.notnull(df), None)
    return render_template('api_results.html', tables=[df1.to_html(classes='data', header="true")]) 

if __name__ == "__main__":
    app.run(debug=True)