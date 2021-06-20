from dataclasses import dataclass, field
from typing import Dict, List, ForwardRef
import collections

@dataclass
class Node:
    titles: List[str] = field(default_factory=list)
    children: Dict[str, ForwardRef("Node")] = field(default_factory=dict)

def extract_keywords(query: str):
    words = [word.lower() for word in query.split(' ')]
    words.sort()
    return words

def build_index(pages: List[str]) -> Node:
    root = Node()
    for page in pages:
        words = extract_keywords(page)
        flesh_out_subtree(root, words, page)
    return root

def flesh_out_subtree(sub_root: Node, words: List[str], title: str):
    start_index = 0
    if len(words) == 0:
        sub_root.titles.append(title)
        return
    for i in range(len(words)):
        current_word = words[i]
        next_node = sub_root.children.setdefault(current_word, Node())
        flesh_out_subtree(next_node, words[i+1:], title)

def find_node(root: Node, keywords: List[str]) -> Node:
    current = root
    for keyword in keywords:
        current = current.children.get(keyword)
        if not current:
            break
    return current

def get_candidates(node: Node, limit=10) -> List[str]:
    results = []
    if not node:
        return results
    queue = collections.deque([node])
    while queue and len(results) < limit:
        item = queue.popleft()
        results.extend(item.titles)
        queue.extend(item.children.values())
    return results[:limit]

# No this doesn't work bc the page title words are sorted
# when you translate back to trie-traversal -> title, the order 
# will be mangled. 
# def get_candidates_in_order(node: Node, limit=10) -> List[str]:
#     results = []
#     if not node:
#         return results
#     queue = collections.deque([node])
#     while queue and len(results) < limit:
#         item = queue.popleft()
#         results.extend(item.titles)
#         children = list(item.children.keys())
#         children.sort()
#         children.reverse()
#         for child in children:
#             queue.appendleft(item.children.get(child))
#     return results[:limit]

def search(index: Node, query: str, limit=10) -> List[str]:
    keywords = extract_keywords(query)
    node = find_node(index, keywords)
    return get_candidates(node, limit)


# def search_in_order(index: Node, query: str, limit=10) -> List[str]:
#     keywords = extract_keywords(query)
#     node = find_node(index, keywords)
#     return get_candidates_in_order(node, limit)

def solve(titles: List[str], queries: List[str]):
    root = build_index(titles)
    for query in queries:
        pages = search(root, query)
        pages.sort()
        for page in pages:
            print(page)

def main():
    tiles_num = int(input())
    titles = []
    for _ in range(tiles_num):
        title = input()
        titles.append(title)
    query_size = int(input())
    queries = []
    for _ in range(query_size):
        query = input()
        queries.append(query)
    solve(titles, queries)
  
if __name__ == "__main__":
    main()


