# list_func = [3, 2, 1]
list_func = [2, 1]

node_list = ['in', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'out']

result = []
stack = []
def f(node, func):
    start = node_list.index(node) + 1
    return node_list[start: start+func]

def dfs(in_node, i):
    stack.append(in_node)
    if i == len(list_func):
        result.append(stack.copy())
        return

    a_list = f(in_node, list_func[i])
    for node in a_list:
        dfs(node, i+1)
        stack.pop()

if __name__ == '__main__':
    dfs(node_list[0], 0)
    print(result)
