from PIL import Image
import numpy as np

def convert_to_inverted_white_black(filepath, output_path, white_tolerance):
    try:
        # Bild laden und in RGB konvertieren
        img = Image.open(filepath).convert("RGB")
        
        # Bild als Numpy-Array laden
        img_array = np.array(img)

        # Toleranz für Weiß definieren
        lower_bound = 255 - white_tolerance  # Untere Grenze für Weiß
        white_mask = np.all(img_array >= [lower_bound, lower_bound, lower_bound], axis=-1)

        # Erstelle ein invertiertes Schwarz-Weiß-Bild
        bw_image = np.ones((img_array.shape[0], img_array.shape[1]), dtype=np.uint8) * 255  # Start: alles weiß
        bw_image[white_mask] = 0  # Weiße Bereiche werden schwarz

        # Bild speichern
        output_image = Image.fromarray(bw_image)
        output_image.save(output_path)
        print(f"Bild gespeichert als: {output_path}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

if __name__ == "__main__":
    # Pfad zur Bilddatei
    image_path = "/home/pi/Desktop/Platinenprojekt/pictures/stencil.jpg"
    output_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_schablone.png"  # Ausgabepfad
    
    white_tolerance = 200 # Toleranz für Weiß (z.B. 30 bedeutet nahe an 255)
    convert_to_inverted_white_black(image_path, output_path, white_tolerance)
