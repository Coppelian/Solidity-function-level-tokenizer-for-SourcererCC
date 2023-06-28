import os


def split_sol(path_1):
    li = []
    datanames = os.listdir(path_1)
    for dataname in datanames:
        if os.path.splitext(dataname)[1] == '.sol':  # recognize *.sol file
            li.append(dataname)
    return li


class FileUtil:
    def alter(self, file, encode='UTF-8'):
        """
        Exchange command line
        :param file: filepath file location
        :return:
        """
        file_data = ""
        is_comment = False
        with open(file, "r", encoding=encode) as f:
            for line in f:
                if line.lstrip().startswith('/*'):
                    if line.rstrip().endswith('*/'):
                        line_1 = line.replace(line, '\n')
                        file_data += line_1
                        continue
                    elif '*/' in line and line.count('*') > 1:
                        file_data += line
                        continue
                    line_1 = line.replace(line, '\n')
                    is_comment = True
                    file_data += line_1
                    continue
                elif '*/' in line and is_comment is True:
                    line_1 = line.replace(line, '\n')
                    is_comment = False
                    file_data += line_1
                    continue
                elif is_comment:
                    line_1 = line.replace(line, '\n')
                    file_data += line_1
                    continue
                elif line.lstrip().startswith('//'):
                    line_1 = line.replace(line, ' \n')
                    # index = line.find("//")
                    # print(line[index:-1])
                    # line = line.replace(line[index:-1], '')
                    # print(line)
                    file_data += line_1
                    continue
                elif '//' in line:
                    line_0 = line.partition('//')
                    line_1 = line_0[0] + '\n'
                    file_data += line_1
                    continue
                file_data += line
        with open(file, "w", encoding=encode) as f:
            f.write(file_data)

    # 判断修改后的新字符串在文件中是否存在
    def new_str_exist(self, file, new_str):
        with open(file, "r", encoding='UTF-8') as f:
            for line in f:
                if new_str in line:
                    return True
        return False


# def test_strip(path1):
#     util_1 = FileUtil()
#     util_1.alter(path1)


if __name__ == '__main__':
    path_1 = './source_file'
    li = split_sol(path_1)
    util = FileUtil()
    for filename in li:
        file_path = os.path.join(path_1, filename)
        util.alter(file_path)
    print("Solidity command line erase complete！")
