import collections


class TreeNode:

    def __init__(self):
        self.children = {}
        self.word = None

    def insert(self, word):
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = TreeNode()
            node = node.children[char]
        node.word = word
        return node

    def traverse(self, query):
        node = self
        for char in query:
            child = node.children.get(char)
            if child:
                node = child
            else:
                return None

        return node

    def __repr__(self, *args, **kwargs):
        return f'< children: {list(self.children.keys())}, word: {self.word} >'
    
    def get_descendant_nodes(self):
        que = collections.deque()
        for char, child_node in self.children.items():
            que.append((char, child_node))
        while que:
            char, child_node = que.popleft()
            if child_node.word:
                yield child_node
            for char, grand_child_node in child_node.children.items():
                que.append((char, grand_child_node))

    def get_decendent_words(self):
        found_nodes_gen = self.get_descendant_nodes()
        words = list(map(lambda node: node.word, found_nodes_gen))
        return words
