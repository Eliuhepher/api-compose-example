# main.py
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp
from schema import schema

app = FastAPI()

app.add_route("/graphql", GraphQLApp(schema=schema))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)