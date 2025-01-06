from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm  # Fortschrittsanzeige

def convert_to_black_white(filepath, output_path, white_tolerance, min_area=50, max_area=10000):
    try:
        # Bild laden und in RGB konvertieren
        img = Image.open(filepath).convert("RGB")
        
        # Bild als Numpy-Array laden
        img_array = np.array(img)

        # Toleranz für Weiß definieren
        lower_bound = 255 - white_tolerance  # Untere Grenze für Weiß
        white_mask = np.all(img_array >= [lower_bound, lower_bound, lower_bound], axis=-1)
        
        # Erstellt ein Schwarz-Weiß-Bild basierend auf der Maske
        bw_image = np.zeros((img_array.shape[0], img_array.shape[1]), dtype=np.uint8)
        bw_image[white_mask] = 255  # Weiße Pixel übernehmen
        
        # Konturen der weißen Bereiche finden
        contours, _ = cv2.findContours(bw_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Erstelle eine neue Maske, in der nur mittlere Bereiche weiß bleiben
        filtered_mask = np.zeros_like(bw_image)

        for contour in contours:
            area = cv2.contourArea(contour)
            # Prüfen, ob die Fläche innerhalb der Grenzen liegt
            if min_area <= area <= max_area:
                cv2.drawContours(filtered_mask, [contour], -1, 255, thickness=cv2.FILLED)
            
            # Berechne die Bounding Box der Kontur
            x, y, w, h = cv2.boundingRect(contour)
            bounding_box_area = w * h
            
            # Berechne die Dichte der weißen Pixel in der Bounding Box
            roi = bw_image[y:y+h, x:x+w]  # Region of Interest (Bereich der Bounding Box)
            white_pixel_count = np.sum(roi == 255)
            density = white_pixel_count / bounding_box_area

            # Filterung basierend auf der Dichte
            if density >= min_density:
                cv2.drawContours(filtered_mask, [contour], -1, 255, thickness=cv2.FILLED)
        
        # Ergebnis als RGB erstellen
        output_array = np.zeros_like(img_array)  # Ausgangspunkt: komplett schwarz
        output_array[filtered_mask == 255] = [255, 255, 255]  # Nur gefilterte weiße Bereiche bleiben weiß

        # Bild speichern
        output_image = Image.fromarray(output_array)
        output_image.save(output_path)
        print(f"Bild gespeichert als: {output_path}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    # Pfad zur Bilddatei
    image_path = "/home/pi/Desktop/Platinenprojekt/pictures/pcb.jpg"
    output_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_platine.png"  # Ausgabepfad
    
    white_tolerance = 120  # Toleranz für Weiß (z.B. 30 bedeutet nahe an 255)
    min_area = 100         # Minimale Fläche, die als weiß beibehalten wird
    max_area = 2000      # Maximale Fläche, die als weiß beibehalten wird
    min_density = 0.8
    
    convert_to_black_white(image_path, output_path, white_tolerance, min_area, max_area)
