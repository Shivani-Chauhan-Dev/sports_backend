from database.database import db
from flask import request,jsonify,send_file
from . import bp
from database.database import db
import os
from model.image import Image


UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@bp.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Save the image metadata to the database
        new_image = Image(filename=file.filename)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({'message': 'Image uploaded successfully', 'image_id': new_image.id}), 200
