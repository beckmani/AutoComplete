from threading import Lock
from tree import TreeNode
from exceptions import TreeAlreadyExist


class Autocomplete:

    def __init__(self, path_to_dict):
        """
        :param path_to_dict: a path to file holds the dictionary
        """
        self._lock = Lock()
        self._tree_root = None
        self.stats = {'wordCount': 0}
        self._build_tree(path_to_dict)

    def get_stats(self):
        return self.stats

    def _build_tree(self, path_to_dict):
        with self._lock:
            if not self._tree_root:
                self._tree_root = TreeNode()
                with open(path_to_dict, 'r') as f:
                    while True:
                        word = f.readline().strip()
                        if not word:
                            break
                        self._tree_root.insert(word)
                        self.stats['wordCount'] = self.stats['wordCount']+1
            else:
                raise TreeAlreadyExist

    def search(self, prefix):
        """
        :param prefix: a prefix to search for
        :return: list of words according to prefix
        """
        words = []
        node = self._tree_root.traverse(prefix)
        if node:
            words = node.get_decendent_words()
        return words
