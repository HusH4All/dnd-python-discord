import os


def get_all_files(directory, folders_only=False):
    file_names = []

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)

        if folders_only:
            if os.path.isdir(file_path):
                file_names.append(file_path)
        else:
            if os.path.isfile(file_path):
                file_names.append(file_path)

    return file_names
