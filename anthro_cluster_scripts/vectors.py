import argparse
import json
import gzip
import os
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pickle

le = LabelEncoder()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--input_dir", help = "directory of per-text gz.jsonl files of words with scores")
	parser.add_argument("counts_in", help = "gz.jsonl with full vocabulary and occurrence counts")
	parser.add_argument("--output_dir", help = "directory of per-text gz.jsonl files with vectors")

	args = parser.parse_args()

	with gzip.open(args.counts_in, "rt") as c_in:
		for line in c_in:
			jcounts = json.loads(line)
			count_list = sorted(jcounts, key=lambda x: x["count"], reverse=True)

	counts_df = pd.DataFrame(count_list)
	counts_df.sort_values("count", ascending=False)
	counts_df.iloc[:1000, df.columns.get_loc("word")]

	for word in counts_df["word"]:
		enc_labels = le.fit_transform(word)

	dec_labels = le.inverse_transform(enc_labels)
	print(dec_labels)

	for directory, files in os.walk(args.input_dir):
		for file in files:
			print(file)
			with gzip.open(os.path.join(directory, file), "r") as f_in, gzip.open(os.path.join(args.output_dir, file), "wb") as v_out:
				jline = json.loads(line)
				pre_vector = []
#				for word in le.inverse_transform(enc_labels):
				for word in dec_labels:
					if jline["word"] == word:
						slot = dec_labels.index(word)
						pre_vector.insert(slot, word)
						np.array([pre_vector])
						#index of score is le.transform()
						#this needs to 
							#anthro_vector = np.array([#?])
						np.save(v_out, anthro_vector)
						pickle.dump(anthro_vector, v_out)

#reverse get words from le, put score of word in respective index position
