from flask import Flask, render_template, request
from serpapi import GoogleSearch
import tempfile
import os
import requests

app = Flask(__name__)

# Replace 'client_id' with your actual Imgur client ID
client_id = '48fdd4bed67d763'


def upload_image_to_imgur(image_path):
    url = 'https://api.imgur.com/3/image'
    headers = {'Authorization': f'Client-ID {client_id}'}
    with open(image_path, 'rb') as f:
        payload = {'image': f.read()}
        response = requests.post(url, headers=headers, files=payload)
        data = response.json()
        if response.status_code == 200:
            return data['data']['link']
        else:
            return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename != '':
                # Save the uploaded image to a temporary file
                temp_image = tempfile.NamedTemporaryFile(delete=False)
                temp_image_path = temp_image.name
                image_file.save(temp_image_path)

                # Upload the image to Imgur and get the URL
                imgur_url = upload_image_to_imgur(temp_image_path)

                # Perform the Google Lens search using the Imgur URL
                params = {
                    "api_key": "21ead71b458d051c367a569ed84627ed80300e1a006d88582330eaacf8c48c99",
                    "engine": "google_lens",
                    "url": imgur_url,
                    "country": "in"
                }
                search = GoogleSearch(params)
                results = search.get_dict()

                # Render the HTML template with the search results
                return render_template('index.html', results=results, path=imgur_url)

    # Render the upload form if GET request or if upload failed
    return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
