import cv2
import face_recognition
import numpy as np

class ReconocimientoFacial:
    @staticmethod
    def capturar_datos_facial():
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("No se pudo abrir la cámara.")
            return None

        print("Por favor, mira a la cámara y presiona 'q' para capturar la imagen.")
        datos_facial = None

        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("No se pudo leer el frame de la cámara.")
                break

            # Convertir la imagen al espacio de color RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detectar las ubicaciones de los rostros en el frame
            face_locations = face_recognition.face_locations(rgb_frame)

            if face_locations:
                # Obtiene las coordenadas del primer rostro detectado
                top, right, bottom, left = face_locations[0]
                # Dibujar un recuadro verde alrededor del rostro detectado
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

            cv2.imshow("Captura de Rostro (Presiona 'q' para capturar)", frame)

            # Si el usuario presiona 'q', se intenta capturar el encoding del rostro
            if cv2.waitKey(1) & 0xFF == ord('q'):
                if face_locations:
                    datos_facial = face_recognition.face_encodings(rgb_frame, face_locations)[0]
                else:
                    print("No se detectó ningún rostro en el momento de la captura.")
                break

        video_capture.release()
        cv2.destroyAllWindows()
        
        if datos_facial is not None:
            print("¡Rostro capturado con éxito!")
        return datos_facial

    @staticmethod
    def convertir_a_bytes(datos):
        return datos.tobytes() if datos is not None else None

    @staticmethod
    def convertir_a_ndarray(datos_bytes):
        return np.frombuffer(datos_bytes, dtype=np.float64) if datos_bytes else None

    @staticmethod
    def comparar_rostros(datos1, datos2):
        if datos1 is None or datos2 is None:
            return False
        return face_recognition.compare_faces([datos1], datos2)[0]
