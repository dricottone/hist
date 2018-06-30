#!/usr/bin/env python3

def _bin_iter(avg, bin_width, num_bins):
    bin_ = int(avg - (bin_width * (num_bins // 2)))
    a = 0
    while a < num_bins:
        yield bin_
        bin_ = bin_ + bin_width
        a = a + 1

def hist(args, bin_num=1):
    """
    Creates a formatted unicode histogram. Requires an iterable of numeric
    values. Optionally set number of bins. By default, creates a single bin
    histogram.
    """

    avg = sum(args)/len(args)
    bin_num = int(bin_num)

    # a single bin
    if bin_num == 1:
        hist_height = len(args)
        print(u'\u2502' + ' {:>3}'.format(hist_height))
        hist_height = hist_height - 1
        while hist_height > 0:
            print(u'\u2502' + '   ' + u'\u2588')
            hist_height = hist_height - 1
        print('{:{}<5}\n'.format(u'\u253c', u'\u2500')
              + '  all\n'
              + '  Avg. = {:.2f}'.format(avg))
        return
        
    # histogram design
    avg = sum(args)/len(args)

    ordered = sorted(args)
    range_ = ordered[-1] - ordered[0]
    bin_width = range_ // bin_num
    if bin_width == 0:
        bin_width = 1



    # collect histogram data
    bin_labels = []
    bin_freq = []
    outliers = []
    for bin_ in _bin_iter(avg, bin_width, bin_num):
        bin_labels.append(str(bin_))
        
        freq = 0
        x = 0
        while x < len(ordered):
            if (ordered[x] < bin_):
                x = x + 1
            elif (ordered[x] >= bin_) and (ordered[x] < bin_ + bin_width):
                ordered.pop(x)
                freq = freq + 1
            else:
                break
        bin_freq.append(freq)

    for unbinned in ordered:
        outliers.append(unbinned)

    # draw histogram
    hist_width = (bin_num * 4) + 1
    hist_height = max(bin_freq)

    y_val = max(bin_freq)
    while y_val > 0:
        row = u'\u2502'
        for x_val in range(bin_num):
            if bin_freq[x_val] == y_val:
                cell_val = str(y_val)
            elif bin_freq[x_val] > y_val:
                cell_val = u'\u2588'
            else:
                cell_val = ''
            row = row + ' {:>3}'.format(cell_val)
        print(row)
        y_val = y_val - 1

    # draw histogram labels
    hist_width = (bin_num * 4) + 1
    horizontal_line = '{corner:{line}<{length}}'.format(corner = u'\u253c',
                                                        line = u'\u2500',
                                                        length = hist_width)
    print(horizontal_line)
    
    labels = ' '
    for label in bin_labels:
        labels = labels + ' {:>3}'.format(label)
    print(labels)

    # draw histogram details as applicable
    if hist_width > 15:
        details_width = hist_width
    else:
        details_width = 15
        
    print('{text:>{length}} {average:<.2f}'.format(text = 'Average =',
                                                   length = details_width - 6,
                                                   average = avg))

    if outliers != []:
        string = ', '.join(str(outlier) for outlier in outliers)
        string = 'Excluded outliers: ' + string
        print('{text:>{length}}'.format(text = string, length = details_width))

    return

if __name__ == '__main__':
    import random
    i = 0
    lst = []
    while i < 100:
        lst.append(random.randrange(1,101))
        i = i + 1
    hist(lst, 11)
