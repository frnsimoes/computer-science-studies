## Big picture: architecture of a dbms

**Modules**:

QUery parsing and optmization: its job is to parse and check the sql, verify it is legal, and then translate into a relational query plan that the system can execute.

Relational operators: the actual operators that are used in the plan. Individual algos that is put together to execute a data flow. Data flow operates on records and files pumping data through the operators to generate output answers to the query.

Files and index management: organize tables and records as group of pages.

Buffer management: provides the illusion that we are operating in memory and not in disk.

Disk space management: translate page request from the buffer into physical bits on one or more devices.

**Hardware**

Page: 32k object.

READ: transfer page of data from disk to ram.
WRITE: transfer page of data from ram to disk.

**Block level storage**

- read and write large chunks of sequential bytes
- "contiguous" disk block is fastest
- predict future behavior:
    - cache popular blocks
    - pre-fetch likely-to-be-accessed blocks
    - buffer writes to sequential blocks
    
A block is a unit of transfer between disk and ram. Page is a common synonym for block.

**Files**

Overview: Files of pages od records

- Tablews stored as logical files
    - consist of pages
        - pages contain a collection of records

- Pages are managed
    - on disk by the disk space manager: pages read/written to physical disk/files
    - in memory by the buffer manager: higher levers of dbms only operate in memory

**DB Files**
A collection of pages, each containing a collection of records.

**File structures**
Unordered heap file: records placed arbitrarily in pages.
Clustered file: records and pages are grouped
Sorted file: pages and records are in sorted order
Index file: B+ trees, linear hashing, may contain records or point to records in other files

**unordered heap file**
- records are placed arbitrarily in pages
- as file shrinks and grows, records are deallocated

**Layout of individual pages**

**The header**

Contains:
- number of records
- free space
- maybe a next/last pointer
- bitmaps, slot table
