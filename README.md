# JoernAnalyzeStackOverflowCode
From stackoverflow get Q&A data, extract code and tags, then using joern tool
get partial code AST and convert AST node type to text
* how to use stackoverflow data
* how to use joern to do code analyse, get AST/DDG/CFG,etc
* how to write gremlin query to visit AST tree stored in Neo4j
* how to convert AST to Text

## Data source
* If you want using Stackoverflow Q&A data, you don't need to write a Crawler,
Stackoverflow has dump all his data and publish it ,you can find here:
https://archive.org/details/stackexchange
* If you don't  know which table you should use, maybe you can start from Posts
https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z
* If you want to try it instead of download all data,you can use online query:
https://data.stackexchange.com/stackoverflow/query/new
* If you want to know more about SO data,you can find here:
https://data.stackexchange.com/stackoverflow/queries

## Joern (a platform for robust analysis of C/C++ code)
* Joern is a robust parser for C/C++ storing abstract syntax trees, control flow graphs and
program dependence graphs in a neo4j graph database. You can get code from :
https://github.com/octopus-platform/joern
* If you want to know about how to install and use Joern, read this:
http://joern.readthedocs.io/en/latest/

### Tips for install Joern
If you follow official guide strictly, you may still encounter some problems, so make
sure the following steps:
1. java version ,better 1.8
2. Neo4J Server 2.1.5 Community Edition, if you can't find in it's official guide:
    wget http://dist.neo4j.org/neo4j-community-2.1.5-unix.tar.gz
3. choose py2neo 2.0 when install python-joern, you can use this site:
   https://pypi.python.org/pypi/py2neo/2.0
4. When istalling gremlin-plugin, you need do mvn clean package, if error occurs,
   you should change all of  the license file data to 2017

### Tips for using Joern
1. Import your code correctly, following this:
    http://joern.readthedocs.io/en/latest/tutorials/unixStyleCodeAnalysis.html#importing-the-code
2. When you need to start Neo4j, using this command in case of error:
   > $NEO4J/bin/neo4j start-no-wait
3. rm .joernIndex dir before doing a new import
4. you can't update Neo4j when it's on running, you need to close it first

## File introduce
1. code_info  some file of types/keyword of different language
2. extrac_code_from_StackOverflow  java code to get question and it's answers from database
3. code_clean_utils.py  tools to do cleaning for code and text
4. get_AST_type_joern.py  gremlin query to get AST node type from Neo4j
5. stackoverflow_data_clean.py get training and testing dataset

### If you think this project may helpful, may you give me a star? :)