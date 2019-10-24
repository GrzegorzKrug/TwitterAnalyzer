import os

out = os.system('pyuic5 -x GUI.ui -o GUI.py')

if out:
    input('Error:', out)


