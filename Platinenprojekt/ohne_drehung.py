import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import random
import json

schablone_position = None
platine_position = None
#deltax = platine_position[0]-schablone_position[0]
#deltay = platine_position[1]-schablone_position[1]


def select_random_region(image, region_size=(2000, 2000)):
    """
    Wählt einen zufälligen Bereich aus einem Bild aus.

    :param image: Eingabebild (Numpy-Array)
    :param region_size: Tuple (Breite, Höhe) des gewünschten Bereichs
    :return: Der zufällige Bereich als Array und die Position (x, y)
    """
    h, w = image.shape
    region_w, region_h = region_size

    # Sicherstellen, dass der Bereich innerhalb des Bildes liegt
    x = random.randint(0, w - region_w)
    y = random.randint(0, h - region_h)

    # Bereich ausschneiden
    region = image[y:y + region_h, x:x + region_w]
    return region, (x, y)


def template_matching_bw(schablone_path, platine_path, region_size=(2000, 2000), threshold=0.3):
    """
    Template-Matching zwischen einem zufälligen Bereich der Schablone und der gesamten Platine.

    :param schablone_path: Pfad zur Schablone (Schwarz-Weiß-Bild)
    :param platine_path: Pfad zur Platine (Schwarz-Weiß-Bild)
    :param region_size: Tuple (Breite, Höhe) des gewünschten Bereichs
    :param threshold: Ähnlichkeitsschwelle für das Matching
    """

    global schablone_position, platine_position

    # Schablone und Platine laden
    schablone = cv.imread(schablone_path, cv.IMREAD_GRAYSCALE)
    platine = cv.imread(platine_path, cv.IMREAD_GRAYSCALE)

    assert schablone is not None, "Schablone konnte nicht geladen werden. Prüfe den Pfad."
    assert platine is not None, "Platine konnte nicht geladen werden. Prüfe den Pfad."

    # Zufälligen Bereich aus der Schablone auswählen
    region, (x, y) = select_random_region(schablone, region_size)
    schablone_position = (x, y)
    print(f"Zufälliger Bereich aus der Schablone ausgewählt: Position ({x}, {y})")

    # Dimensionen des ausgewählten Bereichs
    w, h = region.shape[::-1]

    # Template-Matching anwenden
    res = cv.matchTemplate(platine, region, cv.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv.minMaxLoc(res)

    if max_val < threshold:
        print("Keine Übereinstimmung gefunden.")
        platine_position = None
        return True

    # Markiere den zufälligen Bereich in der Schablone
    schablone_marked = cv.cvtColor(schablone, cv.COLOR_GRAY2BGR)
    cv.rectangle(schablone_marked, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Markiere den gefundenen Bereich in der Platine
    platine_marked = cv.cvtColor(platine, cv.COLOR_GRAY2BGR)
    top_left = max_loc
    platine_position = top_left
    cv.rectangle(platine_marked, top_left, (top_left[0] + w, top_left[1] + h), (0, 0, 255), 2)
    print(f"Gefundene Übereinstimmung: Startposition (x={top_left[0]}, y={top_left[1]}), Größe (w={w}, h={h})")

    # Ergebnisse nebeneinander anzeigen
    combined_image = np.hstack((schablone_marked, platine_marked))

    # Visualisierung
    plt.figure(figsize=(14, 7))
    plt.imshow(cv.cvtColor(combined_image, cv.COLOR_BGR2RGB))
    plt.title(f"Schablone (links) und Platine (rechts) mit markierten Bereichen")
    plt.xticks([]), plt.yticks([])
    plt.show(block=False)
    plt.pause(60)  # Show the plot for 2 seconds
    plt.close() 
    return False
    
if __name__ == "__main__":
    # Paths to the grayscale images
    schablone_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_schablone.png"
    platine_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_platine.png"
    
    max_iterations = 10
    iterations = 0
    # Perform template matching with a random region
    while iterations < max_iterations and template_matching_bw(schablone_path, platine_path, region_size=(2000, 2000), threshold=0.3):
        iterations += 1 

    # Calculate delta x and delta y if positions are found
    if platine_position and schablone_position:
        deltax = platine_position[0] - schablone_position[0]
        deltay = platine_position[1] - schablone_position[1]

        print(f"Delta in x: {deltax}")
        print(f"Delta in y: {deltay}")

        # Save deltax and deltay to a JSON file
        with open("positions.json", "w") as f:
            json.dump({"deltax": deltax, "deltay": deltay}, f)

        print(f"Template position: {schablone_position}")
        print(f"Target position: {platine_position}")
    else:
        print("No valid positions found.")