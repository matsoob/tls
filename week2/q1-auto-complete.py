import collections
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TrieNode:
    children: dict
    word: str

def construct_trie(dictionary: List[str]) -> TrieNode:
    root = TrieNode({}, None)
    for word in dictionary:
        current = root
        for c in word:
            current = current.children.setdefault(c, TrieNode({}, None))
        current.word = word
    return root

def find_node(root: TrieNode, prefix: str) -> TrieNode:
    current = root
    for c in prefix:
        current = current.children.get(c)
        if current is None:
            return None
    return current

def find_node_fuzzy_ordered(root: TrieNode, prefix: str) -> List[TrieNode]:
    if len(prefix) < 1:
        return [root]
    result_nodes = []
    keys = list(root.children.keys())
    # FIXME could be nicer if we used an ordered dict
    keys.sort()
    for key in keys:
        if key == prefix[0]:
            result_nodes.extend(find_node_fuzzy_ordered(root.children.get(key), prefix[1:]))
        else:
            exact_match_child = find_node(root.children.get(key), prefix[1:])
            if exact_match_child:
                result_nodes.append(exact_match_child)
    return result_nodes


def find_first_10_ordered(nodes: List[TrieNode]) -> List[str]:
    # expects the input List to be ordered already
    # uses queue to do a DFS basically -- could also impl with recursion? 
    queue = collections.deque(nodes)
    results = []
    while queue and len(results) < 10:
        item = queue.popleft() 
        if item is None: 
            break
        if item and item.word: 
            results.append(item.word)
        keys = list(item.children.keys()) 
        # FIXME could be nicer if we used an ordered dict
        # or ASCII chars as list indeci so we don't need to sort
        # but since it's just N=26/52, I guess it's fine
        keys.sort() 
        keys.reverse()
        for key in keys:
            queue.extendleft([item.children.get(key)])
    return results

def find_first_x_ordered_recursion(nodes: List[TrieNode], x: int) -> List[str]:
    # expects the input List to be ordered already
    # same as above but implemented with recursion
    if x == 0:
        return []
    results = []
    for node in nodes:
        if node.word:
            results.append(node.word)
            if len(results) == x:
                break
        sorted_dict = dict(sorted(node.children.items()))
        found_words = find_first_x_ordered_recursion(sorted_dict.values(), x - len(results))
        results.extend(found_words)
        if len(results) >= x:
            break
    return results

def print_me(matches: List[str]):
    for match in matches:
        print(match)

def solve(dictionary: list, queries: list):
    root = construct_trie(dictionary)
    for query in queries:
        ordered_nodes_for_prefix = find_node_fuzzy_ordered(root, query)
        #matches = find_first_10_ordered(ordered_nodes_for_prefix)
        matches = find_first_x_ordered_recursion(ordered_nodes_for_prefix, 10)
        print_me(matches)

def main():
  dict_size = int(input())
  dictionary = []
  for _ in range(dict_size):
    dict_word = input()
    dictionary.append(dict_word)
  query_size = int(input())
  queries = []
  for _ in range(query_size):
    query = input()
    queries.append(query)
  solve(dictionary, queries)
  
if __name__ == "__main__":
    main()

