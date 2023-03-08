with open("fgvk.py", "r", encoding="utf-8") as f:
    with open("output.txt", "w", encoding="utf-8") as w:
        for line in f:
            if "text =" in line and "{" not in line:
                try:
                    sor = line.strip().split('"')
                    w.write(line.strip().split('"')[1])
                except:
                    pass
                w.write("\n")