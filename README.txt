/*
[Problem]
  Please write a function that merges two sorted "int" arrays.
  The resulting array must be sorted.
  - Please define a function properly.

  Example:
    merge([1, 4, 5, 8], [3, 7]) -> [1, 3, 4, 5, 7, 8]
*/

int main() {
  int a[] = {1, 4, 5, 8};
  int b[] = {3, 7};
  return 0;
}
# Your team is working on a git repository, with everyone committing code.

# At a certain point, a bug is introduced into the repo by a revision. 
# All subsequent revisions will have the same bug,
# while all revisions before that do not.

# Your task is, given a known good revision and a bad revision,
# find the revision that introduced the bug.

# Assumptions: 
#  - You can assume a predefined function `build` which can build the 
# code of a given revision, and print the output.
#  - The bug can be determined by a string keyword from the build output, 
# defined by the global variable `ERROR_STR`.



