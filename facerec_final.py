import face_recognition
import cv2
import numpy as np

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Load and encode face images
try:
    obama_image = face_recognition.load_image_file("Varun.jpg")
    obama_face_encodings = face_recognition.face_encodings(obama_image)
    if not obama_face_encodings:
        print("No face detected in Varun.jpg")
        exit()
    obama_face_encoding = obama_face_encodings[0]

    biden_image = face_recognition.load_image_file("tomcruise.jpg")
    biden_face_encodings = face_recognition.face_encodings(biden_image)
    if not biden_face_encodings:
        print("No face detected in tomcruise.jpg")
        exit()
    biden_face_encoding = biden_face_encodings[0]

    # Known faces and names
    known_face_encodings = [obama_face_encoding, biden_face_encoding]
    known_face_names = ["Varun", "Tom"]

except FileNotFoundError as e:
    print(f"Error loading face images: {e}")
    exit()

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to capture video frame.")
            break

        if process_this_frame:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # Detect faces and encode
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # Find the best match
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Draw rectangles and names on the video frame
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the video frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

finally:
    # Release webcam and close window
    video_capture.release()
    cv2.destroyAllWindows()
