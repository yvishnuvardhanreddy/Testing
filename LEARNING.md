# FastAPI + HTML/JS Frontend: Learning How API Calls and Responses Work

## Overview
This project demonstrates the full cycle of a backend API built with **FastAPI** and a simple **HTML/JavaScript** frontend that consumes the API. It is intended for learning purposes: see how a frontend calls endpoints, how the server processes requests, and how JSON responses are displayed in the browser.

## Project Structure
```
F:\Learing frontend communication\
├─ backend\
│   ├─ main.py          # FastAPI app + uvicorn entry point
│   └─ requirements.txt
├─ frontend\
│   └─ index.html       # HTML page with JavaScript fetch calls
└─ LEARNING.md          # This document
```

## Backend (`backend/main.py`)
The FastAPI application defines five CRUD endpoints operating on an in‑memory dictionary (`fake_db`):

| Endpoint | Method | Description |
|---|---|---|
| `/items/` | `GET` | Return a list of all items. |
| `/items/{item_id}` | `GET` | Return a single item by ID, or an error if not found. |
| `/items/` | `POST` | Create a new item (name, price, optional description). |
| `/items/{item_id}` | `PUT` | Update an existing item’s name and price. |
| `/items/{item_id}` | `DELETE` | Delete an item by ID. |

The `Item` data model is a Pydantic `BaseModel`, which FastAPI uses for request validation and automatic JSON serialization.

The file also includes an `if __name__ == "__main__"` block that starts **Uvicorn** on `127.0.0.1:8000`:

```python
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

Run this with `python -m backend.main` or `uvicorn backend.main:app --reload`.

## Frontend (`frontend/index.html`)
A single HTML page with five sections, each containing a form/button that calls a different endpoint using the **Fetch API**.

### How the JavaScript works
Each function follows the same pattern:

```js
async function fetchItems() {
  const res = await fetch(`http://127.0.0.1:8000/items/`);
  const data = await res.json();
  document.getElementById("response-get-all").innerHTML = JSON.stringify(data, null, 2);
}
```

1. **`fetch(url)`** – sends an HTTP request to the backend.
2. **`await res.json()`** – parses the JSON response body into a JavaScript object/array.
3. **`JSON.stringify(data, null, 2)`** – pretty‑prints the result into the page.

The five functions correspond to the five endpoints:

| Section | Function | HTTP method |
|---|---|---|
| **Fetch Items** | `fetchItems()` | `GET /items/` |
| **Fetch Single** | `fetchSingleItem()` | `GET /items/{id}` |
| **Create Item** | `createItem()` | `POST /items/` |
| **Update Item** | `updateItem()` | `PUT /items/{id}` |
| **Delete Item** | `deleteItem()` | `DELETE /items/{id}` |

### CORS note
Because the HTML file is loaded via `file://` and the backend runs on `http://127.0.0.1:8000`, some browsers may block the request. The easiest way to avoid this is to use VS Code’s **Live Server** extension (or any local development server) to serve the HTML file over `http://localhost:...`.

## How to Run the Example

### 1. Install dependencies
Open a terminal (PowerShell or CMD) and run:

```powershell
cd F:\Learing frontend communication\backend
pip install -r requirements.txt
```

`requirements.txt` contains:

```
fastapi
uvicorn
```

### 2. Start the FastAPI server
```powershell
cd F:\Learing frontend communication\backend
uvicorn backend.main:app --reload --port 8000
```

You should see output indicating the server is running on `http://127.0.0.1:8000` and that the docs are available at `/docs`.

### 3. Open the frontend page
- **Option A – Double‑click**: `F:\Learing frontend communication\frontend\index.html`
- **Option B – VS Code Live Server**: Right‑click the HTML file and select "Open with Live Server". This serves the page at `http://127.0.0.1:5500` (or another free port) and avoids CORS blocks.

### 4. Interact
- Click **Fetch Items** → see the JSON list of Widget/Gadget.
- Type `item1` in **Fetch Single** → returns that item’s details.
- Fill the **Create** form and click **Create Item** → the new item appears and the list refreshes.
- Use **Update** and **Delete** similarly.

## What Happens Under the Hood

| Step | Description |
|---|---|
| **Client → Server** | The browser’s JavaScript calls `fetch('http://127.0.0.1:8000/items/')`. This creates an HTTP GET request. |
| **Server Routes** | FastAPI matches the URL to the `@app.get("/items/")` function, executes the code, and builds a JSON response (automatically serialising Python `dict`/`BaseModel` objects). |
| **Response Sent** | The server sends back headers `Content-Type: application/json` and the JSON body (e.g., `[{"name":"Widget",...},{"name":"Gadget",...}]`). |
| **Client Receives** | `fetch` resolves with a `Response` object. `await res.json()` extracts the parsed JavaScript object/array. |
| **UI Updated** | The code inserts the JSON string into the page (`innerHTML = JSON.stringify(...)`), so the user sees the data. |

## Next Steps for Learning
- Add **CORS middleware** to allow a real web origin (e.g., `http://localhost:3000`) without browser blocks.
- Replace the in‑memory `fake_db` with a real database (SQLAlchemy, Prisma, etc.).
- Implement **authentication** (JWT, OAuth2) and show how to pass tokens from the frontend.
- Deploy the app to a cloud platform (Render, Vercel, Heroku) and see the same flow over the internet.

---
*This document was created for learning purposes, illustrating the end‑to‑end flow of a FastAPI backend and a plain HTML/JS frontend.*