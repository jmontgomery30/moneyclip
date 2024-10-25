from flask import Flask, request, jsonify
import os
from ai_clipping import analyze_video, create_clips
from ai_broll import add_broll
from animated_captions import generate_captions
from social_media_scheduler import schedule_post

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200

@app.route('/process', methods=['POST'])
def process_video():
    data = request.get_json()
    filepath = data.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'Invalid file path'}), 400

    segments = analyze_video(filepath)
    clips = create_clips(filepath, segments)
    processed_clips = []
    for clip in clips:
        clip_with_broll = add_broll(clip)
        clip_with_captions = generate_captions(clip_with_broll)
        processed_clips.append(clip_with_captions)

    processed_paths = []
    for i, clip in enumerate(processed_clips):
        processed_path = os.path.join(app.config['PROCESSED_FOLDER'], f'clip_{i}.mp4')
        clip.write_videofile(processed_path)
        processed_paths.append(processed_path)

    return jsonify({'message': 'Video processed successfully', 'clips': processed_paths}), 200

@app.route('/schedule', methods=['POST'])
def schedule_video():
    data = request.get_json()
    clip_path = data.get('clip_path')
    platform = data.get('platform')
    schedule_time = data.get('schedule_time')

    if not clip_path or not os.path.exists(clip_path):
        return jsonify({'error': 'Invalid clip path'}), 400
    if not platform or not schedule_time:
        return jsonify({'error': 'Platform and schedule time are required'}), 400

    schedule_post(clip_path, platform, schedule_time)
    return jsonify({'message': 'Clip scheduled successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
