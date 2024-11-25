"""Scripts to generate artificial sensors data for the twin."""
# Python/third-party imports
from pathlib import Path

# Internal imports
from data_generator import generate_data
from plotter_seaborn import three_separate_subplots
from settings import Settings
from db_handler import DBHandler


# Get the settings and dbs objects
server_name, settings, sensors_db_settings, results_db_settings, _ = (
    Settings(
        settings_path=Path('../settings/settings.json')
    ).get_db_settings()
)
sensors_db = DBHandler(
    server_name=server_name,
    database_name=sensors_db_settings['database']
)

# Generate the artificial sensor data
data_generated = generate_data(
    start_timestamp=1704067201,
    end_timestamp=1704067201 + 61 * 24 * 60 * 60,
    max_torque=3000,
    max_speed=300,
    min_temp=-20,
    max_temp=100
)

# Save the artificial data to the db
# saving_message = sensors_db.insert_data(
#     table_name=sensors_db_settings['table'],
#     schema_name=sensors_db_settings['schema'],
#     data=data_generated
# )
# print(saving_message)

# Extract the data sample and plot it
sample_data = data_generated[
    (data_generated['timestamp']>=1704067201)
    & (data_generated['timestamp']<=1704067201 + 24 * 60 * 60)
]
three_separate_subplots(
    x=sample_data['timestamp'],
    y1=sample_data['torque'],
    y2=sample_data['speed'],
    y3=sample_data['oli_temperature'],
    y1_title='Torque in time',
    y2_title='Speed in time',
    y3_title='Oil temperature in time',
    y1_axis_title='Torque [Nm]',
    y2_axis_title='Speed [RPM]',
    y3_axis_title='Oil temp [*C]',
    save_title='Physical parameter',
    save=True
)
