import os
import cloudinary
import cloudinary.uploader
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Cloudinary Configuration
cloudinary.config( 
  cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"), 
  api_key = os.getenv("CLOUDINARY_API_KEY"), 
  api_secret = os.getenv("CLOUDINARY_API_SECRET"),
  secure = True
)

@app.route('/upload_portfolio', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file_to_upload = request.files['file']
    
    if file_to_upload:
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(file_to_upload, folder="portfolio")
        
        # This is the URL you will save in your Firebase Firestore database later
        image_url = upload_result['secure_url']
        
        return f"Uploaded successfully! URL: {image_url}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# Initialize Firebase Firestore
# Ensure serviceAccountKey.json is in your main project folder
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        try:
            # Get data from the form
            contact_data = {
                'name': request.form.get('name'),
                'email': request.form.get('email'),
                'phone': request.form.get('phone'),
                'service': request.form.get('service'),
                'date': request.form.get('date'),
                'message': request.form.get('message'),
                'timestamp': firestore.SERVER_TIMESTAMP
            }

            # Save to a collection named 'bookings'
            db.collection('bookings').add(contact_data)
            
            return render_template('contact.html', success=True)
        except Exception as e:
            print(f"Error saving to Firestore: {e}")
            return render_template('contact.html', error=True)

    return render_template('contact.html')


if __name__ == '__main__':
    # host='0.0.0.0' allows you to view the site on your local network
    app.run(host='0.0.0.0', port=5000, debug=True)
