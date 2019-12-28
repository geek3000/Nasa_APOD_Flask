from flask import Flask, render_template, request, send_file, current_app
import json, requests, pdfcrowd, os

API_KEY="yMLIcRiTZCrBGxxdREIOV3UMBCpalccrjnUcYQem"
date=''
def get_data(date=""):
    json_data=""
    if date:
        json_data = requests.get("https://api.nasa.gov/planetary/apod?api_key="+API_KEY+"&date="+date).text
    else:
        json_data = requests.get("https://api.nasa.gov/planetary/apod?api_key="+API_KEY).text
    json_data=json.loads(json_data)
    return json_data
    
app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
@app.route('/index/')

def index():
    path=os.path.join(current_app.root_path, "static", "page.html")
    if request.method == "POST":
        date=request.form['date']
        if date:
            data=get_data(date)
            html= render_template('index.html', title=data['title'],
                            explanation=data['explanation'],
                           date=data['date'],
                           image_link=data['url'])
            with open(path, "w") as page:
                page.write(html)
            return html
            
        else:
            data=get_data()
            html= render_template('index.html', title=data['title'],
                            explanation=data['explanation'],
                           date=data['date'],
                           image_link=data['url'])
            with open(path, "w") as page:
                page.write(html)
            return html
    else:
        data=get_data()
        html=render_template('index.html', title=data['title'],
                            explanation=data['explanation'],
                           date=data['date'],
                           image_link=data['url'])
        with open(path, "w") as page:
                page.write(html)

        return html

@app.route('/save/', methods=["GET"])
def save_as_pdf():
    path=os.path.join(current_app.root_path, "static", "page.html")
    path_pdf=os.path.join(current_app.root_path, "static", "pdf", "page.pdf")
    
    try:
        client = pdfcrowd.HtmlToPdfClient('geek123', 'c3e8b743bba9bdd1164ce6e361eb122d')
        client.convertFileToFile(path, path_pdf)
        return send_file(path_pdf, as_attachment=True)
    except pdfcrowd.Error as why:
        print('Pdfcrowd Error: {}\n'.format(why))
        print("Error create PDF")
    data=get_data()
    html=render_template('index.html', title=data['title'],
                        explanation=data['explanation'],
                        date=data['date'],
                        image_link=data['url'])
    with open(path, "w") as page:
            page.write(html)
    return html
    
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port)
