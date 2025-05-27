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
		text_json = [json.loads(line)["title"] for line in e_in]

	with gzip.open(args.embed_in, "rt") as em_in:
		word_json = [json.loads(line)["word"] for line in em_in]

	with gzip.open(args.embed_in, "rt") as emb_in:
		score_json = [json.loads(line)["score"] for line in emb_in]

	df = pd.DataFrame()
	df = df.assign(text = text_json, word = word_json, score = score_json)
	df["score"] = pd.to_numeric(df["score"], errors="coerce")

	init_data = []
	for title, group in df.groupby(["text"]):
		for noun, group_two in group.groupby(["word"]):
			init_data.append({"text": title[0], "word": noun[0], "score": group_two["score"].mean()})
	#need to persist title for Kmeans labeling so not swap for id?

	holding_df = pd.DataFrame.from_records(init_data)
	data_means = holding_df.to_dict("records")
#	if isinstance(data_means, list):
#		print("is list")
#	elif isinstance(data_means, dict):
#		print("is dict")
#	else:
#		print("who knows")

	titles_df = pd.DataFrame(df.drop_duplicates(subset=["text"]))

#	for title in titles_df["text"]:
#		for data in data_means:
#	for data in data_means:
#		for title in titles_df["text"]:
#			if data["text"] == title:
#				with open(os.path.join(args.output_dir, title), "wt") as d_out:
#					d_out.write(json.dumps({"word": data["word"], "score": data["score"]}) + "\n")
	for title in titles_df["text"]:
		with open(os.path.join(args.output_dir, title), "wt") as d_out:
			for data in data_means:
				if data["text"] == title:
					d_out.write(json.dumps({"word": data["word"], "score": data["score"]}) + "\n")
					print({"text": data["text"], "word": data["word"], "score": data["score"]})
