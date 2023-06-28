import pandas as pd
from tqdm import tqdm
import json
import numpy as np


# Process file_states to csv
def traverse_scc_results(path_1, path_2):
    with open(path_1, 'r') as f:
        with open(path_2, 'w') as f_2:
            for line in f.readlines():
                if line.startswith('f'):
                    continue
                else:
                    f_2.writelines(line[1:])
            f_2.close()
        f.close()


# Process bookkeeping proj to csv
def to_csv(path_1, path_2):
    with open(path_1, 'r') as f:
        with open(path_2, 'w') as f_2:
            for line in f.readlines():
                f_2.writelines(line)
            f_2.close()
        f.close()


# Convert token source file to csv
def convert_tokens(path_1, path_2):
    with open(path_1, 'r') as f:
        with open(path_2, 'w') as f_2:
            for line in f.readlines():
                lists = line.split(',')
                sequence = (lists[0], lists[1], lists[2], lists[3])
                new_line = ','.join(sequence)
                f_2.writelines(new_line + '\n')
            f_2.close()
        f.close()


# Generate token files
def create_token_comparison(path_1, path_2, path_3, path_4):
    df_1 = pd.read_csv(path_1, header=None, names=['a', 'b', 'c', 'd'])
    df_2 = pd.read_csv(path_2, header=None, names=['a', 'b', 'c'])
    df_3 = pd.read_csv(path_3, header=None, names=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    list_1 = []
    for index, row in tqdm(df_1.iterrows()):
        file_num, block_hash, token_number, section_number = row
        file_name = df_2[(df_2['a'] == file_num)]
        for index_1, row_1 in file_name.iterrows():
            file_number = row_1['b'].split('/')[1].split('_')[0]
            continue
        line_info = df_3[(df_3['b'] == block_hash)]
        for index_2, row_2 in line_info.iterrows():
            f_startline = row_2['g']
            f_endline = row_2['h']
            continue
        list_1.append([file_number, f_startline, f_endline, token_number, section_number, block_hash])
        # print('0')
    list_2 = ['file_num', 'f_startline', 'f_endline', 'token_number', 'section_number', 'block_hash']
    df = pd.DataFrame(data=list_1, columns=list_2)
    df.to_csv(path_4, index=None)


def compare_results(path_1, path_2, path_3):
    # sourcererCC token results
    df_1 = pd.read_csv(path_1)
    # nicad
    df_2 = pd.read_csv(path_2)
    list_1 = []
    count = 0
    count_1 = 0
    df_1['file_name'] = df_1['file_name'].apply(lambda x: new_rule(x))
    #print(df_1)
    for index, row in tqdm(df_2.iterrows()):
        count += 1
        file_id, f_startline, f_endline = row
        # e_filename = 'source_zip/' + file_name.split('.')[0] + '.zip'
        token_number = df_1[(df_1['file_name'] == str(file_id)) & (df_1['f_startline'] == f_startline)]
        # print(token_number)
        #token_number = df_1[(df_1['file_name'] == file_id) & (df_1['f_startline'] == f_startline)]
        for index_2, row_2 in token_number.iterrows():
            token_number = row_2['token_number']
        try:
            if token_number < 29:
                reason = 1
                count_1 += 1
            else:
                reason = 2
        except BaseException as e:
            # not identified by scc
            print(row)
            print(e)
            reason = 3
            token_number = 0
        list_1.append([file_id, f_startline, f_endline, token_number, reason])
    list_2 = ['file_id', 'f_startline', 'f_endline', 'token_number', 'reason']
    df = pd.DataFrame(data=list_1, columns=list_2)
    df.to_csv(path_3, index=None)
    print(count)
    print(count_1)
    print("The portion is: ", count_1 / count)


def new_rule(x):
    print(x)
    return x.split('/')[1].split('_')[0]


def compare_results_2(path_1, path_2):
    df_1 = pd.read_csv(path_1)
    df_2 = pd.read_csv(path_2)
    count = 0
    for index, row in tqdm(df_1.iterrows()):
        if row['reason'] == 2:
            # print(row)
            # print(row['reason'])
            df = df_2[(df_2['file_name'] == row['file_name']) & (df_2['f_startline'] == row['f_startline'])].shape[0]
            # print(df_2[(df_2['file_name'] == row['file_name']) & (df_2['f_startline'] == row['f_startline'])])
            # print(df)1
            # print('o')
            if df < 1:
                row['reason'] = 4
                count += 1
            df_1.iloc[index] = row
    print(df_1['reason'].value_counts())
    print(count)
    df_1.to_csv('./temp/nicad_only_test.csv', index=None)


def check_dup(path1):
    pd1 = pd.read_csv(path1, engine='python', encoding='utf-8')
    ss1 = pd1.drop_duplicates(keep='first', inplace=False)
    print(pd1.shape[0])
    print(ss1.shape[0])


def extract_scc_pairs(path_1, path_2):
    df_1 = pd.read_csv(path_1)
    list_1 = []
    list_2 = []
    with open(path_2, 'r') as f:
        for line in tqdm(f.readlines()):
            element = line.strip().split(',')
            df_e1 = df_1[df_1['block_hash'] == int(element[1])]
            df_e2 = df_1[df_1['block_hash'] == int(element[3])]
            # ele_test = df_e1.iloc[0, 0]
            ele_1 = str(df_e1.iloc[0, 0]) + '_' + str(df_e1.iloc[0, 1]) + '_' + str(df_e1.iloc[0, 2])
            ele_2 = str(df_e2.iloc[0, 0]) + '_' + str(df_e2.iloc[0, 1]) + '_' + str(df_e2.iloc[0, 2])
            list_1.append([ele_1, ele_2])
            ele = ele_1 + '_' + ele_2
            list_2.append(ele)
    list_3 = ['func_1', 'func_2']
    df = pd.DataFrame(data=list_1, columns=list_3)
    df.to_csv('./temp/scc_clonepairs.csv', index=None)
    np_array = np.array(list_2)
    np.save('temp/npy/scc_pairs_serialized.npy', np_array)


def extract_scc_dec_pairs(path_1, path_2):
    df_1 = pd.read_csv(path_1)
    list_1 = []
    list_2 = []
    with open(path_2, 'r') as f:
        for line in tqdm(f.readlines()):
            element = line.strip().split(',')
            df_e1 = df_1[df_1['block_hash'] == int(element[1])]
            df_e2 = df_1[df_1['block_hash'] == int(element[3])]
            # ele_test = df_e1.iloc[0, 0]
            ele_1 = str(df_e1.iloc[0, 0]) + '_' + str(df_e1.iloc[0, 1]) + '_' + str(df_e1.iloc[0, 2])
            ele_2 = str(df_e2.iloc[0, 0]) + '_' + str(df_e2.iloc[0, 1]) + '_' + str(df_e2.iloc[0, 2])
            list_1.append([ele_1, ele_2])
            ele = ele_1 + '_' + ele_2
            list_2.append(ele)
    list_3 = ['func_1', 'func_2']
    df = pd.DataFrame(data=list_1, columns=list_3)
    df.to_csv('./temp/scc_dec_clonepairs.csv', index=None)
    np_array = np.array(list_2)
    np.save('temp/npy/scc_dec_pairs_serialized.npy', np_array)


def extract_scc_info(i):
    number = str(i)
    path_1 = '../SccResult/' + number + '/blocks_tokens/files-tokens-0.tokens'
    path_2 = '../SccResult/' + number + '/blocks_tokens/files-tokens-0.csv'
    convert_tokens(path_1, path_2)
    path_3 = '../SccResult/' + number + '/bookkeeping_projs/bookkeeping-proj-0.projs'
    path_4 = '../SccResult/' + number + '/bookkeeping_projs/bookkeeping-proj-0.csv'
    to_csv(path_3, path_4)
    path_5 = '../SccResult/' + number + '/file_block_stats/files-stats-0.stats'
    path_6 = '../SccResult/' + number + '/file_block_stats/files-stats-0.csv'
    traverse_scc_results(path_5, path_6)
    path_7 = '../SccResult/' + number + '/blocks_tokens/files-tokens-0.csv'
    path_8 = '../SccResult/' + number + '/bookkeeping_projs/bookkeeping-proj-0.csv'
    path_9 = '../SccResult/' + number + '/file_block_stats/files-stats-0.csv'
    path_10 = '../SccResult/' + number + '/scc_token_result.csv'
    create_token_comparison(path_7, path_8, path_9, path_10)
    print(str(i) + ' is done.')
    # path_11 = './temp/scc_sc/scc_token_result.csv'
    # path_12 = './temp/scc_sc/results.pairs'
    # extract_scc_pairs(path_11, path_12)
    
    
def ext_scc_simple(path):
    path_1 = path + '/blocks_tokens/files-tokens-0.tokens'
    path_2 = path + '/blocks_tokens/files-tokens-0.csv'
    convert_tokens(path_1, path_2)
    path_3 = path + '/bookkeeping_projs/bookkeeping-proj-0.projs'
    path_4 = path + '/bookkeeping_projs/bookkeeping-proj-0.csv'
    to_csv(path_3, path_4)
    path_5 = path + '/file_block_stats/files-stats-0.stats'
    path_6 = path + '/file_block_stats/files-stats-0.csv'
    traverse_scc_results(path_5, path_6)
    path_7 = path + '/blocks_tokens/files-tokens-0.csv'
    path_8 = path + '/bookkeeping_projs/bookkeeping-proj-0.csv'
    path_9 = path + '/file_block_stats/files-stats-0.csv'
    path_10 = path + '/scc_token_result.csv'
    create_token_comparison(path_7, path_8, path_9, path_10)
    print(path + ' is done.')


def extract_function_info(path_1, path_2):
    file = pd.read_csv(path_1)
    list_1 = []
    # list_func_info = []
    for index, row in file.iterrows():
        x, y = row['func_1'], row['func_2']
        if x not in list_1:
            list_1.append(x)
        if y not in list_1:
            list_1.append(y)
    np.save(file=path_2, arr=np.array(list_1))


def e_f():
    path_1 = './temp/scc_clonepairs.csv'
    path_2 = './temp/npy/scc_pairs_element.npy'
    extract_function_info(path_1, path_2)


def e_f_2():
    path_1 = './temp/scc_dec_clonepairs.csv'
    path_2 = './temp/npy/scc_dec_pairs_element.npy'
    extract_function_info(path_1, path_2)


def e_f_3():
    path_1 = './temp/nicad_clonepairs.csv'
    path_2 = './temp/npy/nicad_pairs_element.npy'
    extract_function_info(path_1, path_2)


def e_f_4():
    path_1 = './temp/scc_dec_converted_clonepairs.csv'
    path_2 = './temp/npy/scc_dec_converted_pairs_element.npy'
    extract_function_info(path_1, path_2)


def compare_serialized(path_1, path_2, path_3, path_4, path_5, path_6):
    list_1 = list(np.load(path_1, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII'))
    list_2 = list(np.load(path_2, mmap_mode=None, allow_pickle=False, fix_imports=True, encoding='ASCII'))
    list_dup = []
    list_dup_ele = []
    list_1_unique = []
    list_2_unique = []
    for i in tqdm(list_1):
        ele = i.split('_')
        ele_1 = ele[0] + '_' + ele[1] + '_' + ele[2]
        ele_2 = ele[3] + '_' + ele[4] + '_' + ele[5]
        if i in list_2:
            list_dup.append(i)
            list_dup_ele.append([ele_1, ele_2])
        else:
            list_1_unique.append([ele_1, ele_2])
    for i in tqdm(list_2):
        if i not in list_dup:
            ele = i.split('_')
            ele_1 = ele[0] + '_' + ele[1] + '_' + ele[2]
            ele_2 = ele[3] + '_' + ele[4] + '_' + ele[5]
            list_2_unique.append([ele_1, ele_2])
    np.save(file=path_3, arr=np.array(list_dup_ele))
    np.save(file=path_4, arr=np.array(list_1_unique))
    np.save(file=path_5, arr=np.array(list_2_unique))
    np.save(file=path_6, arr=np.array(list_dup))


def com_s():
    path_1 = 'temp/npy/n_pairs_serialized.npy'
    path_2 = 'temp/npy/scc_pairs_serialized.npy'
    path_3 = 'temp/npy/dup_pairs.npy'
    path_4 = 'temp/npy/n_pairs_unique.npy'
    path_5 = 'temp/npy/s_pairs_unique.npy'
    path_6 = 'temp/npy/n_s_dup_serialized.npy'
    compare_serialized(path_1, path_2, path_3, path_4, path_5, path_6)


if __name__ == '__main__':
    # for i in range(1,15):
    #     extract_scc_info(i)
    # e_f_4()
    # com_s()
    # ext_scc_simple('./380_result/scc')
    ext_scc_simple('.')
    # ext_scc_simple('temp_recall/scc_def')
