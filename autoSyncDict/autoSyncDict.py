import os
import pickle
import cachetools
import atexit
import dataset


class AutoSyncDict:

    def __init__(self, name=".autodictdata.save", size=0, strategy="lru", json_save=False, clean_start=False):

        atexit.register(self.save_data)
        self._name = name
        self._size = size
        self._strategy = strategy
        self._json_save = json_save
        if os.path.exists(name) and not clean_start:
            with open(name, "rb") as f:
                self._dict = pickle.load(f)
        else:
            self.reset()

    def reset(self):
        if self._size == 0:
            self._dict = {}
        elif self._strategy == "lru":
            self._dict = cachetools.LRUCache(self._size)
        elif self._strategy == "lfu":
            self._dict = cachetools.LFUCache(self._size)

    def save_data(self):
        with open(self._name, "wb") as f:
            pickle.dump(self._dict, f)

    def __del__(self):
        pass

    def __setitem__(self, key, item):
        self._dict[key] = item

    def __getitem__(self, key):
        return self._dict[key]

    def __repr__(self):
        return repr(self._dict)

    def __len__(self):
        return len(self._dict)

    def __delitem__(self, key):
        del self._dict[key]

    def clear(self):
        return self._dict.clear()

    def copy(self):
        return self._dict.copy()

    def has_key(self, k):
        return k in self._dict

    def update(self, *args, **kwargs):
        return self._dict.update(*args, **kwargs)

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def items(self):
        return self._dict.items()

    def pop(self, *args):
        return self._dict.pop(*args)

    def __cmp__(self, dict_):
        return self.__cmp__(self._dict, dict_)

    def __contains__(self, item):
        return item in self._dict

    def __iter__(self):
        return iter(self._dict)


class AutoDbDict:

    def __init__(self, name=".autodictdata.db", clean_start=False):
        self._name = name
        if clean_start and os.path.exists(name):
            os.remove(name)
        self._db = dataset.connect("sqlite:///" + name)

    def reset(self):
        pass

    def __del__(self):
        pass

    def __setitem__(self, key, item):
        table = self._db['dict']
        table.upsert(dict(key=key, item=item), ["key"])

    def __getitem__(self, key):
        table = self._db['dict']
        data = table.find_one(key=key)
        return data["item"]

    def __repr__(self):
        table = self._db['dict']
        str_repr = "{\n"
        for i in table:
            str_repr += "  " + i["key"] + ":" + str(i["item"]) + ",\n"
        str_repr += "}"
        return str_repr

    def __len__(self):
        table = self._db['dict']
        return table.count()

    def __delitem__(self, key):
        table = self._db['dict']
        table.delete(key=key)

    def clear(self):
        table = self._db['dict']
        table.drop()

    def has_key(self, k):
        table = self._db['dict']
        count = table.count(key=k)
        return count > 0

    def keys(self):
        table = self._db['dict']
        return [i["key"] for i in table]

    def values(self):
        table = self._db['dict']
        return [i["item"] for i in table]

    def items(self):
        return self.values()

    def pop(self, *args):
        table = self._db['dict']
        output = []
        for key in args:
            value = table.find_one(key=key)
            output.append(value["item"])
            table.delete(key=key)
        return output

    def __eq__(self, dict_):
        if len(dict_) != len(self):
            return False
        try:
            keys_a = sorted(self.keys())
            keys_b = sorted(dict_.keys())
            if keys_a != keys_b:
                return False
            items_a = sorted(self.values())
            items_b = sorted(dict_.values())
            if items_a != items_b:
                return False
        except Exception as e:
            print(e)
            return False
        return True

    def __contains__(self, item):
        return self.has_key(item)

    def __iter__(self):
        table = self._db['dict']
        for i in table:
            yield i["item"]


if __name__ == '__main__':
    a = AutoDbDict(clean_start=True)
    a["a"] = 1
    a["b"] = "hello"

    print(a)
