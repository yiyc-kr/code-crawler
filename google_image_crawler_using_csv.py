#! /usr/bin/env python
# coding: utf-8

import argparse
import requests
from random import uniform
from time import sleep
import csv
import re


def write_data(output_path, code, item, date, parse_item=False):
    with open(output_path, 'w', encoding="utf-8") as f:
        wr = csv.writer(f)
        for i, v in enumerate(item):
            if not parse_item:
                wr.writerow([code[i], v])
            else:
                v_sp = v.split(';')
                for v_item in v_sp:
                    wr.writerow([re.sub('\D', '', code[i]), v_item.strip()])


def make_search_list(csv_path, output_path, skip_column):
    print("##### Parse CSV #####")

    f = open(csv_path, 'r', encoding='utf-8')
    rdr = csv.reader(f)

    g = open(output_path, 'w', encoding='utf-8', newline='')
    wr = csv.writer(g)

    if skip_column:
        next(rdr, None)

    for line in rdr:
        code = line[0]
        real_keyword = line[1]
        parsed_keyword = re.sub('[^a-zA-Z\- ]+', ' ', real_keyword)
        parsed_keyword = ' '.join([w for w in parsed_keyword.split() if len(w) > 1])

        splited_keyword = parsed_keyword.split()
        if len(splited_keyword) > 4:
            for i in range(4, len(splited_keyword) + 1):
                segments_keyword = ' '.join(splited_keyword[:i])
                wr.writerow([code, real_keyword, segments_keyword])
        else:
            wr.writerow([code, real_keyword, parsed_keyword])
        # if real_keyword != parsed_keyword:
        #     print(code, '\t\t', real_keyword, '\t\t', parsed_keyword)
    f.close()
    g.close()


def main():
    parser = argparse.ArgumentParser(description="Crawling Google Image using CSV File")

    # options
    parser.add_argument('--csv_path', dest="csv_path", type=str, default="./data/list.csv",
                        help="Input CSV File Path")

    parser.add_argument('--output_path', dest="output_path", type=str, default="./data/parsed_list.csv",
                        help="Output Parsed CSV File Path")

    parser.add_argument('--skip_column', dest="skip_column", type=bool, default=False, nargs='?', const=True,
                        help="Parse data")

    parser.add_argument('--image_path', dest="image_path", type=str, default="./data/image",
                        help="Output Image Directory Path")

    flags, unused_flags = parser.parse_known_args()

    make_search_list(flags.csv_path, flags.output_path, flags.skip_column)

    write_data(flags.output_path, code, item, date, flags.parse_item)


if __name__ == '__main__':
    main()
