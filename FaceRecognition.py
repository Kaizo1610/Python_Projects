import cv2
import face_recognition

# Define known faces and names for recognition
known_face_encodings = []
known_face_names = []

# Load known faces and generate encodings
def load_known_faces():
    try:
        # Load images and names of known individuals
        image_person1 = face_recognition.load_image_file("akim.jpg")
        image_person2 = face_recognition.load_image_file("badri.jpg")
        
        # Generate encodings for known faces
        known_face_encodings.append(face_recognition.face_encodings(image_person1)[0])
        known_face_encodings.append(face_recognition.face_encodings(image_person2)[0])
        
        # Corresponding names
        known_face_names.extend(["Akim", "Badri"])
        
        print("Known faces loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error loading known faces: {e}")

# Initialize webcam and check access
def initialize_webcam():
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Webcam not accessible. Please check connection and permissions.")
        return None
    print("Webcam is accessible.")
    return video_capture

# Process each video frame to detect and recognize faces
def process_video(video_capture):
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture image.")
            break
        
        # Resize frame for faster processing and convert to RGB
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Detect face locations and encodings in current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        # Match detected faces with known faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Find the best match for the face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = face_distances.argmin()
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            
            # Scale up face locations and draw a box around the face
            top, right, bottom, left = top * 4, right * 4, bottom * 4, left * 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Draw label with name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
        
        # Display the frame with recognized faces
        cv2.imshow("Video - Face Recognition", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting face recognition.")
            break

    # Release resources and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Load known faces, initialize the webcam, and start processing
load_known_faces()
video_capture = initialize_webcam()
if video_capture:
    process_video(video_capture)
