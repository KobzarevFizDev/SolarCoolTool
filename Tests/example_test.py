from unittest import TestCase, main

import functions_for_tests

class ExampleTest(TestCase):
    def test_summ(self):
        self.assertEqual(functions_for_tests.summ(3, 4), 7)

    def test_diff(self):
        self.assertEqual(functions_for_tests.diff(4,2), 2)

    def test_array(self):
        self.assertEqual([1,2,3,4], [1,2,3,4])

if __name__ == "__main__":
    main(exit=False)