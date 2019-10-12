import glob

files = glob.glob('*.csv')

lines_n = - len(files)

for file in files:
    print(file)
    with open(file, 'rt') as f:
        for line in f:
            lines_n += 1
            print(line)
        
print(lines_n)
