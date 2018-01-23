import sys

def print_progressbar(iteration, total, current_item):
    fill = 'I'
    length = 30
    max_length = 75
    percent = ("{0:.2f}").format(100 * (iteration / float(max((total-1),1))))
    filled_length = int(length * iteration // max((total - 1),1))
    bar = fill * filled_length + '-' * (length - filled_length)
    progress_bar = bar + '| ' + percent + ' ' + str(iteration) + ' ' + str(current_item)
    progress_bar = progress_bar[:max_length]
    progress_bar = progress_bar + ' ' * (max_length - len(progress_bar))
    sys.stdout.flush()
    sys.stdout.write('\r' + progress_bar)

    if iteration == (total-1):
        sys.stdout.write('\n')
        sys.stdout.flush()