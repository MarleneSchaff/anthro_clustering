import argparse
import json
import gzip
import os
import pandas as pd
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

	count_list = []
	with gzip.open(args.counts_in, "rt") as c_in:
		for line in c_in:
			jcounts = json.loads(line)
			count_list.append({"word": jcounts["word"], "count": jcounts["count"]})

	counts_df = pd.DataFrame(count_list)
	counts_df = counts_df.sort_values(by=["count"], ascending=False)
	counts_df.drop_duplicates(subset=["count"], inplace=True)
	counts_df = counts_df.head(512)

	enc_labels = le.fit_transform(counts_df["word"])
	dec_labels = le.inverse_transform(enc_labels)

	for root, directory, files in os.walk(args.input_dir):
		for file in files:
			print(file)
			with gzip.open(os.path.join(root, file), "r") as f_in, gzip.open(os.path.join(root, file), "r") as file_in, gzip.open(os.path.join(args.output_dir, file), "wb") as v_out:
				#try:
				word_json = [json.loads(line)["word"] for line in f_in]
				score_json = [json.loads(line)["score"] for line in file_in]
				df = pd.DataFrame()
				df = df.assign(word = word_json, score = score_json)
				df["score"] = pd.to_numeric(df["score"], errors="coerce")
				pre_vector = []
				for word in dec_labels:
					if word in df["word"]:
						print(word)
						slot = np.where(dec_labels == word)[0][0]
						pre_vector.insert(slot, df[df["word"] == word]["score"])
					else:
						slot = np.where(dec_labels == word)[0][0]
						pre_vector.insert(slot, 0)
				anthro_vector = np.array(pre_vector)
				print(anthro_vector)
				np.save(v_out, anthro_vector)
				pickle.dump(anthro_vector, v_out)
#				except:
#					print("gzip error")
