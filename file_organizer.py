import os
import pickle
from time import sleep
import fire
import shutil
import pathlib

default_paths = []
interval_time = 15
system_ = ""
GREEN = '\033[1;32;40m'


extensions = {
    # audio
    '.aif': 'media/audio',
    '.cda': 'media/audio',
    '.mid': 'media/audio',
    '.midi': 'media/audio',
    '.mp3': 'media/audio',
    '.mpa': 'media/audio',
    '.ogg': 'media/audio',
    '.wav': 'media/audio',
    '.wma': 'media/audio',
    '.wpl': 'media/audio',
    '.m3u': 'media/audio',
    # text
    '.txt': 'text/text_files',
    '.doc': 'text/text_files',
    '.docx': 'text/text_files',
    '.odt ': 'text/text_files',
    '.pdf': 'text/text_files',
    '.rtf': 'text/text_files',
    '.tex': 'text/text_files',
    '.wks ': 'text/text_files',
    '.wps': 'text/text_files',
    '.wpd': 'text/text_files',
    # video
    '.3g2': 'media/video',
    '.3gp': 'media/video',
    '.avi': 'media/video',
    '.flv': 'media/video',
    '.h264': 'media/video',
    '.m4v': 'media/video',
    '.mkv': 'media/video',
    '.mov': 'media/video',
    '.mp4': 'media/video',
    '.mpg': 'media/video',
    '.mpeg': 'media/video',
    '.rm': 'media/video',
    '.swf': 'media/video',
    '.vob': 'media/video',
    '.wmv': 'media/video',
    '.ai': 'media/images',
    '.bmp': 'media/images',
    '.gif': 'media/images',
    '.jpg': 'media/images',
    '.jpeg': 'media/images',
    '.png': 'media/images',
    '.ps': 'media/images',
    '.psd': 'media/images',
    '.svg': 'media/images',
    '.tif': 'media/images',
    '.tiff': 'media/images',
    '.cr2': 'media/images',
    # internet
    '.asp': 'other/internet',
    '.aspx': 'other/internet',
    '.cer': 'other/internet',
    '.cfm': 'other/internet',
    '.cgi': 'other/internet',
    '.pl': 'other/internet',
    '.css': 'other/internet',
    '.htm': 'other/internet',
    '.js': 'other/internet',
    '.jsp': 'other/internet',
    '.part': 'other/internet',
    '.php': 'other/internet',
    '.rss': 'other/internet',
    '.xhtml': 'other/internet',
    '.html': 'other/internet',
    # compressed
    '.7z': 'other/compressed',
    '.arj': 'other/compressed',
    '.deb': 'other/compressed',
    '.pkg': 'other/compressed',
    '.rar': 'other/compressed',
    '.rpm': 'other/compressed',
    '.tar.gz': 'other/compressed',
    '.z': 'other/compressed',
    '.zip': 'other/compressed',
    # disc
    '.bin': 'other/disc',
    '.dmg': 'other/disc',
    '.iso': 'other/disc',
    '.toast': 'other/disc',
    '.vcd': 'other/disc',
    # data
    '.csv': 'programming/database',
    '.dat': 'programming/database',
    '.db': 'programming/database',
    '.dbf': 'programming/database',
    '.log': 'programming/database',
    '.mdb': 'programming/database',
    '.sav': 'programming/database',
    '.sql': 'programming/database',
    '.tar': 'programming/database',
    '.xml': 'programming/database',
    '.json': 'programming/database',
    # executables
    '.apk': 'other/executables',
    '.bat': 'other/executables',
    '.com': 'other/executables',
    '.exe': 'other/executables',
    '.gadget': 'other/executables',
    '.jar': 'other/executables',
    '.wsf': 'other/executables',
    # fonts
    '.fnt': 'other/fonts',
    '.fon': 'other/fonts',
    '.otf': 'other/fonts',
    '.ttf': 'other/fonts',
    # presentations
    '.key': 'text/presentations',
    '.odp': 'text/presentations',
    '.pps': 'text/presentations',
    '.ppt': 'text/presentations',
    '.pptx': 'text/presentations',
    # programming
    '.c': 'programming/c&c++',
    '.class': 'programming/java',
    '.java': 'programming/java',
    '.py': 'programming/python',
    '.sh': 'programming/shell',
    '.h': 'programming/c&c++',
    # spreadsheets
    '.ods': 'text/microsoft/excel',
    '.xlr': 'text/microsoft/excel',
    '.xls': 'text/microsoft/excel',
    '.xlsx': 'text/microsoft/excel',
    # system
    '.bak': 'text/other/system',
    '.cab': 'text/other/system',
    '.cfg': 'text/other/system',
    '.cpl': 'text/other/system',
    '.cur': 'text/other/system',
    '.dll': 'text/other/system',
    '.dmp': 'text/other/system',
    '.drv': 'text/other/system',
    '.icns': 'text/other/system',
    '.ico': 'text/other/system',
    '.ini': 'text/other/system',
    '.lnk': 'text/other/system',
    '.msi': 'text/other/system',
    '.sys': 'text/other/system',
    '.tmp': 'text/other/system'
}
folder_name_available = ["Audio", "Video", "Image", "Text", "Compressed", "Disc", "Programming", "System", "Others"]
audio_formats = ['.aif', '.cda', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl', '.m3u']
image_formats = ['.ai', '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.cr2']
text_formats = ['.txt', '.doc', '.docx', '.odt ', '.pdf', '.rtf', '.tex', '.wks ', '.wps', '.wpd']
video_formats = ['.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm',
                 '.swf', '.vob', '.wmv']
compressed_formats = ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip']
disc_formats = ['.bin', '.dmg', '.iso', '.toast', '.vcd']
programming_format = ['.py', '.c', 'cpp', '.class', '.html', '.htm', '.css', '.js', '.dart']
system_formats = ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk',
                  '.msi', '.sys', '.tmp']

map_formats = {
    'Audio': ['.aif', '.cda', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl', '.m3u'],
    'Video': ['.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf',
              '.vob', '.wmv'],
    'Image': ['.ai', '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.cr2'],
    'Text': ['.ai', '.bmp', '.gif', '.jpg', '.jpeg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.cr2', '.docx',
             '.csv'],
    'Compressed': ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip'],
    'Disc': ['.bin', '.dmg', '.iso', '.toast', '.vcd'],
    'Programming': ['.py', '.c', 'cpp', '.class', '.html', '.htm', '.css', '.js', '.dart'],
    'System': ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ico', '.ini', '.lnk', '.msi',
               '.sys', '.tmp'],
    'Others': []
}
config_file_name = "default_data.txt"


def checker_function():
    try:
        if(len(default_paths)!=0):
            for detail_ in default_paths:
                path = detail_["path"]
                err_list = detail_["default_paths"]
                files_ = []
                if (len(files_) == 0):
                    print(f"{path}: No Files")
                else:
                    print(*files_)
                for f in os.listdir(path):
                    if (os.path.isfile(path + "/" + f)):
                        files_.append(f)
                for file_ in files_:
                    exten_sion = pathlib.Path(file_).suffix
                    folder = finding_file_formats(exten_sion, err_list)
                    print(path + '/' + file_, path + "/" + folder + "/" + file_)
                    shutil.move(path + "/" + file_, path + "/" + folder + "/" + file_)
            return [True, "Nothing"]
        else:
            print("In order to start the automation, First you have to add some path")
            print("the command is: 'python3 file_organizer add_path --path=\"your\path\dir\"'")
            return [False,"No path"]
    except Exception as msg:
        print(msg)
        return [True, "problem"]


def starting_the_application():
    try:
        while True:
            check, msg = checker_function()
            if check:
                print("Status: Working")
                sleep(5)
            else:
                return [check, msg]
    except KeyboardInterrupt:
        print("Stopping automation")
    except Exception as msg:
        print("Error: ",msg)
        print("Stopping automation")


def new_user():
    try:
        df = {
            "default_paths": [],
            "system_": system_,
            "interval_time": interval_time
        }
        pickle.dump(df, open("default_data.txt", "wb"))
        for path_ in default_paths:
            bool_, error_ = making_the_folder(map_formats, path_)
        return [True, "No_msg"]
    except Exception as msg:
        return [False, msg]


def setting_default_value():
    try:
        file_ = open("default_data.txt", "rb")
        file_read = file_.read()

        if len(file_read) <= 10:
            status, error_msg = new_user()
            if status:
                return [True, "No_msg"]
            else:
                return [False, error_msg]
        else:
            data_ = pickle.loads(file_read)
            global system_, interval_time, default_paths
            system_ = data_["system_"]
            interval_time = int(data_["interval_time"])
            default_paths = data_["default_paths"]
            return [True, "NO_Error"]
    except Exception as msg:
        return [False, msg]

def starting_the_main_automation():
    setting_default_value()
    starting_the_application()


def finding_file_formats(file_extension, err_list):
    key_ = err_list.items()
    for value_ in key_:
        if (file_extension in value_[1]):
            return value_[0]
    return "Others"


def making_the_folder(folders_list, path):
    try:
        for folder in folders_list.keys():
            try:
                os.mkdir(path=path + "\\" + folder)
                print(f"{folder} had been created successfully")
            except Exception as msg:
                print(msg)
        return [True, "No_Error"]
    except Exception as msg:
        return [False, msg]


def adding_folder_function(path):
    if (os.path.isdir(path)):
        global default_paths, interval_time, system_
        setting_default_value()
        for p_ in default_paths:
            if (p_["path"] == path):
                return "Path is already exit."
        try:
            try:
                file_ = open("default_data.txt", "rb+")
                file_read = file_.read()
                if len(file_read) != 10:
                    data_ = pickle.loads(file_read)
                    system_ = data_["system_"]
                    interval_time = int(data_["interval_time"])
                    default_paths = data_["default_paths"]
                value_ = {
                    "path": path,
                    "default_paths": map_formats,
                }
                default_paths.append(value_)
            except:
                value_ = {
                    "path": path,
                    "default_paths": map_formats,
                }
                default_paths.append(value_)
            df = {
                "default_paths": default_paths,
                "system_": system_,
                "interval_time": interval_time,
            }
            file_ = open("default_data.txt", "w+")
            file_.truncate()
            file_.close()
            pickle.dump(df, open("default_data.txt", "wb"))
            bool_, error_ = making_the_folder(map_formats, path)
        except Exception as msg:
            print(msg)
    else:
        print("Invalid path, please verify your path")


def remove_files_path():
    key_list = []
    setting_default_value()
    index = 1
    print()
    if (len(default_paths) != 0):
        for path in default_paths:
            print(index, ": ", path["path"])
            key_list.append([index, path["path"]])
            index += 1
        print()
        valid = input("Enter the key which you want to remove: ")
        try:
            valid = int(valid)
            for key in key_list:
                if (key[0] == valid):
                    for path in default_paths:
                        if (key[1] == path["path"]):
                            default_paths.remove(path)
                            print(f"{path['path']} had removed")
                    df = {
                        "default_paths": default_paths,
                        "system_": system_,
                        "interval_time": interval_time,
                    }
                    file_ = open("default_data.txt", "w+")
                    file_.truncate()
                    file_.close()
                    pickle.dump(df, open("default_data.txt", "wb"))
        except Exception as msg:
            return [False, msg]
    else:
        print("Nothing to remove")


# fire config

if __name__ == "__main__":
    fire.Fire({
        "start": starting_the_main_automation,
        "add_path": adding_folder_function,
        "remove_path": remove_files_path
    })
