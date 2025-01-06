import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import json
from wand.image import Image
from wand.color import Color


def rotate_immage(schablone_path, platine_path, platine_rotated_path, rotation):
    with Image(filename=platine_path) as img:
        img.rotate(-rotation, background=Color('rgb(0,0,0)'))
        img.save(filename=platine_rotated_path)
    
    # Schablone und Platine laden
    schablone = cv.imread(schablone_path, cv.IMREAD_GRAYSCALE)
    platine = cv.imread(platine_rotated_path, cv.IMREAD_GRAYSCALE)

    assert schablone is not None, "Schablone konnte nicht geladen werden. Prüfe den Pfad."
    assert platine is not None, "Platine konnte nicht geladen werden. Prüfe den Pfad."
    
    h, w = schablone.shape
    region_w, region_h = w//3, h//2

    for c in range(3):
        for r in range(2):
            # Bereich ausschneiden
            region = schablone[region_h * r:region_h * (r+1), region_w * c:region_w * (c+1)]

            

            # Template-Matching anwenden
            res = cv.matchTemplate(region, platine, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

            if max_val < 0.5:
                print("Keine Übereinstimmung gefunden. R:", r, "C:", c, "Rotation:", rotation, "Max Val:", max_val)
            else:
                print("Übereinstimmung gefunden. R:", r, "C:", c, "Rotation:", rotation, "Max Val:", max_val)
                return True
    return False

def rotate_immage2(schablone_path, platine_path, platine_rotated_path, rotation):
    with Image(filename=platine_path) as img:
        img.rotate(-rotation, background=Color('rgb(0,0,0)'))
        img.save(filename=platine_rotated_path)
    
    # Schablone und Platine laden
    schablone = cv.imread(schablone_path, cv.IMREAD_GRAYSCALE)
    platine = cv.imread(platine_rotated_path, cv.IMREAD_GRAYSCALE)

    assert schablone is not None, "Schablone konnte nicht geladen werden. Prüfe den Pfad."
    assert platine is not None, "Platine konnte nicht geladen werden. Prüfe den Pfad."
    
    y, x = 1000, 1500
    region_w, region_h = 1000, 1000

    region = schablone[y:region_h + y, x:region_w + x]

    w, h = region.shape[::-1]

    # Template-Matching anwenden
    res = cv.matchTemplate(region, platine, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    if max_val < 0.5:
        print("Keine Übereinstimmung gefunden. Rotation:", rotation, "Max Val:", max_val)
    else:
        print("Übereinstimmung gefunden. Rotation:", rotation, "Max Val:", max_val)
        return True
    
    # # Markiere den zufälligen Bereich in der Schablone
    # schablone_marked = cv.cvtColor(schablone, cv.COLOR_GRAY2BGR)
    # cv.rectangle(schablone_marked, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # # Markiere den gefundenen Bereich in der Platine
    # platine_marked = cv.cvtColor(platine, cv.COLOR_GRAY2BGR)
    # top_left = max_loc
    # platine_position = top_left
    # cv.rectangle(platine_marked, top_left, (top_left[0] + w, top_left[1] + h), (0, 0, 255), 2)
    # print(f"Gefundene Übereinstimmung: Startposition (x={top_left[0]}, y={top_left[1]}), Größe (w={w}, h={h})")

    # # Größe der Bilder anpassen, falls sie unterschiedlich sind
    # schablone_marked_resized = cv.resize(schablone_marked, (platine_marked.shape[1], platine_marked.shape[0]))

    # # Ergebnisse nebeneinander anzeigen
    # combined_image = np.hstack((schablone_marked_resized, platine_marked))

    # # Visualisierung
    # plt.figure(figsize=(14, 7))
    # plt.imshow(cv.cvtColor(combined_image, cv.COLOR_BGR2RGB))
    # plt.title(f"Schablone (links) und Platine (rechts) mit markierten Bereichen")
    # plt.xticks([]), plt.yticks([])
    # plt.show(block=False)
    # plt.pause(25)  # Show the plot for 2 seconds
    # plt.close() 
    return False 
    

if __name__ == "__main__":
    # Paths to the grayscale images
    schablone_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_schablone.png"
    platine_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_platine.png"
    platine_rotated_path = "/home/pi/Desktop/Platinenprojekt/pictures/output_platine_rotated.png"

    for r in np.arange(-1, 2, 0.1):
        if rotate_immage2(schablone_path, platine_path, platine_rotated_path, r):
            break
    print(f"Match at rotation: {r}°")

    with open("rotation.json", "w") as f:
            json.dump({"deltar": r}, f)

    

