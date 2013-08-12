#!/usr/bin/python
import unittest
from dict_object_differ import DictObjectDiffer


class testDictObjectDifferConstructor(unittest.TestCase):

    def setUp(self):
        class Object(object):
            pass
        self.gen_obj = Object()

    def test1_constructor(self):
        dod = DictObjectDiffer([], object, {})
        self.assertFalse(dod is None)

    def test2_constructor_raises_on_no_dict(self):
        self.assertRaises(BaseException, DictObjectDiffer, None, object, {})

    def test3_constructor_raises_on_no_object(self):
        self.assertRaises(BaseException, DictObjectDiffer, [], None, {})

    def test4_constructor_raises_on_compare_map(self):
        self.assertRaises(BaseException, DictObjectDiffer, [], object, None)

    def test5_constructor_sets_diff_dict_correctly(self):
        test_dict = {
            'foo': 'bar'
        }

        dod = DictObjectDiffer(test_dict, object, {})
        self.assertEqual(dod.diff_dict, test_dict)

    def test6_constructor_sets_diff_object_correctly(self):
        setattr(self.gen_obj, 'foo', 'bar')

        dod = DictObjectDiffer({}, self.gen_obj, {})
        self.assertEqual(dod.diff_object.foo, 'bar')

    def test7_constructor_sets_compare_map_correctly(self):
        test_dict = {
            'foo': 'bar',
        }

        dod = DictObjectDiffer(test_dict, object, test_dict)
        self.assertEqual(dod.compare_map, test_dict)


class testDictObjectDiffer(unittest.TestCase):

    def setUp(self):
        class Object(object):
            pass
        self.gen_obj = Object()

    def test1_object_equals_dict(self):
        test_dict = {
            'foo': 'foo'
        }
        """ We haven't added a foo attribute to our gen_obj
            so dod.missing_from_object should include {'foo': 'bar'}
        """
        setattr(self.gen_obj, 'foo', 'foo')
        dod = DictObjectDiffer(test_dict, self.gen_obj, {'foo': 'foo'})
        self.assertEqual(
            dod._missing_from_object(test_dict, self.gen_obj, {'foo': 'foo'}),
            {}
        )

    def test2_object_missing_attribute(self):
        test_dict = {
            'foo': 'foo'
        }
        """ We haven't added a foo attribute to our gen_obj
            so dod.missing_from_object should include {'foo': 'bar'}
        """
        dod = DictObjectDiffer(test_dict, self.gen_obj, {'foo': 'foo'})
        self.assertEqual(
            dod._missing_from_object(
                test_dict,
                self.gen_obj,
                {'foo': 'foo'}
            ),
            {'foo': 'foo'}
        )

    def test3_dict_missing_key(self):
        test_dict = {}
        """ We haven't added a foo attribute to our gen_obj
            so dod.missing_from_object should include {'foo': 'bar'}
        """
        setattr(self.gen_obj, 'foo', 'foo')
        dod = DictObjectDiffer(test_dict, self.gen_obj, {'foo': 'foo'})
        self.assertEqual(
            dod._missing_from_dict(
                test_dict,
                self.gen_obj,
                {'foo': 'foo'}
            ),
            {'foo': 'foo'}
        )

    def test4_object_and_dict_differ(self):
        test_dict = {
            'foo': 'bar',
        }
        setattr(self.gen_obj, 'foo', 'baz')
        dod = DictObjectDiffer(test_dict, self.gen_obj, {'foo': 'foo'})
        dict_difference, object_difference = \
            dod._compare_dict_to_object(
                test_dict, self.gen_obj,
                {'foo': 'foo'}
            )
        self.assertEqual(dict_difference, {'foo': 'baz'})
        self.assertEqual(object_difference, {'foo': 'bar'})

    def test5_full_integration_test_missing_from_dict(self):
        test_dict = {
            'foo': 'bar',
            'aaa': 'bbb',
            'ccc': 'bbb',
            'zzz': 'zzz',
        }
        compare_dict = {
            'foo': 'foo',
            'aaa': 'aaa',
            'ccc': 'ccc',
            'yyy': 'yyy',
            'zzz': 'zzz',
        }
        setattr(self.gen_obj, 'foo', 'bar')
        setattr(self.gen_obj, 'aaa', 'zzz')
        setattr(self.gen_obj, 'ccc', 'ddd')
        setattr(self.gen_obj, 'yyy', 'yyy')
        dod = DictObjectDiffer(test_dict, self.gen_obj, compare_dict)
        dod.compare()
        self.assertEqual(dod.dict_difference, {
            'ccc': 'ddd',
            'aaa': 'zzz',
        })
        self.assertEqual(dod.object_difference, {
            'aaa': 'bbb',
            'ccc': 'bbb',
        })
        self.assertEqual(dod.missing_from_dict, {
            'yyy': 'yyy',
        })
        self.assertEqual(dod.missing_from_object, {
            'zzz': 'zzz',
        })


if __name__ == '__main__':
    unittest.main()
