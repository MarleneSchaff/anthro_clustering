import argparse
import gzip
import json
from collections import Counter

c = Counter()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("embed_in", help = "gz.jsonl with embeddings")
	parser.add_argument("counts", help = "gz.jsonl with counts")

	args = parser.parse_args()

	anthrodict = []

	with gzip.open(args.embed_in, "rt") as e_in:
		for line in e_in:
			jline = json.loads(line)
			for word in jline["word"]:
				anthro_noun = jline["word"]
				c[anthro_noun] += 1
				anthrodict.append({"word": anthro_noun, "score": jline["score"]})
				print("first part finished")

	print("second part")
	with gzip.open(args.counts, "wt") as c_out:
		for something in anthrodict:
			c_out.write(json.dumps({"word": something["word"], "count": c[something["word"]]}))
			print(c[something["word"]])
