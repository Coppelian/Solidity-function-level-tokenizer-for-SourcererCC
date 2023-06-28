import os
import json


def getFunctions(filestring, logging, file_path, j_string):
    logging.info("Starting block-level parsing on " + file_path)
    f_path = file_path.split('/')[1]
    # print f_path
    file_string_split = filestring.split('\n')
    method_string = []
    method_pos = []
    method_name = []

    global found_parent
    found_parent = []
    # jsonfile = open('sample.json', 'r')
    # json_string = json.load(jsonfile, encoding='utf-8')
    json_string = j_string
    # json_string = unicode_convert(json_string)
    # jsonfile.close()
    for json_element in json_string:
        # json_E = json_element["path"]
        if json_element["path"].split('.')[0] == f_path.split('.')[0]:
            if json_element["kind"] != 'function':
                continue
            method_body = []
            for line in file_string_split[json_element["line"] - 1:json_element["end_line"]]:
                method_body.append(line)
            method_body = '\n'.join(method_body)
            method_pos.append((int(json_element["line"]), int(json_element["end_line"])))
            method_string.append(method_body)
            method_name.append(json_element["name"])

    if (len(method_pos) != len(method_string)):
        logging.warning("File " + file_path + " cannot be parsed. (3)")
        return (None, None, method_name)
    else:
        logging.warning("File " + file_path + " successfully parsed.")
        return (method_pos, method_string, method_name)


def unicode_convert(input_data):
    if isinstance(input_data, dict):
        return {unicode_convert(key): unicode_convert(value) for key, value in input_data.iteritems()}
    elif isinstance(input_data, list):
        return [unicode_convert(element) for element in input_data]
    elif isinstance(input_data, unicode):
        return input_data.encode('utf-8')
    else:
        return input_data


if __name__ == "__main__":
    getFunctions()
