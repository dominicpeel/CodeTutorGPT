
f = open("chapters.txt", "r")
chapters = {}
chapter_titles = []
chapter = 0
for line in f:
    if line[0] == "C":
        chapter += 1
        chapters[chapter] = []
        chapter_titles.append(line.strip())
    else:
        chapters[chapter].append(line.strip())

for n, topics in chapters.items():
    with open(f"chapter{n}.txt", "w") as f:
        f.write(f"Chapter {n}\n")
        for topic in topics:
            f.write(f"{topic}\n")

with open("chapter_titles.txt", "w") as f:
    for title in chapter_titles:
        f.write(f"{title}\n")
