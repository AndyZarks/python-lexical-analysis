import re


def pre(filename: str) -> list:
    file = open(filename, encoding='utf8').read()
    wordlist = [word for word in file]
    return wordlist


def make_map(fact: bool, maps: list, key: str, category: str = None, seq: list = None):
    if fact:
        for i, element in enumerate(seq, start=1):
            if key == element:
                maps.append([key, f'{category}{i}'])
                break
    else:
        maps.append([key, 'ERROR'])


def proc(w_l: list, c_l: list, n_l: list, v_l: list) -> list:
    my_maps = []
    str_v = ''
    str_n = ''
    i = 0
    while i < len(w_l):
        # 处理空白字符
        if re.search(r'\s', w_l[i]):
            i += 1
        # 处理变量
        elif re.search('[A-Za-z]', w_l[i]):
            while re.search('[A-Za-z]', w_l[i]):
                str_v += w_l[i]
                if i < len(w_l) - 1:
                    i += 1
                else:
                    break
            if len(str_v) < 10:
                if str_v == 'over':
                    break
                elif str_v not in c_l:
                    v_l.append(str_v)
                    make_map(True, my_maps, str_v, 'v', v_l)
                else:
                    make_map(True, my_maps, str_v, 'v', c_l)
                str_v = ''
            else:
                make_map(False, my_maps, str_v)
                str_v = ''
        # 处理数字
        elif re.search(r'\d', w_l[i]):
            while re.search(r'\d', w_l[i]):
                str_n += w_l[i]
                i += 1
            n_l.append(str_n)
            make_map(True, my_maps, str_n, 'n', n_l)
            str_n = ''
        # 处理非数字字母下划线
        else:
            if w_l[i] + w_l[i + 1] == '==':
                make_map(True, my_maps, '==', 'c', c_l)
                i += 2
            elif w_l[i] + w_l[i + 1] == '>=':
                make_map(True, my_maps, '>=', 'c', c_l)
                i += 2
            elif w_l[i] + w_l[i + 1] == '<=':
                make_map(False, my_maps, '<=', 'c', c_l)
                i += 2
            elif w_l[i] + w_l[i + 1] == '!=':
                make_map(False, my_maps, '!=')
                i += 2
            elif w_l[i] + w_l[i + 1] == '++':
                make_map(True, my_maps, '++', 'c', c_l)
                i += 2
            elif w_l[i] + w_l[i + 1] == '--':
                make_map(False, my_maps, '--')
                i += 2
            elif w_l[i] + w_l[i + 1] == '&&':
                make_map(False, my_maps, '&&')
                i += 2
            elif w_l[i] + w_l[i + 1] == '||':
                make_map(False, my_maps, '||')
                i += 2
            elif w_l[i] in c_l:
                make_map(True, my_maps, w_l[i], 'c', c_l)
                i += 1
            else:
                make_map(False, my_maps, w_l[i])
                i += 1
    return my_maps


def analysis(filename):
    character_list = ['if', 'then', 'else', 'int', 'char', 'for', '=', '>=', '==', '-', '+', '/', '%', '++', '"', ',', ';']
    num_list = []
    variable_list = []
    wordlist = pre(filename)
    maps = proc(wordlist, character_list, num_list, variable_list)
    print(f'以下是{filename}的词法分析报告:')
    for _map_ in maps:
        print(f'{_map_[0]}\t({_map_[0]}, {_map_[1]})')
    print('over\n')


analysis('test_code1.txt')
analysis('test_code2.txt')
analysis('test_code3.txt')
