#!/usr/bin/env python

from collections import defaultdict

import pybgpstream

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

    return []


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

    return []


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

    return []


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

    return {}


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
