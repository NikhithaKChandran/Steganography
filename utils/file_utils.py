import os


def read_file(path):
    with open(path, "rb") as f:
        return f.read()


def write_file(data, path):
    with open(path, "wb") as f:
        f.write(data)


def create_header(file_path, data):

    filename = os.path.basename(file_path)
    filesize = len(data)

    header = f"{filename}|{filesize}|"

    return header.encode()


def parse_header(data):

    first_sep = data.find(b'|')
    second_sep = data.find(b'|', first_sep + 1)

    header_end = second_sep + 1

    header = data[:header_end].decode()

    filename, filesize = header.split('|')[:2]

    return filename, int(filesize), header_end


def create_output_path(filename):

    os.makedirs("output", exist_ok=True)

    return os.path.join("output", "recovered_" + filename)