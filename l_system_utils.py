import hashlib
from os.path import join, isdir, isfile, dirname
from os import makedirs
from tempfile import gettempdir

cachedir = join(gettempdir(), "lsd-cache")
print("cachedir: ", cachedir)

def serialize_l_system(string, rules):
    items = [(k,v) for k,v in rules.items()]
    items.sort(key=lambda k:k[0])
    return string + ";" + ";".join("{}:{}".format(k,v) for k,v in items)

def expand_string(string, rules):
    parts = []
    for x in string:
        try:
            parts.append(rules[x])
        except KeyError:
            parts.append(x)
    return "".join(parts)

def cached_expand_string(string, rules):

    # don't cache minimal strings to decrase I/O time
    if not len(string) > 5000:
        return expand_string(string, rules)


    if not isdir(cachedir):
        makedirs(cachedir)

    m = hashlib.sha256()

    serialized_system = serialize_l_system(string, rules)
    m.update(serialized_system.encode('utf-8'))
    cachefile = join(cachedir, m.hexdigest())

    if isfile(cachefile):
        with open(cachefile) as f:
            return f.read()
    else:
        value = expand_string(string, rules)
        with open(cachefile, "w") as f:
            f.write(value)
        return value

class PlaceHolder(object):
    "So that we can track what is a placeholder"
    def __init__(self, value):
        self.value = value
