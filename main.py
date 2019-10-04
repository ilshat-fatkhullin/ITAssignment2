import math
import os
import time


def compress(bytes_to_compress):
    d = {b'': 0}
    s = b''
    t = []

    result = b''

    ti = time.time()

    for byte in bytes_to_compress:
        byte = int.to_bytes(byte, length=1, byteorder='big', signed=False)
        sc = s + byte
        if sc in d:
            s = sc
        else:
            t.append((d[s], byte))
            d[sc] = len(d)
            s = b''

    print(time.time() - ti)
    ti = time.time()

    if len(s) > 0:
        t.append(t[d[s] - 1])

    for k, v in t:
        result += convert_to_binary(k, v)

    print(time.time() - ti)
    return result


def decompress(bytes):
    d = {}

    result = b''

    i = 0
    value = 0
    n = 1

    while i < len(bytes):
        byte = bytes[i]
        value *= 2 ** 7
        value += byte % 128
        if byte >= 128:
            i += 1

            x = b''
            x += int.to_bytes(bytes[i], length=1, signed=False, byteorder='big')

            if value in d.keys():
                x = d[value] + x

            d[n] = x

            result += x
            value = 0
            n += 1
        i += 1

    return result


def get_length_in_bits(integer):
    if integer <= 1:
        return 1
    return int(math.log2(integer)) + 1


def convert_to_binary(value, x):
    length = get_length_in_bits(value)
    number_of_bytes = math.ceil(length / 7)
    result = 0

    degree = 1

    for i in range(number_of_bytes):
        result += (value % 128) * degree
        value //= 128
        degree *= 128
        if i == 0:
            result += degree
        degree *= 2

    result *= 256
    result = result ^ int.from_bytes(bytes=x, byteorder='big', signed=False)
    return int.to_bytes(result, length=number_of_bytes + 1, byteorder='big', signed=False)


def read_file(path):
    file = b''
    with open(path, 'rb') as sr:
        byte = sr.read()
        while byte:
            file += byte
            byte = sr.read()
    return file


def write_file(path, array):
    with open(path, 'wb') as sw:
        sw.write(array)


def compress_to_file(from_file, to_file):
    input_file = read_file(from_file)
    compressed = compress(input_file)
    write_file(to_file, compressed)


def decompress_to_file(from_file, to_file):
    input_file = read_file(from_file)
    decompressed = decompress(input_file)
    write_file(to_file, decompressed)


def main():
    # compress_to_file(from_file='./dataset/exe/file1.exe',
    #                 to_file='./IlshatFatkhullinOutputs/dataset/exe/file1.exe')

    os.mkdir('./IlshatFatkhullinOutputs/')
    os.mkdir('./IlshatFatkhullinOutputs/dataset')

    for file_type_dir in os.listdir('./dataset'):

        os.mkdir('./IlshatFatkhullinOutputs/dataset/%s' % file_type_dir)

        print('Processing: %s' % file_type_dir)

        for root, dirs, files in os.walk('./dataset/' + file_type_dir):
            for file in files:
                compress_to_file(from_file='./dataset/%s/%s' % (file_type_dir, file),
                                 to_file='./IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, file))

                print('%s compressed' % file)

                decompress_to_file(from_file='./IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, file),
                                   to_file='./IlshatFatkhullinOutputs/dataset/%s/%s' % (file_type_dir, 'decompressed_' + file))

                print('%s decompressed' % file)


if __name__ == '__main__':
    main()
