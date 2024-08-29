**Disk-oriented DBMS**:

There are some database files in disk. When the execution engine wants to get a record com a page, let's say, page number 2, first we bring the page directory (that maps page numbers?) into the memory (buffer pool). Then, knowing what page it is, we get page 2 into the buffer pool. When this happens, the buffer pool gives the execution engine a pointer to the page number 2. So the execution engine interprets what's inside the page 2. 

The DBMS could use mmap to manage all of this: stores the contents of a file into the address space of a program. So the OS would be responsible for moving file pages in and out of memory, so the DBMS doesn't need to worry about it.

But there are a lot of problems with this strategy:
- OS can flush dirty pages at any time. (transaction safety)
- DBMS doesnt know which pages are in memory (because the OS is managing it). The OS will stall a thread on page fault.
- Difficult to validate pages. Any access can cause a SIGBUS that the DBMS must handle

**file storage**

the storage manager is responsible for maintaning a database's files. Some do their own scheduling for reads and writes to improve spatial and temporal locality of pages.

it organizes the files as a collection of pages.
- tracks data read/written to pages
- tracks the available space.


**page layout**

a page is a fixed-size block of data
- it can contain tuples, meta-data, indexes, log records...
- most system do not mix page types
- some systems require a page to be self-contained.

each page is given a unique identifier
- the dbms uses an indirection layer to map page ids to physical locations.

there are three different notions of "page3s" in a dbms:
- hardware page (usually 4kb)
- os page (usually 4kb, x64 2mb/1gb)
- database page (512b-32kb)

**tuple layout**
