import sys
from os import mkdir, listdir, path
from shutil import rmtree

def split_file(filename, to_dir):
    if path.exists(to_dir):
        rmtree(to_dir)
    mkdir(to_dir)
    f = open(filename, 'rb')
    data = f.read()
    f.close()
    if data[:2] == '\xff\xfe':
        data = data.decode('utf16').encode('utf8')
    i_lines = [line + '\n' for line in data.splitlines()]
    loc_name = (i_lines[0][2:-1]).decode('utf-8')
    ff = open(to_dir + loc_name + '.txt', 'w')
    for line in i_lines:
        if line[0] == '#' and line[1] == ' ':
            ff.close()
            loc_name = (line[2:-1]).decode('utf-8')
            ff = open(to_dir + loc_name + '.txt', 'w')
        ff.write(line)

def merge_file(dir, filename, mode):
    file_list = []
    f = open(filename, 'wb')
    if mode == 'utf16':
        f.write('\xff\xfe')
    for file in listdir(unicode(dir, 'utf-8')):
        file_n = path.join(dir, file)
        ff = open(file_n, 'rb')
        data = ff.read()
        if mode == 'utf16':
            data = data.decode('utf8').encode(mode)
            f.write(data[2:])
        else:
            f.write(data)
        ff.close()
    f.close()

def main():
    if len(sys.argv) != 3:
        print 'usage: split_file.py {--split | --merge | --merge2} file'
        sys.exit(1)

    dist_dir = 'src/'
    option = sys.argv[1]
    filename = sys.argv[2]
    if option == '--split':
        split_file(filename, dist_dir)
    elif option == '--merge':
        merge_file(dist_dir, filename, 'utf8')
    elif option == '--merge2':
        merge_file(dist_dir, filename, 'utf16')
    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
  main()