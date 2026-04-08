function removeElement(nums: number[], val: number): number {
  let i = 0;
  let k = 0;

  const n = nums.length;

  while (i < n) {
    if (nums[i] === val) {
      let j = i + 1;
      while (j < n) {
        if (nums[j] !== val) {
          break;
        } else {
          j++;
        }
      }
      if (j < n) {
        // replace nums[i] with nums[j]
        let temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
        k++;
      }
      if (j >= n) {
        return k;
      }
      i++;
    } else {
      i++;
      k++;
    }
  }
  return k;
}

//  Optimal solution

var removeElement2 = function (nums: number[], val: number) {
  let writeIndex = 0;
  for (let readIndex = 0; readIndex < nums.length; readIndex++) {
    if (nums[readIndex] !== val) {
      nums[writeIndex] = nums[readIndex];
      writeIndex++;
    }
  }
  return writeIndex;
};
