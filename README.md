Project Name: Bitmap Index Compression Tool

Description: Creates bitmaps of the list (animal, age, adopted). Provides functionality for creating and compressing bitmap indices. The main functions available are create_index and compress_index.

To use 
```
import compression as comp
```

Parameters

- bitmap_index - The input file used in the compression
- output_path - The path to a directory where the compressed version will be written.
- compression_method - A string specifying the bitmap compression method (only WAH works currently)
- word_size -  An integer specifying the word size to be used

```
comp.compression_index(bitmap_index, output_path, compression_method, word_size)
```

Parameters
- input_path - The file used to create the bitmap index
- output_path - The path to a directory where the output bitmap file will be written
- sorted - A boolean specifying whether sorted before input
```
comp.create_index(input_file, output_path, sorted)
```

example:
```
compress_index(bitmap_index, ./, WAH, 16)
./bitmap_index_WAH_16

compress_index(bitmap_index, output_path, BBC, 8)
./bitmap_index_BBC_8
```
