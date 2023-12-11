# PT_Demo_Python_FastAPI

## Contents
- [Setup on Windows](#setup-on-windows)
- [Links](#links)

## Setup on Windows

1. Download Python from [the official website](https://www.python.org/downloads/) and install the latest LTS (long term support).

2. Execute the following command to install FastAPI:
```
py -m pip install fastapi
```

3. Execute the following command to install Uvicorn ASGI server for production:
```
py -m pip install "uvicorn[standard]"
```

4. Create a new `main.py` file having the following contents:

```
from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
```

5. Run the ASGI server from the main.py directory using the following command:

```
py -m uvicorn main:app --reload
```

6. Open the following URLs in the browser:
- http://127.0.0.1:8000/docs => old school Swagger
- http://127.0.0.1:8000/redoc => modern Swagger
- http://127.0.0.1:8000 => {"Hello":"World"}
- http://127.0.0.1:8000/items/6?q=somequery => {"item_id":6,"q":"somequery"}

## Links
- https://fastapi.tiangolo.com/
- https://stackoverflow.com/questions/39832219/pip-not-working-in-python-installation-in-windows-10
- https://stackoverflow.com/questions/64936440/python-uvicorn-the-term-uvicorn-is-not-recognized-as-the-name-of-a-cmdlet-f
- https://asgi.readthedocs.io/en/latest/
- 