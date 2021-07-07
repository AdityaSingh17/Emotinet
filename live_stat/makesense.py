lines_seen = set()  # Holds lines already seen.
outfile = open("SensiblePredictions.txt", "w")
infile = open("RawPredictions.txt", "r")

for line in infile:
    if line not in lines_seen:  # If current line is not a duplicate.
        outfile.write(line)
        lines_seen.add(line)
outfile.close()
