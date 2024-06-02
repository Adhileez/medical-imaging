import os
from flask import Flask, request, jsonify, send_from_directory
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

UPLOAD_FOLDER = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/input_data_128/val/images'
IMAGES_FOLDER = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/converted npy to png/images_png'
PREDICTIONS_FOLDER = 'C:/Users/ADHI/Desktop/MAJOR PROJECT/BraTS2020_TrainingData/converted npy to png/predictions_png'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER, exist_ok=True)
os.makedirs(PREDICTIONS_FOLDER, exist_ok=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered successfully"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.username)
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    file = request.files['file']
    if not file:
        return jsonify(message="No file uploaded"), 400
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify(message="File uploaded successfully"), 201

@app.route('/images/<filename>', methods=['GET'])
@jwt_required()
def get_image_slices(filename):
    base_name = os.path.splitext(filename)[0]  # Strip .npy extension
    slices = [f for f in os.listdir(IMAGES_FOLDER) if f.startswith(base_name)]
    return jsonify(slices=slices), 200

@app.route('/predictions/<filename>', methods=['GET'])
@jwt_required()
def get_prediction_slices(filename):
    base_name = os.path.splitext(filename)[0]  
    base_name = base_name.replace('image', 'mask')
    slices = [f for f in os.listdir(PREDICTIONS_FOLDER) if f.startswith(base_name)]
    return jsonify(slices=slices), 200

@app.route('/images_predictions/<filename>', methods=['GET'])
@jwt_required()
def get_images_predictions(filename):
    base_name = os.path.splitext(filename)[0]
    image_slices = [f for f in os.listdir(IMAGES_FOLDER) if f.startswith(base_name)]
    prediction_slices = [f for f in os.listdir(PREDICTIONS_FOLDER) if f.startswith(base_name.replace('image', 'mask'))]
    return jsonify(image_slices=image_slices, prediction_slices=prediction_slices), 200

@app.route('/static/predictions_png/<path:filename>')
def static_predictions(filename):
    return send_from_directory(PREDICTIONS_FOLDER, filename)    

@app.route('/static/images_png/<path:filename>')
def static_images(filename):
    return send_from_directory(IMAGES_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)


























