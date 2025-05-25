import argparse
import json
import gzip
import pandas as pd
import math
import os

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embed_in", help = "gz.jsonl with embeddings file")
	parser.add_argument("--output_dir", help = "directory of files per text with scores averaged across multiple occurrences")

	args = parser.parse_args()

	with gzip.open(args.embed_in, "rt") as e_in:
		text_json = [{"text": json.loads(line)["title"]} for line in e_in]
		word_json = [{"word": json.loads(line)["word"]} for line in e_in]
		score_json = [{"score": json.loads(line)["score"]} for line in e_in]
		df = pd.DataFrame()
		df = df.assign(text = text_json, word = word_json, score = score_json)
		df["score"] = pd.to_numeric(df["score"], errors="coerce")

	data_means = []
	for noun, group in df.groupby(["word"]):
		for title, group_two in group.groupby(["text"]):
			data_means.append({"text": title[0], "word": noun[0], "score": group_two["score"].mean()})
	print(df.head(20))
	#need to persist title for Kmeans labeling so don't swap for id

#	df.loc = [df.groupby(["word"]).transform("nunique") > 2)

	for text in file:
		with open(os.path.join(args.output_dir, df["title"]), "wt") as d_out:
			for text in data_means["text"]:
				d_out.write(json.dumps({"text": data_means["text"], "word": data_means["word"], "score": data_means["score"]}) +"\n")
