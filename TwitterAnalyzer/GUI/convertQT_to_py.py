import os

out = os.system('pyuic5 -x GUI_QT.ui -o GUI.py')

if out:
    input('Error:', out)


