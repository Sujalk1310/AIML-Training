import cv2
import mediapipe as mp
import numpy as np
import time

# Setup
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# Webcam input
cap = cv2.VideoCapture(0)
prev_frame_time = 0
new_frame_time = 0

def record():
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    t_end = time.time() + 60 * 1/6 #minute
    while time.time() < t_end:
        success, image = cap.read()
        out.write(image) 
        cv2.putText(image, "Recording...", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('Record', image)
        out.release()

# Parameters for distress detection
# previous_left_wrist = None
# previous_right_wrist = None
# previous_left_elbow = None
# previous_right_elbow= None
# previous_left_shoulder = None
# previous_right_shoulder = None
frame_counter = 0
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring No Video in Camera frame")
            continue

        # Drawing
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            # Get the landmarks (keypoints) of the body
            landmarks = results.pose_landmarks.landmark
            # print(landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT].y)
            
            left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y
            right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y
            mouth = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT].y
            # Get the vertical positions of the wrists, elbows, and shoulders
            # left_wrist = np.array((landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, 
            #                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y,
            #                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST].z))
            # right_wrist = np.array((landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
            #                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y,
            #                         landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].z))                  
            # left_elbow = np.array((landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x,
            #                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y,
            #                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].z))
            # right_elbow = np.array((landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
            #                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y,
            #                         landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].z))
            # left_shoulder = np.array((landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
            #                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y,
            #                           landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].z))
            # right_shoulder = np.array((landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
            #                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y,
            #                            landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].z))

            # if (
            #     previous_left_wrist is not None and
            #     previous_right_wrist is not None and
            #     previous_left_elbow is not None and
            #     previous_right_elbow is not None and
            #     previous_left_shoulder is not None and
            #     previous_right_shoulder is not None
            # ):
                # Calculate the absolute difference in positions of wrists, elbows, and shoulders
                # left_wrist_motion = (
                #     np.linalg.norm(left_wrist - previous_left_wrist)
                # )       
                # right_wrist_motion = (
                #     np.linalg.norm(right_wrist - previous_right_wrist)
                # )
                # if (right_wrist_motion+left_wrist_motion>0.6):
                #     print("dist")
                # left_elbow_motion = (
                #     np.linalg.norm(left_elbow - previous_left_elbow)
                # )
                # right_elbow_motion = (
                #     np.linalg.norm(right_elbow - previous_right_elbow)
                # )
                # if (right_elbow_motion+left_elbow_motion>0.4):
                #     print("dist")
                # left_shoulder_motion = (
                #     np.linalg.norm(left_shoulder- previous_left_shoulder)
                # )
                # right_shoulder_motion = (
                #     np.linalg.norm(right_shoulder- previous_right_shoulder)
                # )
                # if (left_shoulder_motion+right_shoulder_motion>0.2):
                #     print("dist")

                # Check if the sum of motions is above the distress threshold

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = str(int(fps))
            if(left_wrist < mouth and right_wrist < mouth):
                message = f"Distress Detected {fps}"
                frame_counter += 1
            else:
                message = fps
                frame_counter = 0
            if (frame_counter > 30):
                message = "Warn 1"
            if (frame_counter > 60):
                message = "Warn 2"
            if (frame_counter > 90):
                message = "Calling Emergency Services"
                record()
                frame_counter = 0
            print(message)
            cv2.putText(image, message, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Update previous positions
            # previous_left_wrist = left_wrist
            # previous_right_wrist = right_wrist
            # previous_left_elbow = left_elbow
            # previous_right_elbow = right_elbow
            # previous_left_shoulder = left_shoulder
            # previous_right_shoulder = right_shoulder

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )

        cv2.imshow('MediaPipe Pose Estimation Program Video Demo', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
