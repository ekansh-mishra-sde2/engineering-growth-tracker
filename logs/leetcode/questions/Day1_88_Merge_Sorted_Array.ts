/**
 Do not return anything, modify nums1 in-place instead.
 */
/**
 Do not return anything, modify nums1 in-place instead.
 */
function merge(nums1: number[], m: number, nums2: number[], n: number): void {
  if (n === 0) {
    nums1.slice(0, m);
    return;
  }
  if (m === 0) {
    // nums1 = nums2;
    nums1.splice(0, nums1.length, ...nums2);
    return;
  }

  let ans: number[] = [];
  let i = 0;
  let j = 0;

  while (i < m && j < n) {
    if (nums1[i] <= nums2[j]) {
      ans.push(nums1[i]);
      i++;
    } else {
      ans.push(nums2[j]);
      j++;
    }
  }

  if (i === m) {
    ans.push(...nums2.slice(j, n));
  } else {
    ans.push(...nums1.slice(i, m));
  }

  nums1.splice(0, nums1.length, ...ans);
}

//
// optimal solution
function mergeOptimal(
  nums1: number[],
  m: number,
  nums2: number[],
  n: number,
): void {
  let i = m - 1; // last valid element in nums1
  let j = n - 1; // last element in nums2
  let k = m + n - 1; // last position in nums1

  while (j >= 0) {
    if (i >= 0 && nums1[i] > nums2[j]) {
      nums1[k] = nums1[i];
      i--;
    } else {
      nums1[k] = nums2[j];
      j--;
    }
    k--;
  }
}
