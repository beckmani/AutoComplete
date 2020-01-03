import unittest
from exceptions import TreeAlreadyExist
from auto_complete import Autocomplete


class OneACTest(unittest.TestCase):
    def test_exception_on_second_ac(self):
        ac = Autocomplete('../dictionary.txt')
        with self.assertRaises(TreeAlreadyExist) as context:
            ac._build_tree('../dictionary.txt')
        self.assertTrue('_build_tree function should be called only once' in str(context.exception))

    def test_get_stats(self):
        ac = Autocomplete('../dictionary.txt')
        self.assertEqual(204833, ac.get_stats()['wordCount'])

    def test_get_ac_with_wrong_path(self):
        with self.assertRaises(FileNotFoundError) as context:
            ac = Autocomplete('non_exist')
        self.assertTrue('No such file or directory' in str(context.exception))
