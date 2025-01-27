import json
from typing import Callable, Dict
from pathlib import Path
import logging.config


logging.config.fileConfig('logging.ini')
logger = logging.getLogger('root')


def load_last_save(file_path:Path):
    """Carrega o último valor salvo ou retorna 0 se não existir."""
    if file_path.exists():
        return int(file_path.read_text())
    
    file_path.write_text("0")
    return 0


def add_last_save(file_path:Path, last):
    """Salva o último valor em um arquivo."""
    file_path.write_text(str(last))


def save_json(file_path, dump_data):
    """Salva os dados no formato JSON."""
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(dump_data, file, ensure_ascii=False, indent=4)


def load_content(file_path):
    """Carrega o conteúdo de um arquivo JSON, retornando uma lista vazia se o arquivo não existir."""
    if file_path.exists():
        with file_path.open(encoding="utf-8") as file:
            return json.load(file)
    return []


def Save(func: Callable[[Dict], Dict]) -> Callable[[Path, Path, Path, int, int], None]:
    def process_data(content_path, file_path, last_save_file, batch=10, final_range=50):
        """Processa e salva os dados com base nas condições fornecidas."""
        content = load_content(content_path)
        last = load_last_save(last_save_file)

        dump_data = load_content(file_path)

        for i in range(last, final_range):

            obj = func(content[i])

            dump_data.append(obj)
            if (i + 1) % batch == 0:
                save_json(file_path, dump_data)
                last += batch
                add_last_save(last_save_file, last)
                logger.info(f"Salvamento do arquivo: {file_path} Ultimo indice: | {last:>6}|")
    return process_data



