from utils import *

lines = read_lines()
nums = [list(filter(str.isdigit, line)) for line in lines]
print(sum(int(ns[0] + ns[-1]) for ns in nums))

numbers = "one, two, three, four, five, six, seven, eight, nine".split(', ')
pattern = f"(?=([0-9]|{'|'.join(numbers)}))"
nums = [re.findall(pattern, line) for line in lines]
trans = lambda s: {s: str(i+1) for i, s in enumerate(numbers)}.get(s, s)
print(sum(int(trans(ns[0]) + trans(ns[-1])) for ns in nums))
