filepath1 = 'D:\\Unreal Projects\\FlyProject2\\about.txt'
filepath2 = 'D:\\Unreal Projects\\AplikacjaGotowa\\Radar_software\\FlyProject\\about.txt'

f1 = open(filepath1, "w")
f2 = open(filepath2, "w")

lines = ['''[POL] Aplikacja modeluje system zobrazowania sytuacji powietrznej instalowany w samolotach wielozadaniowych. Zobrazowanie informacji przedstawione zostalo na wyswietlaczu MDF w formacie FCR. \n
[ENG] The application models the airborne situation display system installed in fighter aircrafts. 
The information display was presented on the MDF display in the FCR format. \n
KEYBOARD:
Simulation: W/S - Acceleration, A/D - Yaw, Q/E - Roll, UP/DOWN - Pitch, P - Pause, MOUSE
MFD: T/G - Elevation tilt, F/H - Azimuth yaw, ARROWS - Acquisition cursor, Space - STT, MOUSE''']

f1.writelines(lines)
f2.writelines(lines)
