# Python/third-party imports
import json
import pandas as pd

# Internal imports
from db_handler import DBHandler
from unittest import TestCase


class TestDBHandler(TestCase):
    def setUp(self):
        """
        Set up the test case by loading the settings from
        "settings/settings.json" and initializing a DBHandler object.
        """
        with open("settings/settings.json", "r") as server:
            settings = json.load(server)
        self.server_name = settings['server']
        self.database_name = settings['sensors']['database']
        self.schema_name = settings['sensors']['schema']
        self.table_name = settings['sensors']['table']
        self.db_object = DBHandler(
            server_name=self.server_name,
            database_name = self.database_name
        )


    def test_check_table_timestamps(self):
        """
        Test the `check_table_timestamps` method of the DBHandler class.

        This test verifies that the `check_table_timestamps` method retrieves
        the correct minimum and maximum timestamps from a specified table
        and schema. It also checks that the timestamps returned are equivalent
        when converted to pandas Timestamp objects with seconds as the unit.
        """
        timestamps = self.db_object.check_table_timestamps(
            table_name=self.table_name,
            schema_name = self.schema_name,
            print_message=True
        )
        timestamps_int = []
        for timestamp in timestamps:
            timestamps_int.append(pd.to_datetime(timestamp, unit='s'))
        self.assertEqual(timestamps[0], timestamps_int[0])
        self.assertEqual(timestamps[1], timestamps_int[1])


    def test_load_data(self):
        """
        Test the `load_data` method of the DBHandler class.

        This test verifies that the `load_data` method retrieves
        the correct data from a specified table and schema given
        a list of columns and timestamps range. It also checks that
        the data returned is of the correct length and contains the
        expected columns.
        """
        data = self.db_object.load_data(
            table_name=self.table_name,
            schema_name=self.schema_name,
            columns=['torque', 'speed'],
            timestamps_list=[1705199900, 1705200000]
        )
        self.assertTrue(len(data), 101)
        self.assertTrue('torque' in data.columns)
        self.assertTrue('speed' in data.columns)
