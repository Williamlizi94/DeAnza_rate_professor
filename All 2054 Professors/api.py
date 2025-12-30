"""
De Anza College Professors API
RESTful API for querying professor data from RateMyProfessors
"""

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
import os
import time

app = FastAPI(
    title="De Anza College Professors API",
    description="API for querying professor ratings and reviews from De Anza College",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Load data on startup
DATA_FILE = "rmp_deanza_all_professors.json"
professors_data = []


def load_data():
    """Load professor data from JSON file"""
    global professors_data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            professors_data = json.load(f)
        print(f"Loaded {len(professors_data)} professors from {DATA_FILE}")
    else:
        print(f"Warning: {DATA_FILE} not found. API will return empty results.")


@app.on_event("startup")
async def startup_event():
    load_data()


@app.post("/reload")
async def reload_data():
    """Reload professor data from JSON file (for updates)"""
    try:
        load_data()
        return {
            "status": "success",
            "message": f"Data reloaded successfully. {len(professors_data)} professors loaded.",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reloading data: {str(e)}")


@app.get("/")
async def root():
    """Serve the web interface"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {
        "message": "De Anza College Professors API",
        "version": "1.0.0",
        "endpoints": {
            "web_interface": "/",
            "api_docs": "/docs",
            "professors": "/professors",
            "professor_by_name": "/professors/name/{name}",
            "professor_by_department": "/professors/department/{department}",
            "search": "/search",
            "stats": "/stats"
        }
    }


@app.get("/professors")
async def get_professors(
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    limit: int = Query(20, ge=1, le=100, description="Number of results per page"),
    department: Optional[str] = Query(None, description="Filter by department"),
    min_rating: Optional[float] = Query(None, ge=0, le=5, description="Minimum average rating"),
    max_difficulty: Optional[float] = Query(None, ge=0, le=5, description="Maximum average difficulty"),
    format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")
):
    """
    Get all professors with optional filtering and pagination
    
    - **page**: Page number (starts from 1)
    - **limit**: Number of results per page (max 100)
    - **department**: Filter by department name
    - **min_rating**: Minimum average rating (0-5)
    - **max_difficulty**: Maximum average difficulty (0-5)
    """
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/professors.html"):
        return FileResponse("static/professors.html")
    filtered = professors_data.copy()
    
    # Apply filters
    if department:
        filtered = [p for p in filtered if p.get("Department", "").lower() == department.lower()]
    
    if min_rating is not None:
        filtered = [
            p for p in filtered
            if (rating := _get_float(p.get("Average_Rating"))) is not None
            and rating >= min_rating
        ]
    
    if max_difficulty is not None:
        filtered = [
            p for p in filtered
            if (difficulty := _get_float(p.get("Average_Difficulty"))) is not None
            and difficulty <= max_difficulty
        ]
    
    # Pagination
    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": paginated
    }


@app.get("/professors/name/{name}")
async def get_professor_by_name(
    name: str,
    format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")
):
    """
    Get professor(s) by name (case-insensitive partial match)
    
    - **name**: Professor's name (can be partial match)
    """
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/professors.html"):
        return FileResponse("static/professors.html")
    name_lower = name.lower()
    matches = [
        p for p in professors_data
        if name_lower in p.get("Full_Name", "").lower()
    ]
    
    if not matches:
        raise HTTPException(status_code=404, detail=f"Professor(s) with name '{name}' not found")
    
    return {
        "count": len(matches),
        "data": matches
    }


@app.get("/professors/department/{department}")
async def get_professors_by_department(
    department: str,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")
):
    """
    Get professors by department
    
    - **department**: Department name
    - **page**: Page number
    - **limit**: Results per page
    """
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/professors.html"):
        return FileResponse("static/professors.html")
    matches = [
        p for p in professors_data
        if department.lower() == p.get("Department", "").lower()
    ]
    
    if not matches:
        raise HTTPException(status_code=404, detail=f"No professors found in department '{department}'")
    
    # Pagination
    total = len(matches)
    start = (page - 1) * limit
    end = start + limit
    paginated = matches[start:end]
    
    return {
        "department": department,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": paginated
    }


@app.get("/search")
async def search_professors(
    q: str = Query(..., description="Search query (searches in name and department)"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")
):
    """
    Search professors by name or department
    
    - **q**: Search query
    - **page**: Page number
    - **limit**: Results per page
    """
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/professors.html"):
        return FileResponse("static/professors.html")
    query_lower = q.lower()
    matches = [
        p for p in professors_data
        if query_lower in p.get("Full_Name", "").lower()
        or query_lower in p.get("Department", "").lower()
    ]
    
    # Pagination
    total = len(matches)
    start = (page - 1) * limit
    end = start + limit
    paginated = matches[start:end]
    
    return {
        "query": q,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": paginated
    }


@app.get("/stats")
async def get_stats(format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")):
    """Get statistics about the professor database"""
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/stats.html"):
        return FileResponse("static/stats.html")
    
    if not professors_data:
        return {"message": "No data available"}
    
    departments = {}
    total_reviews = 0
    ratings = []
    difficulties = []
    
    for prof in professors_data:
        # Department stats (only count non-empty departments)
        dept = prof.get("Department")
        if dept:  # Only count non-empty departments
            departments[dept] = departments.get(dept, 0) + 1
        
        # Reviews count
        num_ratings = prof.get("Num_Ratings", 0)
        if isinstance(num_ratings, (int, float)):
            total_reviews += num_ratings
        
        # Rating stats
        rating = _get_float(prof.get("Average_Rating"))
        if rating is not None:
            ratings.append(rating)
        
        # Difficulty stats
        difficulty = _get_float(prof.get("Average_Difficulty"))
        if difficulty is not None:
            difficulties.append(difficulty)
    
    return {
        "total_professors": len(professors_data),
        "total_reviews": total_reviews,
        "departments": {
            "count": len(departments),
            "list": sorted(departments.keys())
        },
        "ratings": {
            "average": sum(ratings) / len(ratings) if ratings else 0,
            "min": min(ratings) if ratings else 0,
            "max": max(ratings) if ratings else 0
        },
        "difficulty": {
            "average": sum(difficulties) / len(difficulties) if difficulties else 0,
            "min": min(difficulties) if difficulties else 0,
            "max": max(difficulties) if difficulties else 0
        },
        "top_departments": sorted(
            departments.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
    }


@app.get("/departments")
async def get_departments(format: Optional[str] = Query(None, description="Response format: 'json' or 'html'")):
    """Get list of all departments"""
    # Return HTML if format is not explicitly 'json'
    if format != "json" and os.path.exists("static/departments.html"):
        return FileResponse("static/departments.html")
    
    departments = set()
    for prof in professors_data:
        dept = prof.get("Department")
        if dept:
            departments.add(dept)
    
    return {
        "count": len(departments),
        "departments": sorted(list(departments))
    }


def _get_float(value):
    """Convert value to float, return None if conversion fails"""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

