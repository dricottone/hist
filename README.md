# hist

Create a histogram on the terminal.

## Usage

```
$ ps -eo pmem --sort=-pmem --no-headers | head -n 20 | python -m hist --bins=20 --positive
│ 10                                                         
│  █                                                         
│  █                                                         
│  █                                                         
│  █                                                         
│  █  5                                                      
│  █  █                                                      
│  █  █                                                      
│  █  █  2        2                                          
│  █  █  █        █                          1               
┼────────────────────────────────────────────────────────────
   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
Avg. = 2.25
```

