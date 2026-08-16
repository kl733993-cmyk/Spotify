import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_song():
    song_url = request.form.get('url')
    if not song_url:
        return "Please provide a valid Spotify URL."
    
    try:
        subprocess.run(['spotdl', song_url], check=True)
        return "Download completed successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
