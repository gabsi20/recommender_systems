#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def print_progressbar(iteration, total, current_item):
    fill = '█'
    length = 30
    max_length = 50
    percent = ("{0:.2f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    progress_bar = '\r|' + bar + '| ' + percent + ' ' + str(iteration) + ' ' + str(current_item)
    progress_bar = progress_bar[:max_length]
    progress_bar = progress_bar + ' ' * (max_length - len(progress_bar))
    sys.stdout.write(progress_bar)
    sys.stdout.flush()
    if iteration == total: 
        print()