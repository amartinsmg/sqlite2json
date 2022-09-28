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


def db2json(db_path: str, query: str) -> str:
    try:
        db = sqlite3.Connection(db_path)
    except Exception as e:
        raise f'Connection to database failed: {e}'
    else:
        try:
            cur = db.cursor()
            cur.execute(query)
        except Exception as e:
            raise f'Database Query failed: {e}'
        else:
            cols_name = tuple([t[0] for t in cur.description])
            data = cur.fetchall()
            data_formatted = []
            for row in data:
                row_dict = {}
                for i in range(len(cols_name)):
                    if row[i] is not None:
                        row_dict[cols_name[i]] = row[i]
                data_formatted.append(row_dict)
            json_object = json.dumps(data_formatted, indent=4)
        db.close()
        return json_object


if __name__ == '__main__':
    if len(argv) == 1:
        print_help()

    db_path = out_file = query = table = ''
    i = 1
    while i < len(argv):
        s = argv[i]
        if re.search('.db$', s):
            db_path = s
        elif s == '-o':
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
        i += 1

    if (query == '' and table == '') or db_path == '':
        print('Fatal error: too few arguments')
        print('For help use -h flag')
        exit(-1)
    if query == '':
        query = f'SELECT * FROM {table}'

    try:
        json_object = db2json(db_path, query)
        if out_file == '':
            print(json_object)
        else:
            try:
                json_file = open(out_file, 'w+')
            except Exception as e:
                raise f'Could not open the JSON file: {e}'
            else:
                json_file.write(json_object)
                json_file.close()
    except Exception as e:
        print(e)
        exit(-1)
