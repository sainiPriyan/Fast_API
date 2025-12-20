from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

contacts = {1: 'Alice', 2: 'Bob', 3: 'Charlie', 4: 'Diana', 5: 'Ethan', 6: 'Fiona'}

class Contact(BaseModel):
    id: int
    name: Optional[str] = None

myapp = FastAPI()

@myapp.get('/')
def index():
    return {'data':{'name': 'John Doe'} }

@myapp.get('/about')
def about():
    return {'about':'This is an about page.'}

@myapp.get('/contact/list')
def contact_list(query : str = 'all', id:bool = False):
  if id == False:
    if query == 'even':
        even_contacts = [contacts[i] for i in contacts.keys() if i % 2 == 0]
        return {'contacts': even_contacts}

    elif query == 'odd':
        odd_contacts = [contacts[i] for i in contacts.keys() if i % 2 != 0]
        return {'contacts': odd_contacts}
    
    elif query == 'all':
        return {'contacts': list(contacts.values())}
    
  else:
    if query == 'even':
        even_contacts = [(i, contacts[i]) for i in contacts.keys() if i % 2 == 0]
        return {'contacts': even_contacts}

    elif query == 'odd':
        odd_contacts = [(i, contacts[i]) for i in contacts.keys() if i % 2 != 0]
        return {'contacts': odd_contacts}
    
    elif query == 'all':
        return {'contacts': list(contacts.items())}

@myapp.get('/contact/{id}')
def contact(id: int, message: str = 'Hello'):
    return {'contact_id': contacts.get(id, 'Not Found'), 'message': message}


@myapp.get('/contact/{id}/details')
def contact_details(id: int):
    return {'contact_id': id, 'details': contacts.get(id, 'Not Found')}

@myapp.post('/contact/create')
def create_contact(contact: Contact):
    contacts[contact.id] = contact.name
    return {'message': 'Contact created successfully'}




