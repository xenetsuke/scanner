from pyzbar.pyzbar import decode;
import cv2;
import firebase_admin
from firebase_admin import credentials, firestore

# Replace these values with your actual Firebase project credentials
cred = credentials.Certificate(
    {
  "type": "service_account",
  "project_id": "medvend-7c6e8",
  "private_key_id": "73eb33e962638ac3cf062da75de14ea637aa5fd8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDQWZCoTDUZbWfV\nlafcaCZKamV9HuvDy4xmSAAvKopZrhfI232qXaaxXvM5MHNnOS6QqOfcAevk0N+B\niTcnEC9F7p+QUM9ntSiIvWNZd3YRVTHZ6atD6IrxiSAS9YiUeG7OX3BWzZjQmg9a\nUCpVRmDlJmUnu38RiqJ106ST3AmRucXO3urjJ+EQoWq8/rSu7R/PG+E8rmdP3i7n\nANRFM/ddq3CkXAA5Ah8BAz0T/bVyjuhqj2+Y1RM2Vs8nmr/w5qPn/JXX96OBBVi1\na4MOxgIHZrCPOxUTaLPKE1gBgjsWAho4b6oEDEXOMavVaeyviZojb/pDZzE1mHv0\nT5EsRu6hAgMBAAECggEAAWWPFxgSMOrtA854gfnMEYcEP3KECsANe9zMaVnd+2nF\niLMcCkwYDKArVQIOwoy+TK1kapL7I9xKaEjH3+7hOXisTe4GpLHisn2VQR6HZ13U\nElCwbi7a69+qPeL2SHevPmwizDS6HrsnjSbhDP557vca9lBfEP+ymIPZ9Ssn6z0c\nYDRgn4h03aeB4fcRSwHP3PClnuEOnRJJk5o0y+Zzb/spknHP51wt00hlbWlvpcdq\nS1vQAPbdU+QCRp8lFpsM5B45Y5ywaNuqUzE3IpmUu/xZG8mRzn6CzqxFyRMFQZwK\nNvD/Wmcqqt4R36puXW2mhLLB6KLFL2o7PsqHL9V50QKBgQDxLV1pv8l2oL+B4RYS\nSON2FvrizzaQcl4ei6xFSr4XTl7usFFf61Xq/NrtoM3RUSwKm1eZw14pS2q2Lr13\nk3yVvEAExzClHWxxaiEvhrZCuOHHTp/DOXm9NVxNBwDNpbT2aooimE6q4jbAoOWZ\nStZy3WdQJ9yaG/K1Ojy6wnvfsQKBgQDdJ7N/byUpFShXVewy2bzvxk9a+K0uG/FB\nKzgIfhkDqe7o/KjA6Bo/id+eU4vbaQ6f7t8/yo8htRYLGPufRlI6QprVzBVXS39R\n/ER/sGJTv8GU47WSMYpnFT/F6uf7nM9UCoCg6TKyg1iH69aytHV74FXEscNzSDsF\nn8tZZ7Yp8QKBgQDwuIvlUhT+v8GGHCjQhUnrg1JU8egPUufYaya+XrTPRF0Ctp/y\nMk2mZ00JI5hq1S81QwmzosmoQ+s1/f8EjAQs3CG14y8Njwm/RePrsPTYMfrA2Rwj\nWonFLa57/4JwwHWYAozvrL/QVku6Bp5EW+sh6RUGb1MDyuN8ua0F57qGcQKBgDJV\niuECJu8Gxbu67ptUO1BHTmBiIOhRq8MtVv9307Glx553guEE8pRriN28HiS98Hou\nH9mg/JqrYGz+Lqa9lpFz/1GRtXm80SmTxPNa7cYp6qE8gmLXq6xyhaVCJbJ6qiVy\njnwRF1zR0CB/aMobkHG1SVAPNXDTi7tn9xxOIoPBAoGBALMNEbL0ACpfB1NpQv1r\nKZ4KfBUBogopdKby1fDHwA6HV9+nGlmEt/IptYZ/8Ci9Si7fBiOX+ichk9ndbGM+\nOdKkDo09FiquWCEb60a/YKG/1Vv0uXV/mOaapb0OvI7lyut0Qlm4q2hRgMgLErVL\nbmps3wGsXv+LdslN6a7NmbUw\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-miq54@medvend-7c6e8.iam.gserviceaccount.com",
  "client_id": "101606156353001165215",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-miq54%40medvend-7c6e8.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
)

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred, {'databaseURL': 'https://medvend-7c6e8-default-rtdb.asia-southeast1.firebasedatabase.app/'})
# Function to open QR code scanner, collect QR data, and send it to Firebase
def scan_qr_code_and_send_to_firebase():
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Decode QR codes in the frame
        decoded_objects = decode(frame)

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Check for QR codes
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            print(f"QR Code Data: {qr_data}")

            # Send data to Firebase
            db = firestore.client()
            doc_ref = db.collection('qr_codes').add({'data': qr_data})
            print(f"Data sent to Firebase with document ID: {doc_ref.id}")

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start the QR code scanner and send data to Firebase
scan_qr_code_and_send_to_firebase()

