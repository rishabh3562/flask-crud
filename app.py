from flask import Flask, request, jsonify, send_file
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Hello, World!"

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()

        # Validate input
        if not data or 'link' not in data or 'language' not in data:
            return jsonify({"error": "Invalid or missing JSON data. Provide 'link' and 'language'."}), 400

        video_url = data['link']
        language = data['language']

        # Download video
        yt = YouTube(video_url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()

        if not video_stream:
            return jsonify({"error": "No suitable video stream found."}), 404

        video_path = video_stream.download(filename="video.mp4")

        # Extract audio
        video_clip = VideoFileClip(video_path)
        audio_path = "audio.mp3"
        video_clip.audio.write_audiofile(audio_path)

        # Placeholder for translated text (implement translation logic)
        translated_text = "Hello, how are you?"  # Replace with actual translation logic

        # Convert translated text to speech
        translated_audio_path = "translated_audio.mp3"
        tts = gTTS(translated_text, lang=language)
        tts.save(translated_audio_path)

        # Merge translated audio with video
        translated_audio = AudioFileClip(translated_audio_path)
        final_clip = video_clip.set_audio(translated_audio)
        output_path = "translated_video.mp4"
        final_clip.write_videofile(output_path)

        # Clean up
        video_clip.close()
        translated_audio.close()
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(translated_audio_path)

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
