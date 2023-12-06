import __main__

def read_lines(filename=None, sep='\n'):
    if filename is None:
        filename = __main__.__file__.rsplit('.', 1)[0] + '.txt'
    with open(filename, 'r') as f:
        return f.read().strip().split(sep)
