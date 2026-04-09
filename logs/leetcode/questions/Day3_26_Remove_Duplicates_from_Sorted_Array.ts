function removeDuplicates(nums: number[]): number {
  let writeHead = 1;
  const n = nums.length;
  for (let readHead = 1; readHead < n; readHead++) {
    if (nums[readHead] > nums[readHead - 1]) {
      nums[writeHead] = nums[readHead];
      writeHead++;
    }
  }
  return writeHead;
}
