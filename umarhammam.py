#!/usr/bin/python3
import sys
import os
import shutil
import argparse
import re
import json
import chardet

def main():

    # regex pattern untuk melakukan parsing ke nginx error log
    pattern =   (r''
                '^(?P<timestamp>\d{4}/\d{2}/\d{2}\ \d{2}:\d{2}:\d{2})'
                '\ \[(?P<severity>emerg|alert|crit|error|warn|notice|info)\]'
                '\ (?P<process_id>\d+)'
                '\#(?P<thread_id>\d+):'
                '\ \*(?P<connection_id>\d+)'
                '\ (?P<message>.+?)'
                ',\ client:\ (?P<client_ip>\d+\.\d+\.\d+\.\d+)'
                ',\ server:\ (?P<server>.+?)'
                ',\ request:\ (?P<request>.+?)'
                '(?:,\ host:\ \"(?P<host>.+?)\")?'
                '$'
                )

    # setup argparse untuk parsing arguments yg dimasukkan 
    # oleh user (inputfile, -t, -o)
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str, help="input file (nginx error log)")
    parser.add_argument("-t", type=str, choices=["text", "json"], default="text", help="type, text or json")
    parser.add_argument("-o", type=str, help="output file")
    
    args = parser.parse_args()

    # inputfile
    inputfile = os.path.abspath(args.inputfile)

    # outputfile
    # jika user tidak memasukkan -o/outputfile, output disimpan 
    # di current working directory 
    # dgn nama file ".nginx_error_log.txt" atau ".nginx_error_log.json"
    if args.o:
        outputfile = args.o
    else:
        if args.t == "text":
            outputfile = ".nginx_error_log.txt"
        else:
            outputfile = ".nginx_error_log.json"

    # user memilih type: text
    # cukup copy saja ke outputfile
    if args.t == "text":
        try:
            shutil.copyfile(inputfile, outputfile)
        except OSError as e:
            print(e)
            return

        print("output file has been saved to " + outputfile)

    # user memilih type json
    if args.t == "json":
        # cara: ekstrak tiap baris log dengan menggunakan regex pattern di 
        # atas. lalu append 
        # ke dalam list "lines" di bawah ini, lalu dump ke outputfile
        lines = []

        try:
            encoding = chardet.detect(open(inputfile, mode="rb").read())['encoding']
            # read inputfile
            with open(inputfile, mode="r", encoding=encoding) as filehandle_i:
                # baris per baris
                for line in filehandle_i:
                    r = re.compile(pattern)

                    # ekstrak menggunakan regex pattern di atas.
                    # match_obj.groupdict() akan menghasilkan dictionary.
                    # list_of_dict akan berisi:
                    # [{'timestamp': '2021/07/11 07:19:30', 
                    # 'severity': 'error', ...dst}]
                    list_of_dict = [match_obj.groupdict() for match_obj in r.finditer(line.strip())]
                    
                    # append ke lines
                    lines.append(list_of_dict[0])
                    
        except OSError as e:
            print(e)
            return

        # open outputfile
        try:
             filehandle_o = open(outputfile, mode="w", encoding="utf-8")
        except OSError as e:
            print(e)
            return

        # dump ke outputfile
        json.dump(lines, fp=filehandle_o, indent=2)
        filehandle_o.close()

        print("output file has been saved to " + outputfile)
        
if __name__ == "__main__":
    main()
