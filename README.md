# MoviWeb App

Flask app to manage favourite movies per user. Movie data comes from the OMDb API.

## Setup
1. Clone the repo and open the folder.
2. Create and activate a virtual environment:
   python3 -m venv .venv
   source .venv/bin/activate
3. Install the packages:
   pip install -r requirements.txt
4. Get a free API key at https://www.omdbapi.com/apikey.aspx
5. Create a file named .env in the project folder with one line:
   OMDB_API_KEY=your-key-here
6. Start the app:
   python app.py
   Then open http://127.0.0.1:5002