import requests

BASE = "http://127.0.0.1:5000/"


# Use POST() to create a new Car in our database
response = requests.post(BASE + "car/0", {"brand":"Audi", "model":"A3", "year":2014, "bhp": 180})
print(response.json())

input()



# Use PATCH() to update the entry
response = requests.patch(BASE + "car/0", {"model":"A4", "year":2016})
print(response.json())

input()



# We can then use GET() to either get an entry by its ID or get all entries
response = requests.get(BASE + "car/0")
print(response.json())

input()

response = requests.get(BASE + "cars/")
print(response.json())



# Finally we can delete an entry from the database using the DELETE() endpoint
response = requests.delete(BASE + "car/0")
print(response)