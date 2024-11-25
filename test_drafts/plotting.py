"""Scripts for plotting the data."""
# Python/third-party imports
from pathlib import Path

# Internal imports
import plotter_seaborn
from settings import Settings
from db_handler import DBHandler

# Determine the start and stop timestamps and load the settings
start_timestamp = 1704067200
stop_timestamp = 1704153600
server_name, settings, sensors_db_settings, results_db_settings, _ = (
    Settings(settings_path=Path('../settings/settings.json')).get_db_settings()
)

# Get the objects of dbs
sensors_db = DBHandler(
    server_name=server_name,
    database_name=sensors_db_settings['database']
)
results_db = DBHandler(
    server_name=server_name,
    database_name=results_db_settings['database']
)

# Get the data
sensors_data = sensors_db.load_data(
    table_name=sensors_db_settings['table'],
    schema_name=sensors_db_settings['schema'],
    timestamps_list=[start_timestamp, stop_timestamp]
)
results_data = results_db.load_data(
    table_name=results_db_settings['table'],
    schema_name=results_db_settings['schema'],
    timestamps_list=[start_timestamp, stop_timestamp]
)
results_data.sort_values('timestamp', inplace=True)

# Plot the data
# plotter_seaborn.two_separate_subplots(
#     x=sensors_data['timestamp'],
#     y1=sensors_data['torque'],
#     y2=sensors_data['speed'],
#     y1_title='Torque in time',
#     y2_title='Speed in time',
#     y1_axis_title='Torque [Nm]',
#     y2_axis_title='Speed [RPM]'
# )

plotter_seaborn.one_plot(
    x=results_data['timestamp'],
    y=results_data['accumulated_destruction'],
    title='Destruction in time',
    y_axis_name='Destruction [%]',
    # save=True
)
