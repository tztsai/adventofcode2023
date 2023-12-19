from utils import *

workflows, parts = map(str.splitlines, read_input(sep='\n\n'))

def parse_workflows(workflows, entry='in'):
    """Parse the workflows into a decision tree."""
    pat = re.compile(r"[^{}]+")
    workflows = {m[0]: m[1].split(',') for m in map(pat.findall, workflows)}
    def parse_workflow(rules):
        if len(rules) == 1:
            name = rules[0]
            if name in ('A', 'R'):
                return name
            return parse_workflow(workflows[name])
        cond, name = rules[0].split(':')
        var, op, val = re.match(r"(\w+)([<>])(\d+)", cond).groups()
        this = parse_workflow([name])
        that = parse_workflow(rules[1:])
        if op == '<':  # var < val; var >= val
            return [var, int(val), this, that]
        else:  # var > val (var >= val+1); var <= val (var < val+1)
            return [var, int(val) + 1, that, this]
    return parse_workflow(workflows[entry])

def parse_part(part):
    return eval(f"dict({part[1:-1]})")

decision_tree = parse_workflows(workflows)
parts = list(map(parse_part, parts))

def check(part, tree=decision_tree):
    if tree == 'A':
        return sum(part.values())
    if tree == 'R':
        return 0
    var, val, left, right = tree
    if part[var] < val:
        return check(part, left)
    else:
        return check(part, right)

print(sum(map(check, parts)))

def check_intervals(intervals, tree=decision_tree):
    if tree == 'A':
        # print(intervals)
        return math.prod(hi - lo + 1 for lo, hi in intervals.values())
    if tree == 'R':
        return 0
    var, val, *branches = tree
    splits = split_intervals(intervals, var, val)
    return sum(check_intervals(s, t) for s, t in zip(splits, branches) if s)

def split_intervals(intervals, var, val):
    lo, hi = intervals[var]
    splits = [[lo, val-1], [val, hi]]
    return [l <= h and {**intervals, var: [l, h]} for l, h in splits]

print(check_intervals({var: [1, 4000] for var in 'xmas'}))