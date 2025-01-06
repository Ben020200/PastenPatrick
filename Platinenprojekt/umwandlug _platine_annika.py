from PIL import Image
import numpy as np
import cv2
from tqdm import tqdm  # Fortschrittsanzeige
def convert_to_black_white(filepath):
    try:
        # Bild laden und in RGB konvertieren
        img = Image.open(filepath).convert("RGB")
        #img = cv2.imread(filepath)
        # Bild als Numpy-Array laden
        img_array = np.array(img)
        lower_bound = 255 - white_tolerance
        white_mask = np.all(img_array >= [lower_bound, lower_bound, lower_bound], axis=-1)
        img_array[white_mask] = [0, 0, 0]  # Setze weiße Pixel auf Schwarz
        # Grün-Kanal extrahieren
        green_channel = img_array[:, :, 1]  # Grün ist der 2. Kanal (Index 1)
        # Schwarz-Weiß-Bild erstellen basierend auf dem Grün-Schwellenwert
        green_threshold = 75
        bw_array = np.where(green_channel > green_threshold, 0, 255).astype(np.uint8)
        # **Schritt 4: Weiße Randbereiche schwarz machen**
        print("Removing white border regions...")
        h, w = bw_array.shape
        mask = np.zeros((h + 2, w + 2), np.uint8)  # Flood-Fill benötigt ein erweitertes Maskenarray
        cv2.floodFill(bw_array, mask, (0, 0), 0)  # Starte Flood-Fill in der oberen linken Ecke

        # Schritt 5: Schrift entfernen (Konturen filtern)
        #print("Removing text regions...")
        #contours, _ = cv2.findContours(bw_array, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #for contour in contours:
            #x, y, w, h = cv2.boundingRect(contour)
            #area = cv2.contourArea(contour)
            #aspect_ratio = w / float(h)
            #perimeter = cv2.arcLength(contour, True)
            # Seitenverhältnis prüfen (für Kreise nahe 1.0)
            #aspect_ratio = w / float(h)
            # Kompaktheit berechnen
            #compactness = 4 * np.pi * area / (perimeter * perimeter) if perimeter > 0 else 0

            # Bedingungen für "Schrift" (kleine, dünne Flächen)
            #if area < 300 or area > 1900 or aspect_ratio > 2 or aspect_ratio < 0.1:
                #cv2.drawContours(bw_array, [contour], -1, 0, thickness=-1)  # Kontur schwarz füllen
            # Bedingungen für Kreise
            #if 0.7 <= aspect_ratio <= 1.3 and compactness > 0.1:
                #cv2.drawContours(bw_array, [contour], -1, 0, thickness=-1)  # Kontur schwarz füllen
        




        # Zurück zu einem Bild konvertieren
        bw_img = Image.fromarray(bw_array, mode="L")
        # Schwarz-Weiß-Bild speichern
        bw_output_path = f"{filepath.rsplit('.', 1)[0]}_bw.png"
        bw_img.save(bw_output_path)
        print(f"Black and white image saved to {bw_output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    # Pfad zur Bilddatei
    image_path = "/home/pi/Desktop/Platinenprojekt/pictures/pcb.jpg"
    white_tolerance = 170
    #min_area = 200
    convert_to_black_white(image_path)