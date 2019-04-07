# AutoSyncDict

Python library to have easy dict like persistency for small lived scripts

## Note

Created and tested against `Python3` only

## How to install

The easiest way to install this library is to run this command

`pip install git+https://github.com/Lightjohn/AutoSyncDict.git`

## How to use

```python
In [1]: from autoSyncDict import AutoSyncDict                                                                                               

In [2]: my_dict = AutoSyncDict()                                                                                                                  

In [3]: my_dict["a"] = 5555 
```

Then you can quit the session and open a new one

```python
In [1]: from autoSyncDict import AutoSyncDict                                                                                               

In [2]: my_dict = AutoSyncDict()                                                                                                                  

In [3]: my_dict                                                                                                                                   
Out[3]: {'a': 5555}

```

There is two kind of dict:

* `AutoSyncDict`: will use **pickle** at the beginning and end of the object 
life to load and save data

* `AutoDbDict`: will use **sqlite** to store the data

## Parameters
 
### AutoSyncDict
 
 * **name**: name of the pickle save file: `.autodictdata.save` by default
 * **size**: size of the dict: 0 by default, normal python `dict`
   * if size is > 0, `cachetools.LRUCache` is used by default
 * **strategy** is size is > 0, options are `lru` and `lfu` for `cachetools.LFUCache`
 * **clean_start** will ignore any existing file: `False` by default
 * **json_save** not implemented yet
 
### AutoDbDict

* **name** name of the sqlite db file: `.autodictdata.db` by default
* **clean_start** will ignore any existing db: `False` by default

## Notes

For any issue please create issue [here](https://github.com/Lightjohn/AutoSyncDict/issues)