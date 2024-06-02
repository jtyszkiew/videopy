def get_file_name(file_path):
    return file_path.split('/')[-1].split('.')[0]


def get_file_name_without_extension(file_path):
    return file_path.split('/')[-1].split('.')[0]


def get_file_extension(file_path):
    return file_path.split('.')[-1]
