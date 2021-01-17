import sys
from vertex_clusterer import vertex_clusterer


clusters = {}

name = ""
file_number = 100
treshold = 20
shingle_size = 10
source_type='f'
print("\n...COMPUTING...\n")


try:
    clusters = vertex_clusterer(treshold, shingle_size, source_type, name, file_number)
except Exception as e:
    print(e)
print('Numero cluster ' + str(len(clusters)))
print('\nClusters: \n')
print(clusters)
file = open("results.csv", "w")
index_cluster = 0
for key in clusters:
	for page in clusters[key]:
	   file.write(str(page) + "," + str(index_cluster) + "\n")
	index_cluster += 1
file.close()
if not clusters:
    sys.exit("\nNessun cluster trovato.\n")
