import os
import subprocess
import glob
import shutil
from flask import Flask, render_template, request, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_song():
    song_url = request.form.get('url')
    if not song_url:
        return "Please provide a valid Spotify URL."
    
    def generate():
        yield "[-] Initializing download process...\n"
        
        # Purane saare mp3 files hata do
        for f in glob.glob("*.mp3"):
            os.remove(f)
        for d in glob.glob("downloaded_playlist"):
            shutil.rmtree(d, ignore_errors=True)
            
        yield "[*] Fetching audio streams via spotdl...\n"
        
        try:
            # spotdl command with better provider fallback
            process = subprocess.Popen(
                ['spotdl', '--audio-provider', 'youtube-music', song_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            for line in process.stdout:
                yield f"{line}"
                
            process.wait()
            
            if process.returncode == 0:
                yield "\n[+] Download completed successfully on server!\n"
            else:
                yield "\n[-] Error: Could not download the song. Try another link."
                
        except Exception as e:
            yield f"\n[-] System Error: {str(e)}"

    return Response(generate(), mimetype='text/plain')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
