import cv2
import numpy as np
import dlib
import pickle as pkl
from sklearnex.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import load_model

x, y = pkl.load(open('data/samples.pkl', 'rb'))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)
x_val, x_test, y_val, y_test = train_test_split(x_test, y_test, test_size=0.5, random_state=42)

std = StandardScaler()
std.fit(x_train)
x_train = std.transform(x_train)
x_val = std.transform(x_val)
x_test = std.transform(x_test)

def detect_face_points(image):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
    face_rect = detector(image, 1)
    if len(face_rect) != 1: return []
    
    dlib_points = predictor(image, face_rect[0])
    face_points = []
    for i in range(68):
        x, y = dlib_points.part(i).x, dlib_points.part(i).y
        face_points.append(np.array([x, y]))
    return face_points
        
def compute_features(face_points):
    assert (len(face_points) == 68), "len(face_points) must be 68"
    
    face_points = np.array(face_points)
    features = []
    for i in range(68):
        for j in range(i+1, 68):
            features.append(np.linalg.norm(face_points[i]-face_points[j]))
            
    return np.array(features).reshape(1, -1)

def Predict(image, model):
    im = image
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    face_points = detect_face_points(im)

    if len(face_points) != 68:
        print("68 face landmarks not detected.")
        return
    
    for x, y in face_points:
        cv2.circle(im, (x, y), 1, (0, 255, 0), -1)
        
    features = compute_features(face_points)
    features = std.transform(features)
    y_pred = model.predict(features)

    roll_pred, pitch_pred, yaw_pred = y_pred[0]
    print(' Roll: {:.2f}°'.format(roll_pred))
    print('Pitch: {:.2f}°'.format(pitch_pred))
    print('  Yaw: {:.2f}°'.format(yaw_pred))
    
    if (pitch_pred >= 5 and yaw_pred > 0):
        print('looking left up')
    elif (pitch_pred >= 5 and yaw_pred < 0):
        print('looking right up')
    elif (pitch_pred <= 5 and yaw_pred > 0):
        print('looking left down')
    else:
        print('looking right down')
        
    cv2.imshow('Preview', im)

vid = cv2.VideoCapture(0)
model = load_model('models/model.h5')
while(True):
      
    ret, frame = vid.read()
    Predict(frame, model)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()