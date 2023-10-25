"""
Module
------

    test_obsio_read_atcf.py

Description
-----------

    This is the base-class object for all Automated Tropical Cyclone
    Forecast (ATCF) formatted file reading application unit-tests.

Classes
-------

    TestObsIOReadATCF()

        This is the base-class object for unit-tests related to the
        `obsio.atcf.read_atcf` module functions; it is a sub-class of
        unittest.TestCase.

Author(s)
---------

    Henry R. Winterbottom; 12 September 2023

History
-------

    2023-09-12: Henry Winterbottom -- Initial implementation.

"""

# ----

import unittest
from unittest.mock import patch

from atcf import ATCF
from exceptions import ATCFReadError

# ----


class TestObsIOReadATCF(unittest.TestCase):
    """
    Description
    -----------

    This is the base-class object for unit-tests related to the
    `obsio.atcf.read_atcf` module functions; it is a sub-class of
    unittest.TestCase.

    """

    def setUp(self: unittest.TestCase) -> None:
        """
        Description
        -----------

        This function configures the unit-test(s) attribute(s).

        """

        # Initialize the base-class attributes.
        self.atcf_instance = ATCF()
        self.assertEqual(self.atcf_instance.obs_type, "atcf")

    @patch("atcf.read_tcvfile")
    def test_read_tcvfile(self: unittest.TestCase, mock_read_tcvfile: str) -> None:
        """
        Description
        -----------

        This method mocks the `read_tcvfile` function.

        Parameters
        ----------

        mock_read_tcvfile: str

            A Python string specifying the name of the mock ATCF
            formatted file.

        """

        # Mock the `read_tcvfile` function and compare the specified
        # attributes.
        mock_tcvobj = {"record1": "data1", "record2": "data2"}
        mock_read_tcvfile.return_value = mock_tcvobj
        atcf_filepath = "fake/atcf/file/path.tcv"
        result = self.atcf_instance.read(atcf_filepath)
        mock_read_tcvfile.assert_called_once_with(filepath=atcf_filepath)
        self.assertEqual(result, mock_tcvobj)

    def test_read_with_none_filepath(self: unittest.TestCase) -> None:
        """
        Description
        -----------

        This method tests that the `ATCFReadError` exception is raised
        if the ATCF-formatted file path is not defined or is NoneType
        upon entry.

        """

        # Test that a missing ATCF-formatted file path raises an
        # exception.
        with self.assertRaises(ATCFReadError):
            self.atcf_instance.read(atcf_filepath=None)


# ----


if __name__ == "__main__":
    unittest.main()
