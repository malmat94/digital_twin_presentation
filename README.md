# Digital Twin Presentation

This project demonstrates the creation of a basic digital twin application. It includes data generation, visualization, machine learning, and database interaction. The main components of the project are outlined below.

---

## Project Overview

1. **Data Generator**  
   - A basic data generator that creates sinusoidal data with added noise.

2. **Visualization Scripts**  
   - Uses `matplotlib` or `seaborn` to generate visualizations:
     - Three line plots on a single canvas.
     - A single line plot.
     - Two plots on one canvas.
     - Two curves on a single plot with dual Y-axes.

3. **Database Interaction**  
   - A class for connecting to and interacting with an MS SQL database using `sqlalchemy` and `pandas`.
   - Performs simple database operations.

4. **Calculation Script**  
   - A script for performing basic calculations on generated or retrieved data.

5. **Machine Learning**  
   - A script for training a machine learning model:
     - Uses `scikit-learn`'s Random Forest Regression.
     - Saves the trained model using `joblib`.

6. **Prediction and Storage**  
   - A script that loads the trained model, performs predictions, and saves the results back to the database.

7. **Prediction Verification**  
   - A script to validate the predictions made by the model.

8. **Visualization**  
   - Visualizes the data using `matplotlib` or `seaborn`.
   - Visualize input data of given data batch, calculation results and 
     predictions/ calculations comparison.

9. **Logging**  
   - Uses `logging` to log messages and errors.
   - Stores logs in a file named `twin_logs.txt`.

10. **Settings**
   - Project is based on settings stored in `settings/settings.json` file.
   - Training and predictions schedule is stored in 
     `prediction_models/prediction_schedule.json` file.

11. **Pipeline**  
   - A full pipeline that integrates all components:
     - Connect to sensors database.
     - Retrieves a time range from the database.
     - Load the sensor data.
     - Performs calculations.
     - Save calculations to the Calculations database.
     - Trains the machine learning model (if specific time range is satisfied).
     - Saves the model.
     - Makes predictions having future sensor data and save it to 
       predictions table.
     - Validates predictions.
     - Make a disposition for further model training if the validation is not 
       good enough.
     - Generates visualizations.
---

## Prerequisites

- Python 3.12+
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib` or `seaborn`
  - `sqlalchemy`
  - `scikit-learn`
  - `joblib`
  - `logging`
- An instance of MS SQL Server.

---
