import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
keyboard = Controller()

cap = cv2.VideoCapture(1)

def is_fist(landmarks):
    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            return False
    return True

while True:
    success, img = cap.read()
    success, img = cap.read()

    if not success or img is None:
        print("⚠️ Could not access camera feed. Check camera permissions or if another app is using the webcam.")
        continue

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            if is_fist(landmarks):
                print("Brake 🚫 (Fist)")
                keyboard.press(Key.left)
                keyboard.release(Key.right)
            else:
                print("Accelerate 🚀 (Hand Open)")
                keyboard.press(Key.right)
                keyboard.release(Key.left)

    cv2.imshow("Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
