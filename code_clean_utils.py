# -*- coding: utf-8 -*-
import re
import codecs
import mysql.connector

SPLIT_CHARS = [',','+','&','!','%','?','_','|',':','-','=','\\','~','*','^','<','>','[',']','$','{','}',';','.','`','@','(',')']
_WORD_SPLIT = re.compile(b"([,+\-&!%'_?|=\s/\*^<>$@\[\](){}#;])")

# all kind of split char
def get_split_set():
    split_set = set()
    for chars in SPLIT_CHARS:
        split_set.add(chars)

# remove all c/c++ comments from code
def remove_cpp_comment(code):
    def blotOutNonNewlines(strIn):  # Return a string containing only the newline chars contained in strIn
        return "" + ("\n" * strIn.count('\n'))

    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):  # Matched string is //...EOL or /*...*/  ==> Blot out all non-newline chars
            return blotOutNonNewlines(s)
        else:  # Matched string is '...' or "..."  ==> Keep unchanged
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    return re.sub(pattern, replacer, code)


#remove non ASCII chars
def replace_trash(unicode_string):
    for i in range(0, len(unicode_string)):
        try:
            unicode_string[i].encode("ascii")
        except:
            # means it's non-ASCII
            unicode_string = ""  # replacing it with a single space
    return unicode_string


#remove non ascii code from text
def remove_non_ascii(text):
    return ''.join([i if ord(i) < 128 else ' ' for i in text])

#line count
def line_count(file):
    count = 0
    the_file = open(file, 'rb')
    while True:
        buffer = the_file.read(8192 * 1024)
        if not buffer:
            break
        count += buffer.count('\n')
    the_file.close()
    return count


# remove standard IO and File operation line
def code_clean(text):
    patternBlank = re.compile(' +')
    patternDouble2 = re.compile('\\n\s*\\n')
    patternPrintf = re.compile('.*?print.*\r?\n')
    patternCout = re.compile('.*?cout.*\r?\n')
    patternCin = re.compile('.*?cin.*\r?\n')
    patternScanf = re.compile('.*?scanf.*\r?\n')
    patternTab = re.compile('\t')
    patternReader = re.compile('.*?Reader.*\r?\n')
    patternStream = re.compile('.*?Stream.*\r?\n')
    patternWriter = re.compile('.*?Writer.*\r?\n')

    a = re.sub(patternBlank, " ", text)
    a = re.sub(patternDouble2, "\n", a)
    a = re.sub(patternPrintf, "", a)
    a = re.sub(patternCout, "", a)
    a = re.sub(patternCin, "", a)
    a = re.sub(patternScanf, "", a)
    a = re.sub(patternTab, ' ', a)
    a = re.sub(patternReader, "", a)
    a = re.sub(patternStream, "", a)
    a = re.sub(patternWriter, "", a)

    return re.sub(r'[\xa0\s]+', ' ', a)


# remove muilti-blanks and new lines to single
def remove_blanks(text):
    patternDouble = re.compile('\\n')
    e = re.sub(patternDouble, " ", text)
    patternBlank = re.compile(' +')
    result = re.sub(patternBlank, ' ', e)

    return result


# make code anonymous, such as all number replaced by NUMBER
# all string replaced by STRING, all variable changed to VAR,etc
def code_anonymous(code):
    f = codecs.open('JoernAnalyzeStackOverflowCode/code_info/c_keyWord', 'r', 'utf8')
    lines = f.readlines()
    keyword = set()
    for line in lines:
        keyword.add(line.encode('utf-8').replace('\n', ''))

    # repalce string
    patterString = re.compile("\"(.*?)\"")
    code = re.sub(patterString, "STRING", code)

    # split by slicers
    codes = _WORD_SPLIT.split(code)

    final_code = ''
    for code in codes:
        if ((code == ' ') | (keyword.__contains__(code))):
            final_code += code
        elif (code != ''):
            # replace number
            if (code.isdigit()):
                final_code += 'NUMBER'
            # if the variable or function's name is long, we keep it
            elif (code.__len__() >= 3):
                final_code += code
            # if the variable or function's name is short, we replace it
            elif (code.__len__() < 3):
                final_code += ' VAR '
    return final_code


# make sure every split char is blan
def get_normalize_code(code,max_lenghth):

    split_set = get_split_set()
    codes= _WORD_SPLIT.split(code)
    result = ''
    count_length = 0
    for c in codes:
        if (c != ''):
            if (c in split_set):
                result += ' '+c+' '
            else:
                result += c
            count_length += 1
        if (count_length == max_lenghth):
            break
    result = " ".join(result.split())
    return result



# order AST type
def AST_type_clean(line_dict, need_repeated):
    line_code = []
    newDict = sorted(line_dict.iteritems(), key=lambda d: d[0])

    for key, value in newDict:
        if (need_repeated):
            remove_duplicated = sorted(str(value).split(' '))
        else:
            remove_duplicated = sorted(set(str(value).split(' ')))
        line_code.append(' '.join(e for e in remove_duplicated))

    return ','.join(e for e in line_code)
