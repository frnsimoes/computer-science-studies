A varint, or variable-length integer, is a method of encoding integers using a variable number of bytes. It's commonly used in computer science and data serialization to save space when storing integers that may have a wide range of values. 

A varint has a prefix bytes, to indicate when if after that byte there are following bytes that the calculation must lavarage. 

Let's look at the example of the decimal 300:
- Binary representation: `100101100`
- Next, divide into chunks: 1. start from the right and group the bits into chunks of 7 bits each. 2. add leading zeros if necessary to make each chink exactly 7 bits long. 

```
Decimal: 300 = `100101100`
# Reverse and divide into chunk, grouping in little-endian order
Chunk 1 (first byte): 10000100
Chunk 2 (last byte): 00010100
```
