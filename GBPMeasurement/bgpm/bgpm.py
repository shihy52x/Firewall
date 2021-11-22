#!/usr/bin/env python

from collections import defaultdict
import time
import glob, os

import pybgpstream
from pybgpstream import BGPStream, BGPRecord, BGPElem
import matplotlib.pyplot as plt
import collections

"""Code file for CS 6250 BGPM Project

Edit this file according to docstrings. 
Do not change the existing function name or arguments in any way.

"""

# Task 1 Part A.
def calculateUniqueIPAddresses(cache_files):
    """Retrieve the number of unique IP prefixes from input BGP data.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list containing the number of unique IP prefixes for each input cache file.
          For example: [2, 5]
    """
    y = []
    cache_files = sorted(cache_files)
    for file in cache_files:
        stream = BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", file)
        records = set()
        for elem in stream:
            records.add(elem._maybe_field("prefix"))
        y.append(len(records))
    return y


# Task 1 Part B.
def calculateUniqueAses(cache_files):
    """Retrieve the number of unique ASes from input BGP data.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list containing the number of the number of unique AS for each input file.
          For example: [2, 5]
    """
    y = []
    cache_files = sorted(cache_files)
    for file in cache_files:
        stream = BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", file)
        records = set()
        for elem in stream:
            records.add(elem.peer_asn)
        y.append(len(records))
    return y



# Task 1 Part C.
def examinePrefixes(cache_files):
    """
    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files_final/1357027200.120.cache", "/rib_files_final/1483257600.120.cache"]

    Returns:
        A list of the top 10 origin ASes according to percentage increase of the advertised prefixes.
        See assignment description for details.
    """
    cache_files = sorted(cache_files)
    first_file = cache_files[0]
    last_file = cache_files[-1]
    dict_first = calAseDict(first_file)
    dict_last = calAseDict(last_file)
    dict_percentage = dict()
    for key in dict_first:
        if key in dict_last:
            a = len(dict_first[key])
            b = len(dict_last[key])
            dict_percentage[key] = float(b)/float(a)

    dict_sort =  {k:v for k, v in sorted(dict_percentage.items(), key=lambda item: -item[1])}
    return [i for i in dict_sort.keys()]

def calAseDict(file):
    stream = BGPStream(data_interface="singlefile")
    stream.set_data_interface_option("singlefile", "rib-file", file)
    records = dict()
    for elem in stream:
        asn = elem.peer_asn
        prefix = elem._maybe_field("prefix")
        if asn in records:
            records[asn].add(prefix)
        else:
            records[asn] = set()
            records[asn].add(prefix)
    return records


# Task 2 Part A.
def calculateShortestPath(cache_files):
    """Compute the shortest AS path length for every origin AS from input BGP data.

    Retrieves the shortest AS path length for every origin AS for every input cache file.
    Your code should return a dictionary where every key is the AS string and every value associated with the key is
    a list of shortest path lengths for that AS. See project description for details on how to do this.

    Note: For any AS that is not present in every input file, fill the corresponding entry in its list with a zero.
    Every value in the dictionary should have the same length.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/rib_files/ris.rrc06.ribs.1357027200.120.cache", "/rib_files/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where every key is the AS and every value associated with the key is
          a list of shortest path lengths for that AS, for every input file, sorted by date (earliest first).
          For example: {"455": [4, 0, 3], "533": [0, 1, 2]}
          corresponds to the AS "455" with shortest path lengths 4, 0 and 3 and the AS "533" with shortest paths 0, 1 and 2.
    """
    cache_files = sorted(cache_files)
    res_global = []
    for file in cache_files:
        stream = BGPStream(data_interface="singlefile")
        stream.set_data_interface_option("singlefile", "rib-file", file)
        res_local = dict()
        i = 0
        for elem in stream:
            i += 1
            #if i > 10000:
                #break
            path_string = elem._maybe_field("as-path")
            as_list = path_string.split(" ")
            as_set = set(as_list)
            path_length = len(as_set)
            origin_as = as_list[-1]
            if origin_as not in res_local:
                res_local[origin_as] = path_length
            else:
                res_local[origin_as] = min(res_local[origin_as], path_length)
        res_global.append(res_local)
    all_keys = set()
    for res_local in res_global:
        for key in res_local.keys():
            all_keys.add(key)
    res = dict()

    for key in all_keys:
        for res_local in res_global:
            if key not in res_local:
                value = 0
            else:
                value = res_local[key]

            if key not in res:
                res[key] = [value]
            else:
                res[key].append(value)
    return res


# Task 3 Part A.
def calculateRTBHDurations(cache_files):
    """Identify blackholing events and compute the duration of all RTBH events from input BGP data.

    Identify events where the IPV4 prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.
    See project description for details on how to do this.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/update_files_blackholing/ris.rrc06.ribs.1357027200.120.cache", "/update_files_blackholing/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a
            prefix and each value equal to a list of explicit RTBH event durations.
            For example: {"455": {"123": [4, 1, 3]}}
            The above example corresponds to the peerIP "455", the prefix "123" and event durations of 4, 1 and 3.
    """
    cache_files = sorted(cache_files)
    for file in cache_files:
        stream = BGPStream(data_interface="singlefile")
        # stream.add_filter("ipversion", "4")
        stream.set_data_interface_option("singlefile", "upd-file", file)
        res_local = dict()
        i = 0
        for elem in stream:
            i += 1
            #if i > 10000:
            #break
            import pdb
            print(elem)
            print(elem.fields)
            path_string = elem._maybe_field("as-path")
            as_list = path_string.split(" ")
            as_set = set(as_list)
            path_length = len(as_set)
            origin_as = as_list[-1]
    return {}


# Task 4.
def calculateAWDurations(cache_files):
    """Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input data.

    Identify explicit AW events.
    See project description for details on how to do this.

    Args:
        cache_files: A list of absolute file paths.
          File paths may not be in order but will end with a timestamp that can be used for sorting.
          For example: ["/update_files/ris.rrc06.ribs.1357027200.120.cache", "/update_files/ris.rrc06.ribs.1483257600.120.cache]

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a
            prefix and each value equal to a list of explicit AW event durations.
            For example: {"455": {"123": [4, 1, 3]}}
            The above example corresponds to the peerIP "455", the prefix "123" and event durations of 4, 1 and 3.
    """

    return {}


cache_file = "/home/mininet/Projects/git/bgpmeasurement/bgpm/rib_files/ris.rrc06.ribs.1357027200.120.cache"
cache_file_path = "/home/mininet/Projects/git/bgpmeasurement/bgpm/rib_files"

files = []
for file in os.listdir(cache_file_path):
    files.append(os.path.join(cache_file_path, file))
files = sorted(files)
print(files)

x = []
for file in files:
    time_string = file.split('.')[3]
    x.append(time.gmtime(int(time_string)).tm_year)
#y = calculateUniqueIPAddresses(files)
#plt.plot(x, y)
#plt.savefig(fname = "uniq_ip.png")

#y = calculateUniqueAses(files)
#plt.plot(x, y)
#plt.savefig(fname = "uniq_ase.png")

#examinePrefixes(files)
import pdb

# res = calculateShortestPath(files)
# snapshots =[]
# for i in range(len(x)):
#     snapshots.append(dict())
#
# for key, val in res.items():
#     for i in range(len(x)):
#         if val[i] in snapshots[i]:
#             snapshots[i][val[i]] += 1
#         else:
#             snapshots[i][val[i]] = 1
#
#
# f, axs = plt.subplots(2,2,figsize=(8,16))
# n = len(x)
# for i in range(n):
#     snapshot = snapshots[i]
#     x_cul = []
#     y_cul = []
#     cul_sum = 0
#     for key in sorted(snapshot.keys()):
#         if key != 0:
#             val = snapshot[key]
#             x_cul.append(key)
#             cul_sum += val
#             y_cul.append(cul_sum)
#
#     y_cul = [float(k)/float(cul_sum) for k in y_cul]
#     ax = plt.subplot(len(x), 1, i + 1)
#     ax.set_title(str(x[i]))
#     ax.plot(x_cul, y_cul)
# plt.savefig("ecdf.png")

cache_file_path = "/home/mininet/Projects/git/bgpmeasurement/bgpm/update_files_blackholing"

files = []
for file in os.listdir(cache_file_path):
    files.append(os.path.join(cache_file_path, file))
files = sorted(files)
print(files)

x = []
import pdb
pdb.set_trace()
for file in files:
    time_string = file.split('.')[3]
    print(time.gmtime(int(time_string)))
    x.append(time.gmtime(int(time_string)).tm_year)
calculateRTBHDurations(files)

