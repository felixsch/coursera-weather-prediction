A quick webapp using flask and sqlalchemy to load weather predictions from openMeteo.

## How to run this App

```
# Step 1: Create a virtual environment
python3 -m venv weather-example

# Step 2: Activate the virtual environment (Linux/macOS)
source weather-example/bin/activate

# (Windows)
weather-example\Scripts\activate

# Step 4: Run your application
./run-app run

# Step 5: Open the page in your browser
xdg-open http://localhost:5000
```

Note: When you running the Flask application manually without the script `run-app` make sure to run `flask initialize-database` before you run `FLASK_APP="src/app.py" flask run`.
