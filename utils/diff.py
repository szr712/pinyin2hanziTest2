import difflib


def diff(a, b):
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b).get_opcodes():
        if tag != 'equal':
            yield i1,i2,j1,j2,a[i1:i2], b[j1:j2]
