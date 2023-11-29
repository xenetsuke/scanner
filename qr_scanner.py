import cv2;
from pyzbar.pyzbar import decode ;

def scan_qr_code():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        # Decode QR codes
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # Extract QR code data
            data = obj.data.decode('utf-8')
            print(f"QR Code Data: {data}")

            # Draw a rectangle around the QR code
            points = obj.polygon
            if len(points) == 4:
                hull = cv2.convexHull(points, clockwise=True)
                cv2.polylines(frame, [hull], True, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('QR Code Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    scan_qr_code()
