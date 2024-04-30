import os 
import subprocess
import main_tower
import main_pump1

#os.system('/../High_level/main_tower.py' & '/../High_level/main_pump1.py')

subprocess.call(['python','/../High_level/main_tower.py','python', '/../High_level/main_pump1.py'])