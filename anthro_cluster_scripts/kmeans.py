import argparse
import gzip
import json
import math
import os
import numpy as np
import pickle
import torch
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
#import matplotlib
#from matplotlib.backends.backend_qtagg import PyQt5

#matplotlib.use("qtagg")

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_dir", help = "directory of per-text gz.jsonl files each with vector")
#	parser.add_argument("clusters_out", help = "produces Kmeans scatterplot")

	args = parser.parse_args()

	text_labels = []
	vectors = []
	for root, directory, files in os.walk(args.input_dir):
		for file in files:
			text_labels.append(file)
			with open(os.path.join(root, file), "rb") as f_in:
				file_line = torch.from_numpy(np.load(f_in))
				vectors.append(file_line)
						#can add .tolist() here to get rid of dtype at end

	vec = np.array(vectors)
	v_array = vec.reshape(-1, vec.shape[-1])
	kmeans = KMeans(n_clusters = 10)
	kmeans.fit(v_array)
	cluster = kmeans.predict(v_array)
	plt.scatter(v_array[:, 0], v_array[:, 1], c = cluster)

#	with open(args.clusters_out, "w") as c_out:
	for i, text in enumerate(text_labels):
		plt.annotate(text, (v_array[:, 0][i], v_array[:, 1][i]))
#		plt.savefig("kmeans.png")
		plt.show()
