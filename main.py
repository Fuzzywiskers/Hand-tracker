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
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS  #make line connectiosn between landmarks#
                    )

                    finger_tips = {
                        "Thumb": hand_landmarks.landmark[4],        #hand_landmark.landmark[#] is how landmark defines finger tips#
                        "Index": hand_landmarks.landmark[8],
                        "Middle": hand_landmarks.landmark[12],
                        "Ring": hand_landmarks.landmark[16],
                        "Pinky": hand_landmarks.landmark[20]
                    }

                    for name, landmark in finger_tips.items():
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        cv2.putText(
                            img, 
                            name,
                            (x, y -10),      #so the text is slightly above the finger#
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            1
                        )

                        #turnt he tips of your finger a green circle#
                        cv2.circle(
                            img,
                            (x, y),
                            5, 
                            (0, 255, 0),
                            -1      #will fill the whole circle#
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

