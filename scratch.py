pieces = ["aaa", "bbb"]
labelled = []

for piece in pieces:
    labelled.append({"text": piece, "source": "guide.docx"})

print(len(labelled))
print(labelled[1]["text"])