#Malia Moreno
#8 July 2026

#imports#
import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

#setting up camera capture(cap)#
#also, make sure the camera is on or you'll get a warning#
cap = cv2.VideoCapture(0)       #number for the specific camera (bult in)#
cap.set(3, 1280)
cap.set(4, 720)



def main():
    with mp_hands.Hands(
        max_num_hands = 2,
        min_detection_confidence = 0.7,
        min_tracking_confidence = 0.7
    ) as hands:
        #get img(frame) from camera#
        while True:
            attempt = 0
            success, img = cap.read()

            #sometimes camera takes a little time to load, so this lets the camera have some time to load (and if it doesn't the program closes)#
            while not success and attempt < 5:
                time.sleep(0.2)     #seconds#
                success, img = cap.read()
                attempt += 1
            if not success:
                print("failed to read frame")
                break

            #flip the image#
            img = cv2.flip(img, 1)

            h, w, _ = img.shape
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            #draw those hand landmarks#
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(
                        img,
                        hand_landmarks
                    )

            cv2.imshow("Image", img)

            #close window if press q#
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    #closes the window#
    cap.release()  
    cap.destroyAllwindows()

if __name__ == "__main__":
    main()

