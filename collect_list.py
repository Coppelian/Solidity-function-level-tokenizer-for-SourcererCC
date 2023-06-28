import os

number = 'source_file_zip'
path = './' + number
files = os.listdir(path)
new = open('projects-list.txt', 'w', encoding="utf-8")
for file in files:
    p = number + "/" + file
    new.writelines(p)
    new.write('\n')
new.close()
