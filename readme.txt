syntax:
    unicode_hist.hist(list_object [, number_bins])

     *  list_object can be any list-like object (lists, tuples, etc.)
     *  number_bins can be any numeric type (default is 1)


example output:

>>> unicode_hist.test()
│                  17                        
│                   █                        
│                   █                        
│                   █                        
│                   █                        
│                   █                        
│                   █                        
│          10  10   █  10          10        
│           █   █   █   █           █        
│           █   █   █   █           █       8
│           █   █   █   █   7       █   7   █
│   6   6   █   █   █   █   █       █   █   █
│   █   █   █   █   █   █   █       █   █   █
│   █   █   █   █   █   █   █   4   █   █   █
│   █   █   █   █   █   █   █   █   █   █   █
│   █   █   █   █   █   █   █   █   █   █   █
│   █   █   █   █   █   █   █   █   █   █   █
┼────────────────────────────────────────────
    8  16  24  32  40  48  56  64  72  80  88
                              Average = 48.63
             Excluded outliers: 1, 2, 2, 3, 6
