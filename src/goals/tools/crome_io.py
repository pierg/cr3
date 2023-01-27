# type: ignore
import json
import os
import pickle
from pathlib import Path
from typing import OrderedDict
import collections

from matplotlib.figure import Figure

from shared.paths import output_folder

def sort_dict_hierarchically(d):
    # Create an ordered dictionary
    ordered_dict = collections.OrderedDict()

    # Recursively sort the sub-dictionaries
    for key, value in sorted(d.items()):
        if isinstance(value, dict):
            ordered_dict[key] = sort_dict_hierarchically(value)
        else:
            ordered_dict[key] = value
    return ordered_dict

def sort_dict_by_int_keys(d):
    # Create an ordered dictionary
    ordered_dict = {}

    # Sort the dictionary by key
    for key, value in sorted(d.items(), key=lambda item: int(item[0])):
        ordered_dict[int(key)] = value

    return ordered_dict


def sort_dictionary(d):
    # myKeys = list(d.keys())
    # myKeys.sort()
    # sorted_dict = {i: d[i] for i in list(d.keys()).sort}
    try:
        if isinstance(d, list):
            for v in d:
                sort_dictionary(v)
            # return sorted(sort_dictionary(v) for v in d)
        if isinstance(d, dict):
            new_dict = {}
            for k in sorted(list(d.keys())):
                new_dict[k] = sort_dictionary(d[k])
            return new_dict
            # return {k: sort_dictionary(d[k]) for k in sorted(list(d.keys()))}
        return d
    except Exception as e:
        print(e)
    return d


#

def save_to_file(
        file_content: str | dict | Figure | object,
        file_name: str | None = None,
        folder_name: str | None = None,
        absolute_path: Path | None = None,
        sort: bool = True,
        overwrite: bool = False,
) -> Path:

    if folder_name is not None:
        file_folder = output_folder / folder_name
    elif absolute_path is not None:
        if absolute_path.suffix == "":
            file_folder = absolute_path
        else:
            file_folder = absolute_path.parent
            file_name = absolute_path.name
    else:
        file_folder = f"{output_folder}"

    if Path(file_name).suffix == "" and isinstance(file_content, dict):
        file_name += ".json"
    elif Path(file_name).suffix == "" and isinstance(file_content, Figure):
        file_name += ".pdf"
    elif Path(file_name).suffix == "" and isinstance(file_content, str):
        file_name += ".txt"
    elif Path(file_name).suffix == "":
        file_name += ".dat"

    if folder_name is not None and absolute_path is not None:
        raise AttributeError

    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    file_path: Path = Path(file_folder) / file_name

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    _write_file(file_content, file_path, sort=sort, overwrite=overwrite)

    print(f"{file_name} saved in {str(file_path)}")
    return file_path


def _write_file(file_content: str | dict | Figure | object, absolute_path: Path, sort: bool = True,
                overwrite: bool = False):
    # if not overwrite:
    #     absolute_path = rename_if_already_exists(absolute_path)
    if isinstance(file_content, OrderedDict):
        with open(absolute_path, "w") as f:
            file_content = json.dumps(file_content, indent=4)
            json.dump(json.loads(file_content), f, indent=4, sort_keys=False)
        f.close()
    elif isinstance(file_content, dict):
        # file_content_origin = file_content
        if sort:
            # file_content = sort_dictionary(file_content)
            file_content = sort_dict_by_int_keys(file_content)

        file_content = json.dumps(file_content, indent=4)
        if Path(absolute_path).suffix != ".json":
            absolute_path_str = str(absolute_path) + ".json"
            absolute_path = Path(absolute_path_str)
        with open(absolute_path, "w") as f:
            json.dump(json.loads(file_content), f, indent=4)
        f.close()
    elif isinstance(file_content, Figure):
        file_content.savefig(absolute_path)
    elif isinstance(file_content, str):
        with open(absolute_path, "w") as f:
            f.write(file_content)
        f.close()
    else:
        with open(absolute_path, "wb") as f:
            try:
                pickle.dump(obj=file_content, file=f)
            except Exception as e:
                raise e
        f.close()
