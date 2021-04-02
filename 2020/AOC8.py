def read_instruction(operations, arguments):
    ix = 0
    accumulator = 0
    execution = {i:0 for i in range(len(operations))}
    second_time = False

    while second_time == False:
        op = operations[ix]
        arg = arguments[ix]
        execution[ix] += 1
        
        if execution[ix] > 1:
            return 0, accumulator, execution

        if op == 'acc':
            accumulator += arg
            ix += 1
        elif op == 'jmp':
            ix += arg
        elif op == 'nop':
            ix += 1
        else:
            raise # unexpected value
            
        if ix >= len(operations):
            return 1, accumulator, execution

def alter_instructions(operations, arguments, execution):
    instruct = [k for k,v in execution.items() if v >= 1] # instructions that were run at least once
    changeable_ops = [ix for ix,op in enumerate(operations) if ix in instruct and op in ['nop', 'jmp']] # ops from subset that are changeable

    for ix in changeable_ops:
        altered_ops = operations[:]   
        altered_ops[ix] = 'nop' if altered_ops[ix] == 'jmp' else 'jmp'
        n, acc, _exec = read_instruction(altered_ops,arguments)
        
        if n == 1: return acc

if __name__ == "__main__":
    _input = open("aoc_8.txt").read().splitlines()
    operations = [i.split(' ')[0] for i in _input]
    arguments = [int(i.split(' ')[1]) for i in _input]
    
    print("PART 1")
    n, accumulator, execution = read_instruction(operations,arguments)
    print(accumulator)
    print("")
    print("PART 2")
    alter_instructions(operations, arguments, execution)

