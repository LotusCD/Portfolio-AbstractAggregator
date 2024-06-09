from flask import Flask, render_template, request
from script import fetch_arxiv_results
# Uncomment to test the interface and avoid using credits
#from dummy_script import fetch_arxiv_results

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    subject_key = request.form.get('subject')
    subject = {subject_key:"y"}
    query = request.form.get('query').split()
    results = fetch_arxiv_results(subject, query)
    if isinstance(results, str):
        return results
    else:
        return render_template('response.html', results=results)
    
if __name__ == '__main__':
    app.run(debug=True)