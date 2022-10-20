#include <iostream>
using namespace std;
/*
[Author] 
  Amber Rogowicz 		Oct. 18, 2022
[Problem]
  Please write a function that merges two sorted "int" arrays.
  The resulting array must be sorted.
  - Please define a function properly.

  Example:
    merge([1, 4, 5, 8], [3, 7]) -> [1, 3, 4, 5, 7, 8]
  Inputs: 
	int a[]   - sorted array of contiguous integers
	int len_a - length of a
	int b[]   - sorted array of contiguous integers
	int len_b - length of b
  Outputs:
	int *     - sorted allocated array of integers length = len_a + len_b

  Note: The return array allows duplicates
*/
int*  merge(int* a, int len_a, int* b, int len_b){
	int len_ret;
	if((len_ret = len_a + len_b) <= 0)
		return(nullptr);
	int* ret = (int*)malloc(len_ret*sizeof(int));
	int i, aptr, bptr;
	i =  aptr = bptr = 0;
	while((aptr < len_a) && (bptr < len_b)){
		ret[i++] = (a[aptr] < b[bptr])?a[aptr++]:b[bptr++];
	}
	if(aptr != len_a){
		for( ;aptr < len_a; aptr++)
			ret[i++] = a[aptr];
	} else {
		for( ;bptr < len_b; bptr++)
			ret[i++] = b[bptr];
	}
	return(ret);
} 


int main() {
  int a[] = {1, 4, 5, 8};
  int b[] = {3, 7};

  int *ret = merge(a, 4, b, 2);
  cout << "merged array: [";
  for(int i = 0; i < 6; i++)
     cout << ret[i] << ", ";
  cout << "]\n";
  int c[] = {1, 4, 5, 8};
  int d[] = {3, 4, 9};
  free(ret);
  ret = merge(c, 4, d, 3);
  cout << "merged array: [";
  for(int i = 0; i < 7; i++)
     cout << ret[i] << ", ";
  cout << "]\n";

  return 0;
}
