import argparse
import math
import re
from argparse import ArgumentError
from collections import Counter

pattern = r'(^[-+]?([0-9]+)(\.[0-9]+)?)$'


def is_number(num):
    match = re.match(pattern, num)
    return num if match else None


def extract_numbers(string):
    numbers = []
    for num in string.split():
        r = is_number(num)
        if r:
            numbers.append(r)
        else:
            print(f"{num} is not a long. It will be skipped.")
    return numbers


def find_longest_string(last_string, current_string):
    len_last_string = len(last_string)
    len_current_string = len(current_string)
    if len_last_string > len_current_string:
        return last_string
    elif len_last_string == len_current_string:
        return last_string if last_string > current_string else current_string
    else:
        return current_string


def read_from_file(file_name):
    with open(file_name, mode="r") as file:
        data = [line.strip() for line in file.readlines() if line]
    return data


def write_to_file(file_name, data_list):
    data_str = "\n".join(data_list)
    with open(file_name, mode="w") as file:
        file.write(data_str)


def for_long(sorting_type, reverse, input_file=None):
    number_list = []
    if input_file:
        lines = read_from_file(input_file)
        for line in lines:
            result = extract_numbers(line)
            number_list.extend(result)
    else:
        while True:
            try:
                data = input()
                if not data:
                    break
                result = extract_numbers(data)
                number_list.extend(result)
            except EOFError:
                break
    n_numbers = len(number_list)
    output = []
    if sorting_type == 'natural':
        sorted_number_list = sorted(number_list, key=int, reverse=reverse)
        output.append(f"Total numbers: {n_numbers}.")
        output.append("Sorted data: " + " ".join(sorted_number_list))
    else:
        counts = Counter(number_list)
        sorted_counts = sorted(counts.items(), key=lambda x: (int(x[1]), int(x[0])))
        output.append(f"Total numbers: {n_numbers}.")
        for num, count in sorted_counts:
            output.append(f"{num}: {count} time(s), {math.floor(count / n_numbers * 100)}%")
    return output


def for_line(sorting_type, reverse, input_file=None):
    key = None if sorting_type == 'natural' else len
    line_list = []
    longest_line = ''
    if input_file:
        lines = read_from_file(input_file)
        for line in lines:
            line_list.append(line)
            longest_line = find_longest_string(longest_line, line)
    else:
        while True:
            try:
                data = input()
                if not data:
                    break
                line_list.append(data)
                longest_line = find_longest_string(longest_line, data)
            except EOFError:
                break
    n_lines = len(line_list)
    output = []
    if sorting_type == "natural":
        sorted_line_list = sorted(line_list, key=key, reverse=reverse)
        output.append(f"Total lines: {n_lines}.")
        output.append("Sorted data:")
        output.append("\n".join(sorted_line_list))
    else:
        counts = Counter(line_list)
        sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]))
        output.append(f"Total numbers: {n_lines}.")
        for num, count in sorted_counts:
            output.append(f"{num}: {count} time(s), {math.floor(count / n_lines * 100)}%")
    return output


def for_word(sorting_type, reverse, input_file=None):
    word_list = []
    longest_word = ''
    if input_file:
        lines = read_from_file(input_file)
        for line in lines:
            word_list.extend(line.split())
    else:
        while True:
            try:
                data = input()
                if not data:
                    break
                word_list.extend(data.split())
            except EOFError:
                break
    for word in word_list:
        longest_word = find_longest_string(longest_word, word)
    n_word_list = len(word_list)
    output = []
    if sorting_type == "natural":
        sorted_word_list = sorted(word_list, key=None, reverse=reverse)
        output.append(f"Total words: {n_word_list}.")
        output.append(f"Sorted data: {' '.join(sorted_word_list)}")
    else:
        counts = Counter(word_list)
        sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]))
        output.append(f"Total numbers: {n_word_list}.")
        for num, count in sorted_counts:
            output.append(f"{num}: {count} time(s), {math.floor(count / n_word_list * 100)}%")
    return output


def main(**kwargs):
    sorting_type = kwargs['sortingType'] if kwargs['sortingType'] in ['natural', 'byCount'] else 'natural'
    input_file = kwargs['inputFile'] if kwargs['inputFile'] else None
    output_file = kwargs['outputFile'] if kwargs['outputFile'] else None
    if kwargs['dataType'] == 'word':
        r = for_word(sorting_type=sorting_type, reverse=False, input_file=input_file)
        if output_file:
            write_to_file(output_file, r)
        else:
            print(*r, sep="\n")
    elif kwargs['dataType'] == 'line':
        r = for_line(sorting_type=sorting_type, reverse=False, input_file=input_file)
        if output_file:
            write_to_file(output_file, r)
        else:
            print(*r, sep="\n")
    elif kwargs['dataType'] == 'long':
        r = for_long(sorting_type=sorting_type, reverse=False, input_file=input_file)
        if output_file:
            write_to_file(output_file, r)
        else:
            print(*r, sep="\n")
    else:
        r = for_word(sorting_type=sorting_type, reverse=False, input_file=input_file)
        if output_file:
            write_to_file(output_file, r)
        else:
            print(*r, sep="\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple command-line program', exit_on_error=False)
    parser.add_argument('-dataType', help='Data type file to process')
    parser.add_argument('-sortingType', help='Sort type file to process')
    parser.add_argument('-inputFile', help='Input file name')
    parser.add_argument('-outputFile', help='Output file name')

    try:
        args, unknown = parser.parse_known_args()
    except ArgumentError as err:
        if 'dataType' in str(err):
            print('No data type defined!')
        elif 'sortingType' in str(err):
            print('No sorting type defined!')
    else:
        for unknown_args in unknown:
            print(f'-{unknown_args}" is not a valid parameter. It will be skipped.')

        main(**vars(args))
