# Python/third-party imports
import pandas as pd
from sqlalchemy import create_engine


class DBHandler:
    def __init__(
        self,
        server_name: str,
        database_name: str,
    ):
        """
        Initialize the DBHandler object.

        Parameters
        ----------
        server_name : str
            The name of the server to connect to.
        database_name : str
            The name of the database to connect to.

        Attributes
        ----------
        server_name : str
            The name of the server to connect to.
        database_name : str
            The name of the database to connect to.
        engine : sqlalchemy.engine.Engine
            The engine object to interact with the database.
        """

        self.server_name = server_name
        self.database_name = database_name
        self.engine = create_engine(
            f"mssql+pyodbc://{self.server_name}/{self.database_name}?"
            f"driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
        )


    def insert_data(
        self,
        table_name: str,
        schema_name: str,
        data: pd.DataFrame
    ) -> str:
        """
        Inserts data into a specified table in a specified database.

        Parameters
        ----------
        table_name : str
            The name of the table to insert data into.
        schema_name : str
            The name of the schema to insert data into.
        data : pandas.DataFrame
            The data to insert into the table.

        Returns
        -------
        str
            A message indicating that the data was inserted successfully.
        """

        data.to_sql(
            name=table_name,
            schema=schema_name,
            con=self.engine,
            if_exists='append',
            index=False
        )
        data_shape = data.shape
        data_rows = data_shape[0]
        data_columns = data_shape[1]
        saving_message = (
            f'Data of shape {data_columns} columns and {data_rows} rows '
            f'inserted into {self.database_name}.{schema_name}.{table_name}'
        )
        return saving_message


    def load_data(
        self,
        table_name: str,
        schema_name: str,
        columns: list[str] | str = '*',
        timestamps_list: list[int] = None
    ):
        """
        Loads data from a specified table in a specified database.

        Parameters
        ----------
        table_name : str
            The name of the table to load data from.
        schema_name : str
            The name of the schema to load data from.
        columns : list[str] | str, optional
            The columns to load from the table. Defaults to '*'.
        timestamps_list : list[int], optional
            The start and end timestamps to load data for. Defaults to None.

        Returns
        -------
        pandas.DataFrame
            The loaded data.
        """

        if isinstance(columns, list):
            columns = ', '.join(columns)

        if timestamps_list:
            where_clauses = (
                f"WHERE timestamp >= {timestamps_list[0]}"
                f" and timestamp <= {timestamps_list[1]}"
            )
        else:
            where_clauses = ""
        query = (
            f"SELECT {columns} "
            f"FROM {schema_name}.{table_name} "
            f"{where_clauses}"
        )

        return pd.read_sql(query, con=self.engine)


    def get_max_and_min_time(
        self,
        table_name: str,
        schema_name: str,
    ) -> pd.DataFrame:
        """
        Gets the maximum and minimum timestamp from a specified table in a
        specified database.

        Parameters
        ----------
        table_name : str
            The name of the table to get the timestamps from.
        schema_name : str
            The name of the schema to get the timestamps from.

        Returns
        -------
        pandas.DataFrame
            A DataFrame containing the maximum and minimum timestamps.
            Timestamps are integers in seconds.
        """

        query = (
            f"SELECT MAX(timestamp) as max_timestamp, "
            f"MIN(timestamp) as min_timestamp "
            f"FROM {self.database_name}.{schema_name}.{table_name}"
        )
        return pd.read_sql(query, con=self.engine)


    def check_table_timestamps(
        self,
        table_name: str,
        schema_name: str,
        print_message=False
    ) -> tuple[pd.Timestamp, pd.Timestamp]:
        """
        Retrieves and optionally prints the minimum and maximum timestamps
        of a specified table in a specified database schema.

        Parameters
        ----------
        table_name : str
            The name of the table to retrieve timestamps from.
        schema_name : str
            The name of the schema containing the table.
        print_message : bool, optional
            If True, prints the retrieved timestamps. Defaults to False.

        Returns
        -------
        tuple[pandas.Timestamp, pandas.Timestamp]
            A tuple containing the minimum and maximum timestamp as
            pandas.Timestamp objects is in format '%Y-%m-%d %H:%M:%S'
            example: 2024-01-01 00:00:00
        """

        max_min_timestamps = self.get_max_and_min_time(
            table_name=table_name,
            schema_name=schema_name
        )
        max_datetime = pd.to_datetime(
            max_min_timestamps.loc[0, 'max_timestamp'], unit='s'
        )
        min_datetime = pd.to_datetime(
            max_min_timestamps.loc[0, 'min_timestamp'], unit='s'
        )

        if print_message:
            print(
                f"Min timestamp of "
                f"{self.database_name}.{schema_name}.{table_name} is:"
                f"\n{min_datetime} -> "
                f"{max_min_timestamps.loc[0, 'min_timestamp']} "
                f"\nand max timestamp is:"
                f"\n{max_datetime} -> "
                f"{max_min_timestamps.loc[0, 'max_timestamp']} "
            )
        return min_datetime, max_datetime
