from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Create the FastAPI app instance
app = FastAPI()

# Setup CORS middleware
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is our main endpoint for the real estate data
@app.get("/properties")
def get_properties():
    # 1. Read the data from our CSV file
    df = pd.read_csv("properties.csv")

    # 2. Calculate our simple "AI" score
    # We define profitability as the annual rent divided by the price.
    df["profitability_score"] = (df["monthly_rent"] * 12) / df["price"]

    # 3. Sort the properties by our score (best deals first)
    df = df.sort_values(by="profitability_score", ascending=False)

    # 4. Convert the DataFrame to a list of dictionaries to send as JSON
    properties_list = df.to_dict(orient="records")

    return properties_list

# You can keep the root endpoint for testing if you like
@app.get("/")
def read_root():
    return {"Hello": "World"}