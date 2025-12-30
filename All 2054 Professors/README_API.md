# De Anza College Professors API

RESTful API for querying professor ratings and reviews from De Anza College.

## Installation

1. Install dependencies:
```bash
pip install -r requirements_api.txt
```

## Running the API

### Development Server
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Interactive API docs (Swagger)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### 1. Root
- **GET** `/`
- Returns API information and available endpoints

### 2. Get All Professors
- **GET** `/professors`
- Query parameters:
  - `page` (int, default=1): Page number
  - `limit` (int, default=20, max=100): Results per page
  - `department` (string, optional): Filter by department
  - `min_rating` (float, optional): Minimum average rating (0-5)
  - `max_difficulty` (float, optional): Maximum average difficulty (0-5)

**Example:**
```
GET /professors?page=1&limit=10&department=History&min_rating=4.0
```

### 3. Get Professor by Name
- **GET** `/professors/name/{name}`
- Case-insensitive partial match search

**Example:**
```
GET /professors/name/Smith
```

### 4. Get Professors by Department
- **GET** `/professors/department/{department}`
- Query parameters:
  - `page` (int, default=1)
  - `limit` (int, default=20)

**Example:**
```
GET /professors/department/Computer Science?page=1&limit=10
```

### 5. Search Professors
- **GET** `/search?q={query}`
- Searches in both name and department
- Query parameters:
  - `q` (required): Search query
  - `page` (int, default=1)
  - `limit` (int, default=20)

**Example:**
```
GET /search?q=Math&page=1&limit=20
```

### 6. Get Statistics
- **GET** `/stats`
- Returns database statistics including:
  - Total professors
  - Total reviews
  - Department list
  - Rating statistics
  - Difficulty statistics
  - Top departments

### 7. Get All Departments
- **GET** `/departments`
- Returns list of all unique departments

## Example Responses

### Get Professors Response
```json
{
  "total": 1998,
  "page": 1,
  "limit": 20,
  "total_pages": 100,
  "data": [
    {
      "Full_Name": "Carol Cini",
      "Department": "History",
      "Average_Rating": "4.00",
      "Num_Ratings": 734,
      "Average_Difficulty": "2.90",
      "Would_Take_Again_Percent": "71.75",
      "Latest_Reviews": [...]
    }
  ]
}
```

## Error Handling

The API returns standard HTTP status codes:
- `200 OK`: Success
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

## Notes

- The API loads data from `rmp_deanza_all_professors.json` on startup
- Make sure the JSON file exists in the same directory as `api.py`
- The API supports CORS and can be used from web applications


