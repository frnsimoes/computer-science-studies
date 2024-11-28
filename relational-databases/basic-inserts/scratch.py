"""

Scope:

    - Write a FileScan node for the executor that sequentially scans our custom file format
    - Organize file into pages of 4096B each
    - Each page will have line pointers at the top, records at the bottom (growing bottom to top)
    - Individual records will be either fixed width (e.g. a uint32) or length prefixed / pascal strings of max 255 bytes
    - Ideally also support nulls


Plan:

    - Add support for slotted pages
    - Incorporate it as a FileScan
    - Extras like supporting null maps
"""

import csv
import io

schema = ('uint32', 'text', 'text')

"""
Slotted pages:

    uint16 for number of records
    array of uint16s as "line pointers" that indicate the start of each record
    --- space ---
    records from bottom to top
"""

PAGE_SIZE = 1024

"""
with open('movies.csv', 'r') as f:
    reader = csv.reader(f)
    print(next(reader))
    with open('movies_slotted.dat', 'wb') as out:
        # TODO more than one page
        buffer = bytearray(PAGE_SIZE)
        num_records = 0
        records_ptr = PAGE_SIZE
        for row in reader:
            record = io.BytesIO()
            for typ, val in zip(schema, row):
                if typ == 'uint32':
                    record.write(int(val).to_bytes(4, 'little'))
                elif typ == 'text':
                    bs = val.encode('utf8')
                    record.write(len(bs).to_bytes(1))
                    record.write(bs)
                else:
                    raise ValueError('Unknown type')
            record.seek(0)
            rec_bytes = record.read()
            start = records_ptr-len(rec_bytes)
            if start < (num_records + 2) * 2:
                out.write(buffer)
                buffer = bytearray(PAGE_SIZE)
                num_records = 0
                records_ptr = PAGE_SIZE
                continue
            buffer[start:records_ptr] = rec_bytes
            num_records += 1
            buffer[0:2] = num_records.to_bytes(2, 'little')
            buffer[num_records*2:(num_records+1)*2] = start.to_bytes(2, 'little')
            records_ptr = start
            assert(len(buffer) == PAGE_SIZE)
        if num_records > 0:
            out.write(buffer)


"""

def print_dat():
    """
    Read the slotted page data file and print results
    """
    with open('movies_slotted.dat', 'rb') as f:
        while True:
            buffer = f.read(PAGE_SIZE)
            if len(buffer) == 0:
                break
            assert len(buffer) == PAGE_SIZE
            num_records = int.from_bytes(buffer[0:2], 'little')
            records_ptr = PAGE_SIZE
            for i in range(num_records):
                start = int.from_bytes(buffer[(i+1)*2:(i+2)*2], 'little')
                rec = io.BytesIO(buffer[start:records_ptr])
                row = []
                for typ in schema:
                    if typ == 'uint32':
                        row.append(int.from_bytes(rec.read(4), 'little'))
                    elif typ == 'text':
                        n = int.from_bytes(rec.read(1))
                        row.append(rec.read(n).decode('utf8'))
                    else:
                        raise ValueError('Unknown type')
                print(row)
                records_ptr = start

print_dat()


print('---')
