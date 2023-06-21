import os

import logging
from flask import Flask, jsonify, request, send_file
import mimetypes

from utils.get_feature import get_feature
from utils.hyper import *

import warnings
warnings.filterwarnings("ignore")


app = Flask(__name__)

# API endpoint for URL input
@app.route('/extract_feature', methods=['GET', 'POST'])
def predict():
    # Get URL from api
    cv_path = request.args.get('cv_path')

    # Get feature
    try:
        data = get_feature(cv_path)
        status = 1
        if data['avatar_path'] == '':
            return {
                'data': data,
                'status': status,
                'error_code': 500,
                'message': 'No avatar detected'
            }
        else:
            return{
                'data': data,
                'status': status,
                'error_code': 200,
                'message': 'Pass to detect'
            }
    except Exception as e:
        logging.error(e)
        status = 0
        return jsonify({'data': None,
                        'status': status,
                        'error_code': 400,
                        'message': e})

# get image from path
@app.route('/<path:image_filename>')
def get_image(image_filename):
    image_path = os.path.join(avatar_folder, image_filename)
    mimetype, _ = mimetypes.guess_type(image_path)
    return send_file(image_path, mimetype=mimetype, as_attachment=True)


if __name__ == '__main__':
    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    app.run(debug=True, host='192.168.122.102', port=3012)