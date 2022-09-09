import json
import re
import sqlite3
from sys import argv


def print_help():
    print('''usage: python3 sqlite2json.py [OPTIONS] [-q <query> | -t <table>] file...
  Options:
    -o <file> :  Place output into <file>
    -q <query>:  Run the <query> on the database
    -t <table>:  Select all data from <table>''')
    exit(0)


if __name__ == '__main__':
    if len(argv) == 1:
        print_help()

    db_path = out_file = query = table = ''
    i = 1
    while i < len(argv):
        s = argv[i]
        if s == '-o':
            i += 1
            out_file = argv[i]
        elif s == '-q':
            i += 1
            query = argv[i]
        elif s == '-t':
            i += 1
            table = argv[i]
        elif s == '-h':
            print_help()
        elif re.search('.db$', s):
            db_path = s
        i += 1

    if (query == '' and table == '') or db_path == '':
        print('Fatal error: too few arguments')
        print('For help use -h flag')
        exit(-1)
    if query == '':
        query = f'SELECT * FROM {table}'
    if out_file == '':
        out_file = 'output.json'

    db = sqlite3.Connection(db_path)
    cur = db.cursor()
    cur.execute(query)
    col_name = tuple([t[0] for t in cur.description])
    data = cur.fetchall()
    db.close()
    data_formatted = []

    for element in data:
        element_dict = {}
        for i in range(0, 8):
            element_dict[col_name[i]] = element[i]
        data_formatted.append(element_dict)

    json_object = json.dumps(data_formatted, indent=4)
    json_file = open(out_file, 'w+')
    json_file.write(json_object)
    json_file.close()