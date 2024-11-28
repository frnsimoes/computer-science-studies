import csv
import io


class QueryNode(object):
    def close(self):
        if self.child:
            self.child.close()


class Root(QueryNode):
    def next(self):
        x = self.child.next()
        if x is None:
            self.child.close()
        return x


class MemoryScan(QueryNode):
    """
    Yield all records from the given "table" in memory.

    This is really just for testing... in the future our scan nodes
    will read from disk.
    """
    def __init__(self, table):
        self.table = table
        self.idx = 0

    def next(self):
        if self.idx >= len(self.table):
            return None

        x = self.table[self.idx]
        self.idx += 1
        return x


PAGE_SIZE = 1024

class FileScan(QueryNode):
    """
    Yield all rows from the given heap file in our custom format!
    """
    def __init__(self, filename, schema):
        self.filename = filename
        self.schema = schema
        self.file = None
        self.buffer = None
        self.record_i = None  # `i` from print_dat
        self.end = None

    def next(self):
        if self.file is None:
            self.file = open(self.filename, 'rb')

        if self.buffer is None:
            self.buffer = self.file.read(PAGE_SIZE)
            if len(self.buffer) == 0:
                return None
            assert len(self.buffer) == PAGE_SIZE
            self.record_i = 0
            self.end = PAGE_SIZE

        num_records = int.from_bytes(self.buffer[0:2], 'little')
        start = int.from_bytes(self.buffer[(self.record_i+1)*2:(self.record_i+2)*2], 'little')
        rec = io.BytesIO(self.buffer[start:self.end])
        row = []
        for typ in self.schema:
            if typ == 'uint32':
                row.append(int.from_bytes(rec.read(4), 'little'))
            elif typ == 'text':
                n = int.from_bytes(rec.read(1))
                row.append(rec.read(n).decode('utf8'))
            else:
                raise ValueError('Unknown type')
        self.end = start

        self.record_i += 1
        if self.record_i == num_records:
            # reached last record on page
            self.buffer = None

        return tuple(row)

    def close(self):
        if self.file:
            self.file.close()


class CSVFileScan(QueryNode):
    """
    Yield all rows from the given table in CSV format.

    We expect the csv to use commas as delimiters, for the first row to be
    field names, and for the schema to be a sequence of types of the same
    length as *every* row of the csv
    """
    def __init__(self, filename, schema):
        self.filename = filename
        self.schema = schema
        self.file = None
        self.reader = None

    def next(self):
        if self.file is None:
            self.file = open(self.filename)
            self.reader = csv.reader(self.file)
            next(self.reader)  # discard header

        try:
            return tuple(t(v) for t, v in zip(self.schema, next(self.reader)))
        except StopIteration:
            self.file.close()
            return None

    def close(self):
        if self.file:
            self.file.close()  # TODO possible issue with double close?


class Projection(QueryNode):
    """
    Map the child records using the given map function, e.g. to return a subset
    of the fields.
    """
    def __init__(self, proj):
        self.proj = proj

    def next(self):
        x = self.child.next()
        if x is None:
            return None
        return self.proj(x)


class Selection(QueryNode):
    """
    Filter the child records using the given predicate function.

    Yes it's confusing to call this "selection" as it's unrelated to SELECT in
    SQL, and is more like the WHERE clause. We keep the naming to be consistent
    with the literature.
    """
    def __init__(self, predicate):
        self.predicate = predicate

    def next(self):
        while True:
            x = self.child.next()
            if x is None or self.predicate(x):
                return x


class Limit(QueryNode):
    """
    Return only as many as the limit, then stop
    """
    def __init__(self, n):
        self.remaining = n

    def next(self):
        if self.remaining == 0:
            return None
        self.remaining -= 1
        return self.child.next()


class Sort(QueryNode):
    """
    Sort based on the given key function
    """
    def __init__(self, key, desc=False):
        self.key = key
        self.desc = desc
        self.tuples = None
        self.idx = 0

    def next(self):
        if self.tuples is None:
            self.tuples = []
            while True:
                x = self.child.next()
                if x is None:
                    break
                self.tuples.append(x)
            self.tuples.sort(key=self.key, reverse=self.desc)
       
        if self.idx >= len(self.tuples):
            return None
        
        x = self.tuples[self.idx]
        self.idx += 1
        return x


def Q(*nodes):
    """
    Construct a linked list of executor nodes from the given arguments,
    starting with a root node, and adding references to each child
    """
    ns = iter(nodes)
    parent = root = Root()
    for n in ns:
        parent.child = n
        parent = n
    parent.child = None
    return root


def run(q):
    """
    Run the given query to completion by calling `next` on the (presumed) root
    """
    while True:
        x = q.next()
        if x is None:
            break
        yield x


if __name__ == '__main__':
    # Test data generated by Claude and probably not accurate!
    birds = (
        ('amerob', 'American Robin', 0.077, True),
        ('baleag', 'Bald Eagle', 4.74, True),
        ('eursta', 'European Starling', 0.082, True),
        ('barswa', 'Barn Swallow', 0.019, True),
        ('ostric1', 'Ostrich', 104.0, False),
        ('emppen1', 'Emperor Penguin', 23.0, False),
        ('rufhum', 'Rufous Hummingbird', 0.0034, True),
        ('comrav', 'Common Raven', 1.2, True),
        ('wanalb', 'Wandering Albatross', 8.5, False),
        ('norcar', 'Northern Cardinal', 0.045, True)
    )
    schema = (
        ('id', str),
        ('name', str),
        ('weight', float),
        ('in_us', bool),
    )

    # ids of non US birds
    assert tuple(run(Q(
        Limit(4),
        Projection(lambda x: (x[0],)),
        Selection(lambda x: not x[3]),
        MemoryScan(birds)
    ))) == (
        ('ostric1',),
        ('emppen1',),
        ('wanalb',),
    )
    
    # id and weight of 3 heaviest birds
    assert tuple(run(Q(
        Projection(lambda x: (x[0], x[2])),
        Limit(3),
        Sort(lambda x: x[2], desc=True),
        MemoryScan(birds),
    ))) == (
        ('ostric1', 104.0),
        ('emppen1', 23.0),
        ('wanalb', 8.5),
    )

    movies_types = (int, str, str)
    ratings_types = (int, int, float, str)

    assert tuple(run(Q(
        Projection(lambda x: (x[1],)),
        Selection(lambda x: x[0] == 5000),
        CSVFileScan('/Users/oz/Downloads/ml-20m/movies.csv', movies_types)
    ))) == (
        ('Medium Cool (1969)',),
    )

    assert tuple(run(Q(
        Projection(lambda x: (x[1],)),
        Selection(lambda x: x[0] == 5000),
        FileScan('movies_slotted.dat', ('uint32', 'text', 'text'))
    ))) == (
        ('Medium Cool (1969)',),
    )
    print('ok')

    
