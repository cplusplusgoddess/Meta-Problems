#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Your team is working on a git repository, with everyone committing code.

# Author: Amber Rogowicz
# At a certain point, a bug is introduced into the repo by a revision. 
# All subsequent revisions will have the same bug,
# while all revisions before that do not.

# Your task is, given a known good revision and a bad revision,
# find the revision that introduced the bug.

# Assumptions: 
#  - You can assume a predefined function `build` which can build the 
# code of a given revision, and print the output. Dummy version here
#  - The bug can be determined by a string keyword from the build output, 
# defined by the global variable `ERROR_STR`.

# Find the git revision that broke the build - i.e. outputs ERROR_STR
# between git GOOD_REV and BAD_REV
import argparse
import os
import sys
from pathlib import Path

ERROR_STR = "This is BAD"


def build(git_rev) -> str:
	return ERROR_STR + "more junk"


def repo_find(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return path

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        # Bottom case
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # cd .. 
    return repo_find(parent, required)


def find_commits() -> list:
    tree_root = repo_find()
    if not tree_root:
        return None

    from subprocess import run, PIPE, STDOUT
    result = run(["git", "rev-list", "--all"], shell=False,
                 stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
                 cwd=tree_root)

    git_rev = result.stdout
    git_rev = git_rev.decode()
    git_rev = git_rev.rstrip()

    assert result.returncode is not None
    if result.returncode != 0:
        from warnings import warn
        warn("unable to find git revision")
        return None
    rev_list = git_rev.split()
    return rev_list


def find_git_revision(rev) -> dict:
    tree_root = repo_find()

    if not tree_root:
        return None

    from subprocess import run, PIPE, STDOUT
    result = run(["git", "cat-file", "-p", rev], shell=False,
                 stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True,
                 cwd=tree_root)

    git_rev = result.stdout
    git_rev = git_rev.decode()
    git_rev = git_rev.rstrip()

    assert result.returncode is not None
    if result.returncode != 0:
        from warnings import warn
        warn("unable to find git revision")
        return None
    rev_dict = dict_from_result(git_rev)
    return rev_dict


def dict_from_result(result: str) -> dict:
    """
    :param result # a string to search for field name
    :type str
    :param field_name # a search string
    :type field_name: str
    :rtype dict # dict - list of values which follow the field_name matched
                                                         otherwise
    """
    ret_dict = {}
    items = result.split("\n")
    for item in items:
        field_list = item.split(" ")
        ret_dict[field_list[0]] = field_list[1:]
    return ret_dict


def find_first_bad_build(last_known_good) -> str:
    git_dict = {}
    curr_commit = last_known_good
    git_dict = find_git_revision(curr_commit)
    global ERROR_STR
    while git_dict is not None:
        if git_dict is None or "tree" not in git_dict:
            return None
        tree = git_dict["tree"][0]
        if build(tree).find(ERROR_STR) >= 0:
            return curr_commit
        if "parent" in git_dict:
            curr_commit = git_dict["parent"][0]
            git_dict = find_git_revision(curr_commit)
        else:
            return None
    return None


def init_get_args(argv):
    """
    input command line arguments
    param: argv: str
    :return: good: str:bad: str
    """
    argparser = argparse.ArgumentParser(prog="get_bad_rev",
                                        description="FIRST Git revision FOOBAR FINDER")
    argparser.required = True
    argparser.add_argument(
        "-g",
        "--good",
        metavar="Good Revision",
        help="Git hash revision known to produce good build",
    )

    argparser.add_argument(
        "-b",
        "--bad",
        metavar="Bad Revision",
        help="Git hash revision known to produce bad build",
    )

    return argparser.parse_args(argv)


def main(argv=sys.argv[1:]):
    """
    command line arguments expected:
     `-g GOOD_HASH_COMMIT
     `-b BAD_HASH_COMMIT
    param: argv: str
    :return: good: str:bad: str
    """
    args = init_get_args(argv)

    # Start at known good build commit and work up by parent
    # check that rev exists and that it is a good build
    # i.e. build does not return ERROR_STR

    rev_id = find_first_bad_build(args.good)
    if(rev_id):
        print(f"First bad commit rev: {rev_id}\n")
    else:
        print(f"Could not find bad commit after rev: {args.good}\n")


if __name__ == "__main__":
    main()
