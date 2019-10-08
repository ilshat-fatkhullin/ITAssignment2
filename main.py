import math
import os
import shutil


# Helper class for reading the file in formatted way
class FileReader:
    __path = ''
    __file = None
    __byte = None

    def __init__(self, path):
        self.__path = path
        self.__file = open(path, 'rb')
        self.__byte = self.__file.read(1)

    # returns next byte of the file
    def get_next(self):
        result = self.__byte
        self.__byte = self.__file.read(1)
        return result

    # returns true if there are byte to read
    def has_bytes(self):
        return self.__byte

    # closes the stream
    def close(self):
        self.__file.close()


# reads 'from_file' and writes compressed version to 'to_file'
def compress(from_file, to_file):
    file_reader = FileReader(from_file)

    # maps substring to n
    d = {b'': 0}
    s = b''

    byte = None

    with open(to_file, 'wb') as sw:
        while file_reader.has_bytes():
            byte = file_reader.get_next()
            sc = s + byte
            if sc in d:
                s = sc
            else:
                sw.write(convert_to_binary(d[s], byte))
                d[sc] = len(d)
                s = b''

        # is there are overhead which is already exist in d
        if len(s) > 0:
            sw.write(convert_to_binary(d[s], byte))


# reads 'from_file' and writes decompressed version to 'to_file'
def decompress(from_file, to_file):
    file_reader = FileReader(from_file)

    d = {}
    value = 0
    n = 1

    with open(to_file, 'wb') as sw:
        while file_reader.has_bytes():
            byte = int.from_bytes(bytes=file_reader.get_next(), signed=False, byteorder='big')
            value *= 2 ** 7
            value += byte % 128

            # if last byte
            if byte >= 128:
                x = b''
                # adding symbol byte
                x += file_reader.get_next()

                if value in d.keys():
                    x = d[value] + x

                d[n] = x

                sw.write(x)
                value = 0
                n += 1


# returns minimum amount of bits to represent given integer
def get_length_in_bits(integer):
    if integer <= 1:
        return 1
    return int(math.log2(integer)) + 1


# converts pair to required binary representation
def convert_to_binary(value, x):
    length = get_length_in_bits(value)
    number_of_bytes = math.ceil(length / 7)
    bytes = bytearray(number_of_bytes)

    for i in range(number_of_bytes - 1, -1, -1):
        bytes[i] = value % 128
        value //= 128

    # set last byte indicator
    bytes[number_of_bytes - 1] = bytes[number_of_bytes - 1] | 128
    return bytes + x


# adds suffix to file name
# {a}.{b} -> {a}{suffix}.{b}
def add_suffix(file_name, suffix):
    parts = file_name.split('.')
    return parts[0] + suffix + '.' + parts[1]


def main():
    # delete folder if exists

    if 'IlshatFatkhullinOutputs' in os.listdir('./'):
        shutil.rmtree('./IlshatFatkhullinOutputs/')

    # create directory structure

    os.mkdir('./IlshatFatkhullinOutputs/')
    os.mkdir('./IlshatFatkhullinOutputs/dataset')

    for file_type_dir in os.listdir('./dataset'):

        os.mkdir('./IlshatFatkhullinOutputs/dataset/%s' % file_type_dir)

        print('Processing: %s' % file_type_dir)

        for root, dirs, files in os.walk('./dataset/' + file_type_dir):
            for file in files:
                from_file = './dataset/%s/%s' % (file_type_dir, file)
                to_file = './IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, add_suffix(file, 'Compressed'))

                compress(from_file=from_file, to_file=to_file)

                print('%s compressed' % file)

                from_file = './IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, add_suffix(file, 'Compressed'))
                to_file = './IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, add_suffix(file, 'Decompressed'))

                decompress(from_file=from_file, to_file=to_file)

                print('%s decompressed' % file)


if __name__ == '__main__':
    main()
