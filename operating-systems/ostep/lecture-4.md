Back to virtual memory

Problems with segmentation:
- Support sparseness, but limited.
- External fragmentation. Have to rejeitar or compact memory. Reason: if we have a lot of small segments, we have to compact them to make room for a big segment. This is a problem.

OS responsabilities regarding to memory: two levels of memory management:
- inside virtual addr space

**Paging**

Potential problems with paging: it may be too slow. It may be a memory hog.

Paging: Divide two things: virtual addr spaces and physical memory. Divide them into fixed-size units called pages. Typically 4kb

There is a lot of information per process. Generally stored in memory. Previously we had a base/bounds pair that was just sitting in the CPU, and it would do all the translation to us. Now we have this huge amount of information that is going to be stored in memory. As a result, we have to go to memory to get the translation, and it may be slow.

Example of a very small 'toy' virtual addr space:

4 pages with 8 bytes each. Virtual addr space size: 32 bytes

What is a virtual address and its components?
A virtual address consists of: a virtual page number (VPN) and an offset. This is translated into a physical frame number (PFN). THe offset is not translated at all. 

How does translation occurr? 

The hardware needs to know the location of the page table; page size, the structure pf the page entry.

There is a per CPU register that holds address of the page table of the currently runnign process. It's called page table base register (PTBR)
