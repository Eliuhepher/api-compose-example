import graphene


class Card(graphene.ObjectType):
    """Card model"""
    id = graphene.ID()
    issuer = graphene.String()
    card_number = graphene.String()
    type = graphene.String()
    status = graphene.String()
    cardholder_id = graphene.String()
    expiration_date = graphene.String()

class Client(graphene.ObjectType):
    """Client model"""
    id = graphene.ID()
    name = graphene.String()
    email = graphene.String()

class ClientWithCards(Client):
    """Client with cards model"""
    cards = graphene.List(Card)

class CardWithClient(Card):
    """Card with client model"""
    client = graphene.Field(Client)
