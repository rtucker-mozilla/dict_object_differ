#!/usr/bin/python


class DictObjectDiffer(object):
    diff_dict = []
    diff_object = None
    compare_map = {}
    missing_from_dict = {}
    added_to_dict = {}
    missing_from_object = {}
    added_to_object = {}
    dict_difference = {}
    object_difference = {}

    def __init__(
        self,
        diff_dict=None,
        diff_object=None,
        compare_map=None,
    ):
        """__init__
        :param diff_dict: dictionary of key/value pairs to compare to
            diff_object
        :param diff_object: python object with attributes to compare to the
            diff_dict object
        :param compare_map: mapping of diff_dict keys to object attribute
            The dictionary key is that off the diff_dict
            The value of the key is the attribute of the diff_object
            compare_map[dict_key] = 'object.attribute_name'
        """

        if diff_dict is None:
            raise BaseException("diff_dict is required")
        if diff_object is None:
            raise BaseException("diff_object is required")
        if compare_map is None:
            raise BaseException("compare_map is required")

        self.diff_dict = diff_dict
        self.diff_object = diff_object
        self.compare_map = compare_map

    def compare(self):
        """ compare
            The only public method to be called. Will calculate all of the
            diffs between the object and the dict.
        """
        self.missing_from_dict = self._missing_from_dict()
        self.missing_from_object = self._missing_from_object()
        self.dict_difference, self.object_difference =\
            self._compare_dict_to_object()

    def _compare_dict_to_object(
        self,
        diff_dict=None,
        diff_object=None,
        compare_map=None,
    ):
        """_compare_dict_to_object
        Figure out the dictionary keys that are missing from the object
        :param diff_dict: dictionary of key/value pairs to compare to
            diff_object
        :param diff_object: python object with attributes to compare to the
            diff_dict object
        :param compare_map: mapping of diff_dict keys to object attribute
            The dictionary key is that off the diff_dict
            The value of the key is the attribute of the diff_object
            compare_map[dict_key] = 'object.attribute_name'
        """
        if not diff_dict:
            diff_dict = self.diff_dict

        if not diff_object:
            diff_object = self.diff_object

        if not compare_map:
            compare_map = self.compare_map

        dict_difference = {}
        object_difference = {}

        for k in compare_map.iterkeys():
            try:
                if not diff_dict[k] == getattr(diff_object, compare_map[k]):
                    dict_difference[k] = getattr(diff_object, compare_map[k])
                    object_difference[compare_map[k]] = diff_dict[k]
            except (KeyError, IndexError, AttributeError):
                """ We don't need to track missing items across the
                two comparison metrics here. They are handled via:
                _missing_from_object
                _missing_from_dict
                """
                pass

        return dict_difference, object_difference

    def _missing_from_object(
        self,
        diff_dict=None,
        diff_object=None,
        compare_map=None,
    ):
        """_missing_from_object
        Figure out the dictionary keys that are missing from the object
        :param diff_dict: dictionary of key/value pairs to compare to
            diff_object
        :param diff_object: python object with attributes to compare to the
            diff_dict object
        :param compare_map: mapping of diff_dict keys to object attribute
            The dictionary key is that off the diff_dict
            The value of the key is the attribute of the diff_object
            compare_map[dict_key] = 'object.attribute_name'
        """
        return_dict = {}
        if not diff_dict:
            diff_dict = self.diff_dict

        if not diff_object:
            diff_object = self.diff_object

        if not compare_map:
            compare_map = self.compare_map

        for k in compare_map.iterkeys():
            if not hasattr(diff_object, compare_map[k]):
                return_dict[k] = diff_dict[k]

        return return_dict

    def _missing_from_dict(
        self,
        diff_dict=None,
        diff_object=None,
        compare_map=None,
    ):
        """_missing_from_object
        Figure out the dictionary keys that are missing from the object
        :param diff_dict: dictionary of key/value pairs to compare to
            diff_object
        :param diff_object: python object with attributes to compare to the
            diff_dict object
        """

        return_dict = {}
        if not diff_dict:
            diff_dict = self.diff_dict

        if not diff_object:
            diff_object = self.diff_object

        if not compare_map:
            compare_map = self.compare_map

        for k in compare_map.iterkeys():
            if hasattr(diff_object, compare_map[k]) \
                    and not k in diff_dict:
                return_dict[k] = k

        return return_dict
