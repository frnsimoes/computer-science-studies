import csv

schema = ('uint32', 'text', 'text')

with open("/home/frns/Downloads/ml-20m/movies.csv", "r") as f:
        with open('movies.data', 'wb') as out:
            reader = csv.reader(f)
            next(reader)
            for i, row in enumerate(reader):
                for typ, val in zip(schema, row):
                    if typ == "uint32":
                        out.write(int(val).to_bytes(4, "little"))
                    elif typ == "text":
                        bs = val.encode("utf-8")
                        out.write(len(bs).to_bytes(1))
                        out.write(bs)
                    else:
                        raise ValueError(f"Unknown type: {typ}")
        

with open('movies.data', 'rb') as f:
    while f.peek():
        row = []
        for typ in schema:
            if typ == 'uint32':
                row.append(int.from_bytes(f.read(4), "little"))
            elif typ == 'text':
                n = int.from_bytes(f.read(1))
                row.append(f.read(n).decode("utf8"))
            else:
                raise ValueError("Unknown type: {typ}")

        print(row)


