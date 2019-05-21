import os
import json
import shutil

DICTIONARY_NAME = 'filetype_dict.json'
FILE_NAME = os.path.basename(__file__)
CURRENT_FOLDER = os.listdir('./')


def get_unsorted_files():
    files = []
    for file in CURRENT_FOLDER:
        if os.path.isfile(file) and file not in (DICTIONARY_NAME, FILE_NAME):
            files.append(file)
    return files


def get_filetype_folder_dict():
    try:
        with open(DICTIONARY_NAME) as f:
            file_dict = json.load(f)
    except FileNotFoundError:
        file_dict = {}
        with open(DICTIONARY_NAME, 'w') as f:
            json.dump(file_dict, f)
    return file_dict


def save_dictionary_to_json(dictionary):
    with open(DICTIONARY_NAME, 'w') as f:
        json.dump(dictionary, f)


def get_folder_name_from_user(extension):
    user_input = input(f"{extension} not found in database, please enter a folder in which you would like to save {extension} files\n")
    output = ''
    folders = next(os.walk('./'))[1]
    for folder in folders:
        if folder.lower() == user_input.lower():
            output = folder
    if output == '':
        output = user_input
    return output


def move_file(filename, foldername):
    if not os.path.isfile(f'./{foldername}/{filename}'):
        shutil.move(f'./{filename}', f'./{foldername}/{filename}')
    else:
        split_name = os.path.splitext(filename)
        new_filename = split_name[0] + "-Copy" + split_name[1]
        os.rename(filename, new_filename)
        move_file(new_filename, foldername)


def main():
    unsorted_files = get_unsorted_files()
    filetype_folder_dict = get_filetype_folder_dict()
    extension_not_found_counter = 0
    for file in unsorted_files:
        file_extension = os.path.splitext(file)[1]
        if file_extension in filetype_folder_dict:
            move_file(file, filetype_folder_dict[file_extension])
        else:
            filetype_folder_dict[file_extension] = get_folder_name_from_user(file_extension)
            extension_not_found_counter += 1
    if extension_not_found_counter > 0:
        save_dictionary_to_json(filetype_folder_dict)


if __name__ == "__main__":
    main()

