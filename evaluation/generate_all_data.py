from random import randint
import json
from evaluation.generate_library_data import get_search_time
from evaluation.generate_synth_time_data import get_synth_time
from evaluation.library_generator import spec_library_generator
from evaluation.spec_generator import spec_generator
from goals.tools.crome_io import save_to_file
from shared.paths import output_folder


def remove_random_elements(lst, percentage):
    # Calculate the number of elements to remove
    num_to_remove = int(len(lst) * percentage / 100)
    # Create a copy of the list to remove elements from
    lst = lst.copy()
    # Remove the specified number of random elements
    for i in range(num_to_remove):
        lst.pop(randint(0, len(lst) - 1))
    return lst


def gen_times_for(min_clauses: int = 5, max_clauses: int = 10000):
    data: dict = json.load(open(output_folder / "data.json"))
    max_i = max([int(i) for i in list(data.keys())])
    min_clauses = max([max_i, min_clauses]) + 1
    for i in range(min_clauses, max_clauses, 50):
        spec, specs = spec_generator(i)
        mono_synth, clauses_synth = get_synth_time(spec, specs)
        library = spec_library_generator(i)
        library = remove_random_elements(library, 50)
        search_time, n_candidates, similarity_score = -1, -1, -1
        # search_time, n_candidates, similarity_score = get_search_time(spec, library)

        data[str(i)] = {
            "mono_synth": mono_synth,
            "clauses_synth": clauses_synth,
            "search_time": search_time,
            "n_candidates": n_candidates,
            "similarity_score": similarity_score
        }
        print(f"\n\nnew data point for i={i}")
        print(data[str(i)])

        save_to_file(data, "data.json")


if __name__ == '__main__':
    gen_times_for()
