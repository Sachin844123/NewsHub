# Flask Application

This is a simple Flask web application that demonstrates the basic structure and functionality of a Flask project.

## Project Structure

```
flask-app
├── app.py                 # Main Flask application
├── run.py                 # Production runner
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── .gitignore             # Git ignore file
├── Procfile               # Deployment configuration
├── templates              # HTML templates
│   ├── index.html        # Main page template
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
└── static                 # Static files
    ├── css/
    │   └── styles.css    # Your existing CSS
    └── js/
        └── app.js        # Enhanced JavaScript
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the root directory and add your environment variables.

## Running the Application

To run the application in development mode, use:

```
python app.py
```

For production, use:

```
python run.py
```

## Usage

Visit `http://localhost:5000` in your web browser to view the application. 

## Error Pages

The application includes custom error pages for 404 and 500 errors, which are defined in the `templates` directory.

## License

This project is licensed under the MIT License.