import os

file_path = os.path.join(os.path.dirname(__file__), 'GUI_QT.ui')
out = os.system(f'pyuic5 -x {file_path} -o GUI.py')

if out:
    input('Error:', out)
else:
	input('Its ok.')

