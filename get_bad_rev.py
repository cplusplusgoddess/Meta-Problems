#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Amber Rogowicz
# Your team is working on a git repository, with everyone committing code.
# At a certain point, a bug is introduced into the repo by a revision.
# All subsequent revisions will have the same bug,
# while all revisions before that do not.
#
# Your task is, given a known good revision and a bad revision,
# find the revision that introduced the bug.
#
# Assumptions:
#  - You can assume a predefined function `build` which can build the
# code of a given revision, and print the output. Dummy version here
#  - The bug can be determined by a string keyword from the build output,
# defined by the global variable `ERROR_STR`.
#
# Find the git revision that broke the build - i.e. outputs ERROR_STR
# between git GOOD_REV and BAD_REV
import argparse
import os
import sys
from pathlib import Path

ERROR_STR = "This is BAD"
BISECT_STR = "first bad commit"


# stub function
def build(git_rev) -> str:
    return ERROR_STR


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


def git_bisect(good, bad, start=True) -> str:
    tree_root = repo_find()

    if not tree_root:
        return None

    from subprocess import run, PIPE, STDOUT

    if start:
        result = run(
            ["git", "bisect", "start", bad, good],
            shell=False,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
            close_fds=True,
            cwd=tree_root,
        )

    else:
        result = run(
            ["git", "bisect", "bad", bad],
            shell=False,
            stdin=PIPE,
            stdout=PIPE,
            stderr=STDOUT,
            close_fds=True,
            cwd=tree_root,
        )
    git_rev = result.stdout
    git_rev = git_rev.decode()
    git_rev = git_rev.rstrip()
    return git_rev


def find_first_good_build(first_known_good, first_known_bad) -> str:
    global ERROR_STR
    res = git_bisect(first_known_good, first_known_bad, True)

    while 1:
        if res.find(BISECT_STR) >= 0:
            return res
        rev = res.split("[")
        if len(rev) > 1:
            rev = rev[1].split("]")
            if build(rev[0]).find(ERROR_STR) >= 0:
                res = git_bisect(None, rev[0], False)
                continue
            else:
                break

    return res


def init_get_args(argv):
    """
    input command line arguments
    param: argv: str
    :return: good: str:bad: str
    """
    argparser = argparse.ArgumentParser(
        prog="get_bad_rev", description="FIRST Git revision FOOBAR FINDER"
    )

    argparser.add_argument(
        "-g",
        "--good",
        metavar="Good rev short or long hash",
        help="Git hash revision known to produce good build",
        required=True,
    )
    argparser.add_argument(
        "-b",
        "--bad",
        metavar="Bad rev short or long hash",
        help="Git hash revision known to produce bad build",
        required=True,
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

    # Start at known bad build commit and work up by parent
    # until a good found i.e. build does not return ERROR_STR

    if args.bad and args.good:
        res = find_first_good_build(args.good, args.bad)
        print(f"{res} \n")


if __name__ == "__main__":
    main()
