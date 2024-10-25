import os
from flask import Flask, request, jsonify
import gradio as gr
from ai_clipping import analyze_video, create_clips
from ai_broll import add_broll
from animated_captions import generate_captions
from social_media_scheduler import schedule_post

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
TRAINING_FOLDER = 'training'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['TRAINING_FOLDER'] = TRAINING_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

if not os.path.exists(TRAINING_FOLDER):
    os.makedirs(TRAINING_FOLDER)

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

@app.route('/train', methods=['POST'])
def train_model():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['TRAINING_FOLDER'], file.filename)
        file.save(filepath)
        # Placeholder for model training logic
        return jsonify({'message': 'File uploaded and model training started', 'filepath': filepath}), 200

def gradio_interface():
    def upload_and_process(file):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.name)
        file.save(filepath)
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

        return processed_paths

    def schedule(clip_path, platform, schedule_time):
        schedule_post(clip_path, platform, schedule_time)
        return "Clip scheduled successfully"

    def upload_and_train(file):
        filepath = os.path.join(app.config['TRAINING_FOLDER'], file.name)
        file.save(filepath)
        # Placeholder for model training logic
        return "File uploaded and model training started"

    with gr.Blocks() as demo:
        with gr.Tab("Upload and Process"):
            upload_file = gr.File(label="Upload Video")
            process_button = gr.Button("Process Video")
            output = gr.Gallery(label="Processed Clips")
            process_button.click(upload_and_process, inputs=upload_file, outputs=output)

        with gr.Tab("Schedule"):
            clip_path = gr.Textbox(label="Clip Path")
            platform = gr.Textbox(label="Platform")
            schedule_time = gr.Textbox(label="Schedule Time")
            schedule_button = gr.Button("Schedule Clip")
            schedule_output = gr.Textbox(label="Schedule Status")
            schedule_button.click(schedule, inputs=[clip_path, platform, schedule_time], outputs=schedule_output)

        with gr.Tab("Train Model"):
            train_file = gr.File(label="Upload Training Video")
            train_button = gr.Button("Train Model")
            train_output = gr.Textbox(label="Training Status")
            train_button.click(upload_and_train, inputs=train_file, outputs=train_output)

    demo.launch()

if __name__ == '__main__':
    gradio_interface()
    app.run(debug=True)
