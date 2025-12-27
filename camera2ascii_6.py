import cv2
import numpy as np
import speech_recognition as sr
import threading
from PIL import Image, ImageDraw, ImageFont

shared_data = {"text": "CHECKING "}
running = True

try:
    font = ImageFont.truetype("C:/Windows/Fonts/msgothic.ttc", 12)
except:
    font = None

def voice_recognition_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    # 認識感度を極限まで上げます
    recognizer.energy_threshold = 50 
    
    while running:
        with mic as source:
            try:
                print("...音を待っています...") # これが出るか確認
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=3)
                print("...音を検知！解析中...") # 声を出した時にこれが出るか
                
                text = recognizer.recognize_google(audio, language='ja-JP')
                shared_data["text"] = text + " "
                print(f"★成功: {text}")
            except sr.UnknownValueError:
                print("×：言葉として認識できませんでした")
            except Exception as e:
                print(f"エラー: {e}")

threading.Thread(target=voice_recognition_loop, daemon=True).start()

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rows, cols = 40, 70 
    small_gray = cv2.resize(gray, (cols, rows))
    canvas = np.zeros((rows * 15, cols * 10, 3), dtype=np.uint8)
    pil_img = Image.fromarray(canvas)
    draw = ImageDraw.Draw(pil_img)
    display_text = shared_data["text"]
    for y in range(rows):
        for x in range(cols):
            brightness = small_gray[y, x]
            if brightness > 70:
                char_idx = (y * cols + x) % len(display_text)
                draw.text((x * 10, y * 15), display_text[char_idx], font=font, fill=(0, int(brightness), 0))
    cv2.imshow('Debug AA', np.array(pil_img))
    if cv2.waitKey(1) & 0xFF == 27:
        running = False
        break
cap.release()
cv2.destroyAllWindows()