## homework1-witchapat

### How to Run
1. ``pip install -r requirements.txt`` to install dependencies
2. ``python run.py``, then all set to run!

### APIs
``url/machines/`` Post Method: to create a machine with a JSON body
| Body        | Type      | Description                                                       |
|:------------|:----------|:------------------------------------------------------------------|
| `name`      | `string`  | name of a vending machine                    |
| `location`  | `string`  | Location of the vending machine                     |
ex.
```json
{
    "name": "Vending Machine eiei",
    "location": "Bangkhae"
}
```

``url/machines/`` Get Method: to get all machines info
``url/machines/:id`` Get Method: to get one machine info
``url/machines/:id`` Put Method: to add product to a paticular machine's stock
``url/machines/:id`` Post Method: to buy product from a paticular machine's stock




for add product and buy product from the stock api, the request needs a body like this (which I already know that's not a good practice)
```json
{
    "Water": 1,
    "Coke": 5,
    "Coin": 10
}
```


``url/machines/:id`` Delete Method: to delete a machine by its ID

