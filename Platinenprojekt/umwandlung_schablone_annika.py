import cv2
import os

def convert_to_black_white(image_path, threshold=100):
    """
    Konvertiert ein Bild in ein Schwarz-Weiß-Bild.
    Helle Bereiche (Pixelwerte > threshold) werden Weiß, der Rest wird Schwarz.
    
    :param image_path: Pfad zum Eingabebild
    :param threshold: Schwellenwert für die Helligkeit
    """
    # Lade das Bild
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"Fehler: Bild {image_path} konnte nicht geladen werden.")
        return

    # Wende den Threshold an
    _, black_white = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)

    # Erzeuge einen neuen Dateinamen mit angehängter Endung
    base_name, ext = os.path.splitext(image_path)
    output_path = f"{base_name}_bw{ext}"

    # Speichere das Schwarz-Weiß-Bild
    cv2.imwrite(output_path, black_white)
    print(f"Schwarz-Weiß-Bild gespeichert als: {output_path}")

    # Zeige das Bild an
    #cv2.imshow("Original", image)
    #cv2.imshow("Schwarz-Weiß", black_white)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

# Beispiel-Aufruf
if __name__ == "__main__":
    # Pfade anpassen
    input_image = "/home/pi/Desktop/Platinenprojekt/pictures/stencil.jpg"  # Eingabebild
    convert_to_black_white(input_image, threshold=100)

