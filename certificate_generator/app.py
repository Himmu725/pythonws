from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = Flask(__name__)
CERT_DIR = "certs"
os.makedirs(CERT_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        webinar = request.form['webinar']
        date = request.form['date']

        cert_path = generate_certificate(name, webinar, date)
        return send_file(cert_path, as_attachment=True)

    return render_template('index.html')

def generate_certificate(name, webinar, date):
    template = Image.open('C:\\Users\\Himanshu\\Downloads\\gitlabws\\pythonws\\certificate_generator\\console.png')
    draw = ImageDraw.Draw(template)

    # Load a font (adjust path and size)
    font = ImageFont.truetype("arial.ttf", 50)
    font_small = ImageFont.truetype("arial.ttf", 30)

    # Draw text (adjust x, y for alignment)
    draw.text((600, 400), name, fill="black", font=font)
    draw.text((600, 500), webinar, fill="black", font=font_small)
    draw.text((600, 600), date, fill="black", font=font_small)

    file_path = os.path.join(CERT_DIR, f"{uuid.uuid4()}.png")
    template.save(file_path)
    return file_path

if __name__ == '__main__':
    app.run(debug=True)


