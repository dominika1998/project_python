from project import *
import unittest
import os
from matplotlib.colors import is_color_like


class Test(unittest.TestCase):

    def test_helping_functions(self):
        """ Test helping functions. """
        self.assertEqual(mult((1, 1), 2), [2, 2])
        self.assertEqual(mult((2, 2), 0.7), [1, 1])
        self.assertEqual(mult((1, 2, 3, 4, 5, 6), 2), [2, 4, 6, 8, 10, 12])
        self.assertEqual(mult((1, 1), -2), [-2, -2])
        self.assertEqual(get_name('.\\Ordered_default\\athens.jpg'), 'athens.jpg')
        self.assertEqual(get_name('.\\Python'), 'Python')
        self.assertEqual(init_pictures('.\\Ordered', True),
                         ['.\\Ordered\\2.jpg',
                          '.\\Ordered\\5.png',
                          '.\\Ordered\\1.jpg',
                          '.\\Ordered\\3.jpg',
                          '.\\Ordered\\4.jpg'])
        self.assertEqual(init_pictures('.\\Ordered', False),
                         ['.\\Ordered\\1.jpg',
                          '.\\Ordered\\2.jpg',
                          '.\\Ordered\\3.jpg',
                          '.\\Ordered\\4.jpg',
                          '.\\Ordered\\5.png'])

    def test_empty_and_wrong(self):
        self.assertEqual(run_project('.'), 'Wrong name of a directory! / There is nothing to show!')
        self.assertEqual(run_project('blablabla'), 'Wrong name of a directory! / There is nothing to show!')
        self.assertEqual(run_project(''), 'Wrong name of a directory! / There is nothing to show!')

    """ I take the newest history file to test it: 
        histories[len(histories) - 1 """

    def test_history_al(self):
        run_project('.\\Ordered_default')
        histories = os.listdir('.\\History')
        f1 = open('.\\History\\' + histories[len(histories) - 1])
        f2 = open('.\\Test_files\\test_history_al.txt')
        self.assertTrue([row for row in f1] == [row for row in f2])
        f2.close()
        f1.close()


    def test_history_order(self):
        run_project('.\\Ordered')
        histories = os.listdir('.\\History')
        f1 = open('.\\History\\' + histories[len(histories) - 1])
        f2 = open('.\\Test_files\\test_history_order.txt')
        self.assertTrue([row for row in f1] == [row for row in f2])
        f2.close()
        f1.close()


    def test_history_wrong(self):
        run_project('.\\Ordered_wrong')
        histories = os.listdir('.\\History')
        f1 = open('.\\History\\' + histories[len(histories) - 1])
        f2 = open('.\\Test_files\\test_history_order.txt')
        self.assertTrue([row for row in f1] != [row for row in f2])
        f2.close()
        f1.close()


    def test_color(self):
        self.assertTrue(is_color_like('black'))
        self.assertTrue(is_color_like('#71EAB3'))
        self.assertFalse(is_color_like('dominika'))

    def test_comment_reformat(self):
        self.assertTrue("This comment\nis definitely\ntoo long and I\nneed to\nreformat it\ninto lines." == reformat_comment("This comment is definitely too long and I need to reformat it into lines."));


if __name__ == '__main__':
    unittest.main()
