import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from titlecheck import redundant_title_segment

class TestRedundantTitleSegment(unittest.TestCase):
    def test_doubled_brand(self):
        self.assertEqual(redundant_title_segment('SEO Guide \u2014 SEO Guide'), 'SEO Guide')

    def test_case_insensitive_duplicate(self):
        self.assertEqual(redundant_title_segment('Keyword Research \u2014 keyword research'), 'keyword research')

    def test_em_dash_separator(self):
        self.assertEqual(redundant_title_segment('Foo \u2014 Foo'), 'Foo')

    def test_en_dash_separator(self):
        self.assertEqual(redundant_title_segment('Foo \u2013 Foo'), 'Foo')

    def test_middle_dot_separator(self):
        self.assertEqual(redundant_title_segment('Foo \u00B7 Foo'), 'Foo')

    def test_pipe_separator(self):
        self.assertEqual(redundant_title_segment('Foo | Foo'), 'Foo')

    def test_spaced_hyphen_separator(self):
        self.assertEqual(redundant_title_segment('Foo - Foo'), 'Foo')

    def test_internal_hyphen_no_surrounding_spaces(self):
        self.assertIsNone(redundant_title_segment('on-page SEO tips'))
        self.assertIsNone(redundant_title_segment('on-page-seo'))

    def test_internal_hyphen_preserved_case_insensitive_dup(self):
        self.assertEqual(redundant_title_segment('on-page \u2014 On-Page'), 'On-Page')

    def test_single_segment_no_separators(self):
        self.assertIsNone(redundant_title_segment('Just One Title'))

    def test_empty_string_whitespace_only_none(self):
        self.assertIsNone(redundant_title_segment(''))
        self.assertIsNone(redundant_title_segment(' '))
        self.assertIsNone(redundant_title_segment(None))

    def test_two_distinct_segments(self):
        self.assertIsNone(redundant_title_segment('Keyword Research \u2014 SEO Guide'))

if __name__ == '__main__':
    unittest.main()
