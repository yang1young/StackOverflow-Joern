import re
import codecs
import mysql.connector
import os
import codecs
import CodeCleanUtils as cc
import re
import codeClassify
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import code_clean_utils as cc

PATH = '/home/qiaoyang/codeData/stackoverflow/'
TAGS = ['rvalue-reference','mysql', 'swig', 'heap', 'gtk', 'graph', 'serial-port', 'search', 'qml', 'initializer-list', 'graphics',
          'strtok','boost-spirit', 'crash', 'multiple-inheritance', 'cocos2d-x', 'singleton', 'udp', 'audio','unordered-map', 'ffmpeg',
          'concurrency', '2d', 'functor', 'atomic', 'generics', 'glut', 'eigen', 'qt-creator', 'bash', 'allocation','winsock','googletest',
          'shared-memory', 'csv', 'libcurl', 'sqlite', 'glsl', 'bitmap', 'nested', 'split', '3d','opencl','asynchronous', 'boost-python']
DATABASE_NAME = 'codetag'
DATABASE_USER = 'root'
PASSWORD = ''

#generate train/develope/test data from database
def prepare_data_from_database(save_path, need_anonymous, need_write_to_whole,need_normalize):
    file_object = ''
    code_train = ''
    code_dev = ''
    code_test = ''
    tag_train = ''
    tag_dev = ''
    tag_test = ''

    if (need_write_to_whole):
        file = save_path+'AllData.csv'
        file_object = codecs.open(file, 'w+', 'utf8')
    else:
        code_train = codecs.open(save_path+ 'code.train', 'w+', 'utf8')
        tag_train = codecs.open(save_path + 'tag.train', 'w+', 'utf8')

        code_dev = codecs.open(save_path + 'code.dev', 'w+', 'utf8')
        tag_dev = codecs.open(save_path + 'tag.dev', 'w+', 'utf8')

        code_test = codecs.open(save_path + 'code.test', 'w+', 'utf8')
        tag_test = codecs.open(save_path + 'tag.test', 'w+', 'utf8')

    conn = mysql.connector.connect(user=DATABASE_USER, password=PASSWORD, database=DATABASE_NAME)
    cursor_type = conn.cursor(buffered=True)

    for tag in TAGS:
        cursor_type.execute('select * from selectTagType where (Tags LIKE %s)', ('%' + tag + '%',))
        num_rows = int(cursor_type.rowcount)
        num_train = num_rows * 0.75
        num_dev =  num_rows* 0.05

        for i in range(num_rows):
            row = cursor_type.fetchone()
            code = row[1]
            if(need_anonymous):
                code = cc.code_anonymous(code)
            if(need_normalize):
                code = cc.get_normalize_code(code,300)
            if(code != ''):
                if (need_write_to_whole):
                    file_object.write(code + ' @' + tag + '\n')
                elif(i<num_train):
                    code_train.write(code + '\n')
                    tag_train.write(tag + '\n')
                elif (i < num_train+num_dev):
                    code_dev.write(code + '\n')
                    tag_dev.write(tag + '\n')
                else:
                    code_test.write(code + '\n')
                    tag_test.write(tag + '\n')

# files = os.listdir(data_from)
# files.sort(key=lambda x: x[:-2])
# file_nums = len(files)


def database_code_to_file(into_path):
    conn = mysql.connector.connect(user=DATABASE_USER, password=PASSWORD, database=DATABASE_NAME)
    cursor = conn.cursor(buffered=True)
    cursor.execute('select * from selectTag')
    num_rows = int(cursor.rowcount)

    for i in range(num_rows):
        row = cursor.fetchone()
        id = row[0]
        code = row[1]
        tag = str(row[2])
        f =  codecs.open(into_path+str(id)+'.c','w+','utf8')
        f.write(code)
        f.close()
        print i



