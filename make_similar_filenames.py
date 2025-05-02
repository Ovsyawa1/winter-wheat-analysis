from pathlib import Path
import re


def make_similar_filenames(directory):
    text_extensions = {'.txt'}
    pattern = re.compile(r'\d+-?\d*')
    try:
        dir_path = Path(directory)
        for item in dir_path.iterdir():
            if item.is_file():
                if item.suffix.lower() in text_extensions:
                    
                        
            elif item.is_dir():
                make_similar_filenames(item)
    except FileNotFoundError as e:
        raise f"Не найден файл. Ошибка {e}"