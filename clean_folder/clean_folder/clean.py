from shutil import copyfile, unpack_archive
from pathlib import Path
from re import sub
import argparse
import os

known_extensions = set()
unknown_extensions = set()

result = {
    "images": [],
    "video": [],
    "documents": [],
    "audio": [],
    "archives": [],
    "other": []
}

def read_folder(path, output_folder):
    for el in path.iterdir():
        if el.is_dir():
            if el.name in ["archives", "video", "audio", "documents", "images"]:
                continue
            else:
                read_folder(el)
        else:
            copy_file(el, output_folder)

    remove_empty_folders(path)
    
def copy_file(file, output_folder):
    ext = sort(file)
    if ext == "archives":
        unarchiving(file, output_folder)
  
    else:    
        new_path = output_folder / ext
        new_path.mkdir(exist_ok=True, parents=True)
        copyfile(file, new_path / nozmalize(file.name))
    
    file.unlink()

def sort(file):
    if file.suffix[1:].upper() in ["JPEG", "PNG", "JPG", "SVG"]:
        result["images"].append(file.name)
        sort_folder = "images"
        known_extensions.add(file.suffix)
    elif file.suffix[1:].upper() in ["AVI", "MP4", "MOV", "MKV"]:
        result["video"].append(file.name)
        sort_folder = "video"
        known_extensions.add(file.suffix)
    elif file.suffix[1:].upper() in ["DOC", "DOCX", "TXT", "PDF", "XLSX", "PPTX"]:
        result["documents"].append(file.name)
        sort_folder = "documents"
        known_extensions.add(file.suffix)
    elif file.suffix[1:].upper() in ["MP3", "OGG", "WAV", "AMR"]:
        result["audio"].append(file.name)
        sort_folder = "audio"
        known_extensions.add(file.suffix)
    elif file.suffix[1:].upper() in ["ZIP", "GZ", "TAR"]:
        result["archives"].append(file.name)
        sort_folder = "archives"
        known_extensions.add(file.suffix)
    else:
        result["other"].append(file.name)
        unknown_extensions.add(file.suffix)
        sort_folder = "other"
        
    return sort_folder

def nozmalize(file):
    char_map = {
        ord('а'): 'a', ord('б'): 'b', ord('в'): 'v', ord('г'): 'h', ord('ґ'): 'g', ord('д'): 'd', 
        ord('е'): 'e', ord('є'): 'ie', ord('ж'): 'zh', ord('з'): 'z', ord('и'): 'y', ord('і'): 'i', 
        ord('ї'): 'i', ord('й'): 'i', ord('к'): 'k', ord('л'): 'l', ord('м'): 'm', ord('н'): 'n', 
        ord('о'): 'o', ord('п'): 'p', ord('р'): 'r', ord('с'): 's', ord('т'): 't', ord('у'): 'u', 
        ord('ф'): 'f', ord('х'): 'kh', ord('ц'): 'ts', ord('ч'): 'ch', ord('ш'): 'sh', ord('щ'): 'shch', 
        ord('ю'): 'iu', ord('я'): 'ia', ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V', ord('Г'): 'H', 
        ord('Ґ'): 'G', ord('Д'): 'D', ord('Е'): 'E', ord('Є'): 'Ye', ord('Ж'): 'Zh', ord('З'): 'Z', 
        ord('И'): 'Y', ord('І'): 'I', ord('Ї'): 'Yi', ord('Й'): 'Y', ord('К'): 'K', ord('Л'): 'L', 
        ord('М'): 'M', ord('Н'): 'N', ord('О'): 'O', ord('П'): 'P', ord('Р'): 'R', ord('С'): 'S', 
        ord('Т'): 'T', ord('У'): 'U', ord('Ф'): 'F', ord('Х'): 'Kh', ord('Ц'): 'Ts', ord('Ч'): 'Ch', 
        ord('Ш'): 'Sh', ord('Щ'): 'Shch', ord('Ю'): 'Yu', ord('Я'): 'Ya', ord('ь'): ''
    }

    file, extension = os.path.splitext(file)
    norm_file_name = sub(r'[^\w]', '_', file.translate(char_map))

    return norm_file_name + extension

def unarchiving(file, output_folder):
    output_folder.mkdir(exist_ok=True, parents=True)
    norm_w = file.name.replace(file.suffix, "")
    folder_for_line = output_folder / "archives" / nozmalize(norm_w)
    folder_for_line.mkdir(exist_ok=True, parents=True)
    unpack_archive(str(file.resolve()), folder_for_line.resolve())

def remove_empty_folders(path):
    if not os.path.isdir(path):
        return

    for file in os.listdir(path):
        file_path = os.path.join(path, file)

        if os.path.isdir(file_path):
            remove_empty_folders(file_path)
            if not os.listdir(file_path):
                os.rmdir(file_path)

def run():
    parser = argparse.ArgumentParser(description="Sorting folder")
    parser.add_argument("--sourse", "-s")
    parser.add_argument("--output", "-o", default="output", help="Output folder")

    args = vars(parser.parse_args())
    source = args.get("sourse")
    output = args.get("output")

    output_folder = Path(output)
    path = Path(source)
    read_folder(path, output_folder)

    print(f" Список файлів по категоріям:\n{result}\n Відомі розширення:\n{known_extensions}\n Невідомі розширення:\n{unknown_extensions}")


if __name__ == "__main__":
    run()
