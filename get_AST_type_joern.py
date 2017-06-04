import codecs
from joern.all import JoernSteps
from py2neo.packages.httpstream import http
import code_clean_utils as cc

http.socket_timeout = 9999


# using joern and gremline query to get AST node type
# then match type's location into source code file
def query_node_type():
    step = JoernSteps()
    step.setGraphDbURL('http://localhost:7474/db/data/')
    step.connectToDatabase()

    # get all of function in database
    query = """getNodesWithType('Function')"""
    res = step.runGremlinQuery(query)
    for function in res:
        # for one function, get type for every line
        line_dict = dict()
        function_node_id = int(function.ref[5:])
        # get map of type-location
        query = """queryNodeIndex("functionId:%i").as("x").statements().as("y").select{it.type}{it.location}""" % function_node_id
        function_nodes = step.runGremlinQuery(query)
        for node in function_nodes:
            # get node type and location
            type = str(node[0])
            location = str(node[1])
            if (location != 'None'):
                loc = str(location).split(':')[0]
                # find in line_dict
                if (line_dict.has_key(loc)):
                    temp = line_dict.get(loc) + ' ' + type
                    line_dict[loc] = temp
                else:
                    line_dict[loc] = type

        clean_type = cc.AST_type_clean(line_dict, True)
        # do another query to know which files this function belongs to
        query = """g.v(%d).in("IS_FILE_OF").filter{it.type=="File"}.filepath""" % function_node_id
        file_path = step.runGremlinQuery(query)
        file_name = str(file_path[0]).split('/')[-1]


# do the same thing with query_node_type(), this is query by chunk,
# if function count is huge, query_node_type() function will failed since you
# can not get all function in once query
def query_node_type_chunk():
    step = JoernSteps()
    step.setGraphDbURL('http://localhost:7474/db/data/')
    step.connectToDatabase()

    # get function id
    query = """getNodesWithType('Function').id"""
    res = step.runGremlinQuery(query)
    flag = 1
    CHUNK_SIZE = 51

    for chunk in step.chunks(res, CHUNK_SIZE):
        function_tuple = tuple(chunk)
        function_id_str = str(function_tuple).replace(',', '').replace('\'', '')

        # to know which files this function belongs to
        query = """idListToNodes(%s).as("x").in("IS_FILE_OF").filepath.as("y").select{it.id}{it}""" % chunk
        stms_files = step.runGremlinQuery(query)
        files = dict()
        for stms_file in stms_files:
            files[int(stms_file[0])] = str(stms_file[1]).split('/')[-1]

        query = """queryNodeIndex("functionId:%s").as("x").statements().as("y").as("z").select{it.type}{it.location}{it.functionId}""" % function_id_str
        stms = step.runGremlinQuery(query)
        # get node types
        codes = dict()
        for stm in stms:
            function_node_id = int(stm[2])
            loc = stm[1]
            type = str(stm[0])
            if (function_node_id in codes):
                codes[function_node_id].append([loc, type])
            else:
                codeList = [[loc, type]]
                codes[function_node_id] = codeList

        codesList = codes.items()
        for id, elem in codesList:
            line_dict = dict()
            for e in elem:
                location = str(e[0])
                type = e[1]
                if (location != u'None'):
                    loc = str(location).split(':')[0]
                    if (line_dict.has_key(loc)):
                        temp = line_dict.get(loc) + ' ' + type
                        line_dict[loc] = temp
                    else:
                        line_dict[loc] = type
            clean_type = cc.AST_type_clean(line_dict, True)
            fileName = files.get(id)
