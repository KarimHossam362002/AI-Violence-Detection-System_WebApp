import cv2

def locate_cameras():
    print("Searching for available camera indices...")
    # Loop through the first 6 indices to see what is active
    for index in range(6):
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if cap.isOpened():
            # Grab one frame to verify it's working
            ret, frame = cap.read()
            if ret:
                print(f"Index {index}: Device is AVAILABLE and returning frames.")
            else:
                print(f"Index {index}: Device opened but failed to return frames.")
            cap.release()
        else:
            print(f"Index {index}: Device is closed/unavailable.")

if __name__ == "__main__":
    locate_cameras()
