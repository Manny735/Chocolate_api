from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Supabase credentials
url: str = "https://abumjogbbzpymlmcbjsf.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFidW1qb2diYnpweW1sbWNianNmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4MzkzNTAsImV4cCI6MjA1NzQxNTM1MH0.CqWVeSiyEuwFqx4AW7_fRdR3FfucbSz9iY3AvyzKIs4"  # Use environment variables in production!
supabase: Client = create_client(url, key)

app = FastAPI()

class ChocolateBar(BaseModel):
    specific_bean_origin_or_bar_name: str
    rating: int
    cocoa_percent: int

@app.post("/items/")
async def create_chocolate_bar(chocolate_bar: ChocolateBar):
    try:
        # Insert the new chocolate bar without specifying 'id' (database will auto-generate it)
        response = supabase.table("Chocolate").insert(chocolate_bar.dict()).execute()
        # Check for success or failure using response.data
        if response.data:  # If data is returned, it's a success
            return response.data[0]
        else:  # If no data returned, raise an error
            raise HTTPException(status_code=400, detail=f"Failed to insert item: {response.error if hasattr(response, 'error') else 'Unknown error'}")
    except Exception as e:  # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/items/")
async def read_chocolate_bars():
    response = supabase.table("Chocolate").select("*").execute()
    if response.error:
        raise HTTPException(status_code=404, detail=f"Error fetching items: {response.error['message']}")
    
    if not response.data:
        raise HTTPException(status_code=404, detail="No data found")
    return response.data

@app.put("/items/{item_id}")
async def update_chocolate_bar(item_id: int, chocolate_bar: ChocolateBar):
    try:
        response = supabase.table("Chocolate").update(chocolate_bar.dict()).eq("id", item_id).execute()
        
        # Check for success or failure using response.data
        if response.data:  # If data is returned, it's a success
            return response.data[0]
        else:  # If no data returned, raise an error
            raise HTTPException(status_code=400, detail=f"Failed to update item: {response.error if hasattr(response, 'error') else 'Unknown error'}")
    except Exception as e:  # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.delete("/items/{item_id}")
async def delete_chocolate_bar(item_id: int):
    try:
        response = supabase.table("Chocolate").delete().eq("id", item_id).execute()
        
        # Check for success or failure using response.data
        if response.data is not None:  # If operation completed successfully
            return {"message": "Item deleted successfully"}
        else:  # If no data returned, raise an error
            raise HTTPException(status_code=400, detail=f"Failed to delete item: {response.error if hasattr(response, 'error') else 'Unknown error'}")
    except Exception as e:  # Handle any other exceptions
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
