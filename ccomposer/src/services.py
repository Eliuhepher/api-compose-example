import requests

CARDS_API_URL = "http://localhost:8000"
CLIENTS_API_URL = "http://localhost:9000"

def create_card(card_data):
    """Create a card in the external API."""
    response = requests.post(f"{CARDS_API_URL}/cards", json=card_data)
    return response.json()

def get_card(card_id):
    """Get a card from the external API."""
    response = requests.get(f"{CARDS_API_URL}/cards/{card_id}")
    print(response.json())
    return response.json()

def get_all_cards():
    """Get all cards from the external API."""
    response = requests.get(f"{CARDS_API_URL}/cards")
    response.raise_for_status()
    return response.json()

def create_client(client_data):
    """"Create a client in the external API."""
    response = requests.post(f"{CLIENTS_API_URL}/clients", json=client_data)
    return response.json()

def get_client(client_id):
    """Get a client from the external API."""
    response = requests.get(f"{CLIENTS_API_URL}/clients/{client_id}")
    return response.json()

def get_all_clients():
    """Get all clients from the external API."""
    response = requests.get(f"{CLIENTS_API_URL}/clients")
    response.raise_for_status()
    return response.json()
