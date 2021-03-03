import os

from dotenv import find_dotenv, load_dotenv

# find .env automatically by walking up directories until it's found
dotenv_path = find_dotenv()

# load up the entries as environment variables
load_dotenv(dotenv_path)

# For Entrez API
email = os.environ.get("EMAIL")
entrez_api_key = os.environ.get("ENTREZ_API_KEY")

data_path = os.environ.get("DATA_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data')))
