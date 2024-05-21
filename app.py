from flask import Flask, request, send_file, jsonify
import subprocess
import os
from werkzeug.utils import secure_filename
import threading
import zipfile

app = Flask(__name__)

# Directory to store uploaded and converted files
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Lock to handle single request processing at a time
processing_lock = threading.Lock()

# Encoding configurations
ENCODING_CONFIGS = {
    '96k': '-b:a 96000 -vbr on -compression_level 10 -frame_duration 20 -packet_loss 0 -application audio -cutoff 0 -mapping_family 0 -apply_phase_inv 1',
    '88k': '-b:a 88000 -vbr on -compression_level 10 -frame_duration 20 -packet_loss 0 -application audio -cutoff 0 -mapping_family 0 -apply_phase_inv 1',
    '64k': '-b:a 64000 -vbr on -compression_level 10 -frame_duration 20 -packet_loss 0 -application audio -cutoff 0 -mapping_family 0 -apply_phase_inv 1'
}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Try to acquire the lock
    if not processing_lock.acquire(blocking=False):
        return jsonify({"error": "Server is busy processing another file"}), 400
    
    try:
        filename = secure_filename(file.filename)
        base_name = filename.rsplit('.', 1)[0]
        input_filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(input_filepath)
        
        output_files = []
        for quality, params in ENCODING_CONFIGS.items():
            output_filename = f"{base_name}_{quality}-vbr_opus.ogg"
            output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)
            output_files.append(output_filepath)
            
            # Transcoding the file using FFmpeg
            command = f"ffmpeg -i {input_filepath} -c:a libopus {params} {output_filepath}"
            subprocess.run(command, shell=True, check=True)
        
        # Create a zip file containing all the output files
        zip_filename = f"{base_name}_transcoded.zip"
        zip_filepath = os.path.join(OUTPUT_FOLDER, zip_filename)
        
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for file in output_files:
                zipf.write(file, os.path.basename(file))
        # Return as a downloadable file
        return send_file(zip_filepath, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Release the lock
        processing_lock.release()
        # Clean up the uploaded file
        os.remove(input_filepath)
        for file in output_files:
            os.remove(file)
        os.remove(zip_filepath)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
