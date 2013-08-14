dict_object_differ
==================

Python library for comparing values from an object to a dictionary with selective attribute comparision

usage
=====

foo = {'foo': 'bar'}

bar = CustomObject()

compare map is a mapping of dictionary keys in dict_diff to object_diff

compare_map = {'foo': 'foo'}

dod = DictObjectDiffer(diff_dict=foo, diff_object=bar, compare_map=compare_map)

dod.compare()

dod.missing_from_dict # dictionary containing attributes found in object, but that are not present in the dict

dod.missing_from_object # dictionary containing dictionary keys found in object, but that are not present in the object

dod.dict_difference # dictionary containing the value of the attribute as found in the object

dod.object_difference # dictionary containing the value of the dictionary key as found in the dict
