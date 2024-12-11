import cv2

# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Read the input image
img = cv2.imread('Eagle.jpg')

# Resize the image
width = 800  # Desired width
height = 600  # Desired height
img_resized = cv2.resize(img, (width, height))

# Convert the resized image to grayscale
gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# Draw rectangle around the faces
for (x, y, w, h) in faces:
    cv2.rectangle(img_resized, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Save the output image
cv2.imwrite('output.jpg', img_resized)

# Display the output
cv2.imshow('Face Detection', img_resized)
cv2.waitKey()
cv2.destroyAllWindows()