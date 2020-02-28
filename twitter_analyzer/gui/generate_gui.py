import os

file_path = os.path.join(os.path.dirname(__file__), 'GUI_QT.ui')
dest_path = os.path.join(os.path.dirname(__file__), 'gui.py')
out = os.system(f'pyuic5 -x {file_path} -o {dest_path}')

if out:
    print('Error:', out)
    exit(1)
else:
	print('Its ok.')


