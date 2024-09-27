# schema.py
import graphene
from services import (
    get_card,
    get_client,
    get_all_cards,
    get_all_clients,
    create_card,
    create_client,
)
from models import Card, Client, ClientWithCards, CardWithClient


class Query(graphene.ObjectType):
    """"|Query| class to define the queries."""
    card = graphene.Field(Card, id=graphene.ID(required=True))
    all_cards = graphene.List(Card)
    client = graphene.Field(Client, id=graphene.ID(required=True))
    all_clients = graphene.List(Client)
    all_clients_with_cards = graphene.List(ClientWithCards)
    card_by_id_with_client = graphene.Field(CardWithClient, id=graphene.ID(required=True))

    def resolve_card(self, info, id):
        """Resolve a card by its ID."""
        response = get_card(id)
        print(response)
        return Card(**response)

    def resolve_all_cards(self, info):
        """Resolve all cards."""
        response = get_all_cards()
        return [Card(**card) for card in response]

    def resolve_client(self, info, id):
        """Resolve a client by its ID."""
        response = get_client(id)
        return Client(**response)

    def resolve_all_clients(self, info):
        """Resolve all clients."""
        response = get_all_clients()
        return [Client(**client) for client in response]
    
    def resolve_all_clients_with_cards(self, info):
        """Resolve all clients with their assigned cards."""
        clients = get_all_clients()
        cards = get_all_cards()
        for client in clients:
            client["cards"] = [card for card in cards if card["cardholder_id"] == client["id"]]
        return [ClientWithCards(**client) for client in clients]
    
    def resolve_card_by_id_with_client(self, info, id):
        """Resolve a card with its client."""
        card = get_card(id)
        client = get_client(card["cardholder_id"])
        card["client"] = client
        return CardWithClient(**card)


class CreateCard(graphene.Mutation):
    """"|CreateCard| class to define the mutation."""
    class Arguments:
        """Arguments for the mutation."""
        issuer = graphene.String(required=True)
        card_number = graphene.String(required=True)
        type = graphene.String(required=True)
        status = graphene.String(required=True)
        cardholder_id = graphene.String(required=True)
        expiration_date = graphene.String(required=True)

    card = graphene.Field(Card)

    def mutate(
        self, info, issuer, card_number, type, status, cardholder_id, expiration_date
    ):
        """Mutate to create a card."""
        card_data = {
            "issuer": issuer,
            "card_number": card_number,
            "type": type,
            "status": status,
            "cardholder_id": cardholder_id,
            "expiration_date": expiration_date,
        }
        response = create_card(card_data)
        return CreateCard(card=Card(**response))


class CreateClient(graphene.Mutation):
    """"|CreateClient| class to define the mutation."""
    class Arguments:
        """Arguments for the mutation."""
        name = graphene.String(required=True)
        email = graphene.String(required=True)

    client = graphene.Field(Client)

    def mutate(self, info, name, email):
        """Mutate to create a client."""
        client_data = {"name": name, "email": email}
        response = create_client(client_data)
        return CreateClient(client=Client(**response))


class Mutation(graphene.ObjectType):
    """"|Mutation| class to define the mutations."""
    create_card = CreateCard.Field()
    create_client = CreateClient.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
