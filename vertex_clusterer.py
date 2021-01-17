import operator
from collections import OrderedDict
import utils

def vertex_clusterer(pruning, shingle, source_type, name, link_number):
    page_shingle_dict = {}  # filename della pagina
    clusters = {}  # set di pagine nel cluster
    shingle_dict = {}  # Shingle vector o masked shingle vector
    pruning_treshold = pruning  # Default: 20
    shingle_size = shingle  # Default: 10

    page_shingle_dict = utils.read_file(shingle_size)

    for vector in page_shingle_dict.values():
        temporary_dict = utils.generate_6_7_from_8_shingle_vec(vector)
        shingle_dict = utils.dict_shingle_occurencies(shingle_dict, temporary_dict)


    shingle_dict = OrderedDict(sorted(shingle_dict.items(), key = operator.itemgetter(1)))

    for vector in shingle_dict:
        matching_vectors_dict = {}
        if '*' not in vector:
            matching_vectors_dict = utils.matching_vectors(
                vector, shingle_dict)
            del matching_vectors_dict[max(
                matching_vectors_dict.items(), key = operator.itemgetter(1))[0]]
            for key in matching_vectors_dict:
                if '*' in key:
                    shingle_dict[key] -= shingle_dict[vector]

    shingle_dict = {key: val for key, val in shingle_dict.items() if val >= pruning_treshold or '*' not in key}

    shingle_masked_dict = {key: val for key, val in shingle_dict.items() if '*' in key}

    for masked_vector in shingle_masked_dict:
        clusters[masked_vector] = set()

    for page in page_shingle_dict:
        try:
            matching_dict = utils.matching_vectors(page_shingle_dict[page], shingle_masked_dict)
            best_shingle = max(matching_dict.items(), key = operator.itemgetter(1))[0]
            clusters[best_shingle].add(page)
        except:
            continue
    clusters = {key: val for key, val in clusters.items() if val}
    return clusters
