import json
# import pymysql
import pandas as pd


MIN_LINE = 5


def ctags_json_parser(file_path, source_path):
    """
    Convert ctags json result into standard format.
    :param file_path: Place that you keep the origin output result.
    :param source_path: Where you want to save the result.
    :return:
    """
    json_txt = []
    with open(file_path, 'r', errors='ignore') as jsonfile:
        for line in jsonfile.readlines():
            json_string = json.loads(line)
            end_line = check_endline(str(json_string["path"]), source_path, int(json_string["line"]))
            line_num = check_num(str(json_string["path"]), source_path, int(json_string["line"]))
            json_string["end_line"] = int(end_line)
            json_string["line_num"] = int(line_num)
            json_txt.append(json_string)

        # json_string = json.load(jsonfile)
    """
    for json_element in json_string:
        print(json_element)
        end_line = check_endline(str(json_element["path"]), source_path, int(json_element["line"]))
        json_element["end_line"] = int(end_line)
        json_txt.append(json_element)
    """
    with open(source_path + "sample.json", "w") as outfile:
        json.dump(json_txt, outfile, indent=2)


def check_endline(string, path, start):
    """
    Return the end line of a function.
    :param string: The name of the target file
    :param path: The directory of the target file
    :param start: The start line of the target file
    :return count+1: The end line of a function
    """
    stack = []
    path = path + string
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        mark = 0
        for count in range(start - 1, len(lines)):
            for char in lines[count]:
                # print(lines[count])
                # Push the element in the stack
                if char in [";"] and mark == 0:
                    return count + 1
                if char in ["{"]:
                    mark = 1
                    stack.append(char)
                else:
                    if stack:
                        if char == "}":
                            stack.pop()
                            if not stack:
                                return count + 1
    return 0


def check_num(string, path, start):
    count_line = 0
    stack = []
    path = path + string
    mark = 0
    with open(path, 'r', encoding='utf8') as f:
        lines = f.readlines()
        for count in range(start - 1, len(lines)):
            # print(lines[count])
            if lines[count].strip() in ['\n', '\r\n']:
                continue
            if lines[count].strip() == '':
                continue
            count_line += 1
            for char in lines[count]:
                # print(lines[count])
                # Push the element in the stack
                if char in [";"] and mark == 0:
                    return count_line
                if char in ["{"]:
                    mark = 1
                    stack.append(char)
                else:
                    if stack:
                        if char == "}":
                            stack.pop()
                            if not stack:
                                return count_line
    return 0


def load_json_sql(path):
    """
    Load converted standard result into selected database.
    :param path:
    :return:
    """
    f = open(path, 'r')
    content = f.read()
    a = json.loads(content)
    # print(type(a))
    # print(a[0])
    # print(a[0]['name'])
    connect_database(a)


def connect_database(a):
    """
    save ctags json result to database
    :param a:
    :return:
    """
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='root',
                         password='mh19981215',
                         database='Deckard',
                         charset='utf8')
    cursor = db.cursor()
    count = 0
    name = str(a[0]['path'])
    for i in range(len(a)):
        # print(str(a[i]['name']))
        # print(str(a[i]['path']))
        # print(str(a[i]['pattern']))
        # print(str(a[i]['kind']))
        # print(int(a[i]['line']))
        # print(int(a[i]['end_line']))
        """
        sql = "INSERT INTO function_tag_deckard(f_name,file_name,f_info,f_type,f_startline,f_endline) VALUES('%s','%s','%s','%s','%s','%s')" \
              % (str(a[i]['name']), str(a[i]['path']), str(a[i]['pattern']), str(a[i]['kind']),
                 int(a[i]['line']), int(a[i]['end_line']))
        """
        """cursor.execute(
            'INSERT INTO function_tag_sourcerercc(f_name,file_name,f_info,f_type,f_startline,f_endline) VALUES(%s,%s,%s,%s,%s,%s)',
            (str(a[i]['name']), str(a[i]['path']), str(a[i]['pattern']), str(a[i]['kind']),
             int(a[i]['line']), int(a[i]['end_line'])))"""
        # num_0 = 0
        if int(a[i]['line_num']) > MIN_LINE:
            if a[i]['kind'] != 'function':
                continue
            if name != str(a[i]['path']):
                count = 0
            cursor.execute(
                'INSERT INTO function_tag(file_id,func_id,f_name,file_name,f_info,f_type,f_startline,'
                'f_endline,f_linenum) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                (int(str(a[i]['path']).split('_')[0]), int(count), str(a[i]['name']), str(a[i]['path']),
                 str(a[i]['pattern']), str(a[i]['kind']), int(a[i]['line']), int(a[i]['end_line']),
                 int(a[i]['line_num'])))
            if name == str(a[i]['path']):
                count += 1
            name = str(a[i]['path'])
    cursor.close()
    db.commit()
    db.close()


def load_json_csv(path):
    """
    Load converted standard result into selected database.
    :param path:
    :return:
    """
    file_num = []
    f_startline = []
    f_endline = []
    f = open(path, 'r')
    content = f.read()
    a = json.loads(content)
    for i in range(len(a)):
        if a[i]['kind'] != 'function':
            continue
        # if int(a[i]['end_line']) - int(a[i]['line']) > 5:
        if int(a[i]['line_num']) > 5:
            file_num.append(int(a[i]['path'].split('_')[0]))
            f_startline.append(int(a[i]['line']))
            f_endline.append(int(a[i]['end_line']))
    dataframe = pd.DataFrame({'file_num': file_num, 'startline': f_startline, 'endline': f_endline})
    dataframe.to_csv("result_lib/origin_2.csv", index=False, sep=',')



if __name__ == '__main__':
    ctags_json_parser('./source_file/tags.json', './source_file/')
    # ctags_json_parser('./sc_test/tags.json', './sc_test/')
    # load_json_sql('./sc_test/sample.json')
    # load_json_csv('./final_subset/sample.json')
    # data = pd.read_csv('result_lib/origin.csv')
    # print(data[data['file_num']==0].index.tolist())
    """with open('./sc_test/sample.json', 'r', errors='ignore') as jsonfile:
        json_string = json.load(jsonfile)
        for json_element in json_string:
            print(json_element)"""

