def push(item, stack, length):
    if len(stack) == length:
        stack.append(item)
        stack.pop(0)
    else:
        stack.append(item)
    

def pop(stack):
    if len(stack) != 0:
        item = stack.pop(0)
    else:
        item = None
    return item


if __name__ == '__main__':
    CACHE_LENGTH = 3
    stack = []
    items = [1,2,3,4,5]
    for item in items:
        push(item, stack, CACHE_LENGTH)
        print(stack)
    for _ in range(len(items)):
        popped_item = pop(stack)
        print(stack)
        
