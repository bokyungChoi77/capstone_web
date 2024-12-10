from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import speech_recognition as sr
import io
from pydub import AudioSegment
from pydub.utils import which
import logging

# FFmpeg 경로 설정
AudioSegment.converter = which("ffmpeg")

# Flask 애플리케이션 생성
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 세션 암호화를 위한 키

# 사용자 데이터베이스 (테스트용)
USER_DATA = {
    "cap": "1234"
}

# 파일 크기 제한 (예: 16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# 로깅 설정
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="아이디 또는 비밀번호가 틀렸습니다.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file found!"}), 400

    audio_file = request.files['audio']

    try:
        # 오디오 파일을 WAV로 변환
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # 음성 인식
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="ko-KR")
            return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "오디오를 이해하지 못했습니다. 다시 시도해주세요."}), 400
    except sr.RequestError as e:
        logging.error(f"Google API error: {e}")
        return jsonify({"error": f"Google API error: {e}"}), 500
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)



# from flask import Flask, render_template, request, jsonify
# import speech_recognition as sr
# import io
# from pydub import AudioSegment
# from pydub.utils import which
# import logging

# # FFmpeg 경로 설정
# AudioSegment.converter = which("ffmpeg")

# # Flask 애플리케이션 생성
# app = Flask(__name__)

# # 파일 크기 제한 (예: 16MB)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # 로깅 설정
# logging.basicConfig(level=logging.INFO)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/speech-to-text', methods=['POST'])
# def speech_to_text():
#     if 'audio' not in request.files:
#         return jsonify({"error": "No audio file found!"}), 400

#     audio_file = request.files['audio']

#     try:
#         # 오디오 파일을 WAV로 변환
#         audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
#         wav_io = io.BytesIO()
#         audio.export(wav_io, format="wav")
#         wav_io.seek(0)

#         # 음성 인식
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(wav_io) as source:
#             audio_data = recognizer.record(source)
#             text = recognizer.recognize_google(audio_data, language="ko-KR")
#             return jsonify({"text": text})
#     except sr.UnknownValueError:
#         return jsonify({"error": "오디오를 이해하지 못했습니다. 다시 시도해주세요."}), 400
#     except sr.RequestError as e:
#         logging.error(f"Google API error: {e}")
#         return jsonify({"error": f"Google API error: {e}"}), 500
#     except Exception as e:
#         logging.error(f"Unhandled exception: {e}")
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)
