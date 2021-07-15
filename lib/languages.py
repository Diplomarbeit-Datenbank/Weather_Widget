"""
    This file is to refactor english language in other languages with one text file

    The text file have to be the following syntax:
        : # is the key to set new language (example: #german)
          -> know: write no Capital letters (german != German)
        : write under the # the words to refactor (example: weather=Wetter)
          -> leave no spaces between!

    Example File is the languages_test_file.txt in the same directory
"""

__date__ = '08.07.2021'
__completed__ = '9.07.2021'
__work_time__ = 'about 4 Hours'
__author__ = 'Christof Haidegger'
__version__ = '1.02'
__licence__ = 'Common Licence'
__debugging__ = 'Christof Haidegger'

import sys

try:
    from lib.basics.encode import Encode_umlauts
except ModuleNotFoundError:
    raise ModuleNotFoundError('Module encode is not in directory: .../lib/basics/encode.py')


class Language:
    """
        Class to refactor the words just call it with the file path
    """
    def __init__(self, file_path, language='german'):
        """

        :param file_path: path to the file to compile
        :type: string
        :param language:  language to select
        :type: string

        :raises: *FileNotFoundError when the path to the file is not correct
        """
        try:
            self.file_pointer = open(file_path, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('File not found: ' + file_path)

        self.language = language
        self.file_path = file_path

        # Dict with all the words form the text file
        self.refactor_data = self.read_file()

        self.file_pointer.close()

    def read_file(self):
        """

        :return: the dict data
        """
        encoded_file = Encode_umlauts(self.file_pointer.read())  # decode the umlauts in the files
        read_file = encoded_file.encode().split("\n")  # read the lines of the file
        right_language_strings = dict()  # create new dict for saving the words for faster refactoring
        language_line_index = None  # index where the language starts

        # find the index of the language in the file
        for counter, line in enumerate(read_file):
            if line.find('#' + str(self.language)) != -1:
                language_line_index = counter

        # when index is None the language is not found in the file
        if language_line_index is None:
            print('[Warning] selected language not found in file: ' + self.file_path +
                  ' english will be returned (Remember to write no Capital Letters #german != #German)',
                  file=sys.stderr)
            return None

        else:
            # calc language_line_index + 1 because the index is set to the declaration line of the language
            language_line_index += 1
            # first dict entry will be the selected language
            right_language_strings['language'] = self.language

            # write the language data into the dict
            for line_counter in range(len(read_file) - language_line_index):
                data = read_file[line_counter + language_line_index].split("=")
                if len(data) == 1 and data[0] == '':
                    continue  # to get the blank lines in the file
                # new language is found
                if data[0].find('#') != -1:
                    break
                # syntax error in the language text file
                if len(data) != 2:
                    raise Exception('Failed to compile file: ' + self.file_path + ' Error in line: ' +
                                    str(line_counter) + " (" + str(data) + ")")
                right_language_strings[data[0]] = data[1]

        return right_language_strings

    def refactor(self, string):
        """

        :param string: word or string to return in the right language
        :return:       the right language if possible, otherwise the same param as give
        """
        if self.refactor_data is not None:
            try:
                return self.refactor_data[string]
            # KeyError raises, when the given string is not found in the language dict
            except KeyError:
                print('[Warning] word: "' + string + '" is not found in language data | return string', file=sys.stderr)
                return string

        else:
            print('[Warning] No Language Data | return string', file=sys.stderr)
            return string


def main():
    """

    : this is only to test the software
    """
    lang = Language('languages_test_file.txt', language='german')
    print(lang.refactor_data)
    print(lang.refactor('shit'))

    return 0


if __name__ == '__main__':
    main()
