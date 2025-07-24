# --- FILE: tools/overpass_tool.py ---

import json
import time
import requests
import pandas as pd
from langchain.tools import tool
from pydantic import BaseModel, Field
from typing import Optional

# Make sure you have a config.py file or replace this with your actual URL
# from config import OVERPASS_API_URL
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"


# --- Tool 1: For searching within an entire city (MODIFIED) ---
class CityWideSearchInput(BaseModel):
    """Input schema for searching amenities across an entire city or district."""
    city_or_district: str = Field(description="The city or district to search within, e.g., 'Gorakhpur' or 'Delhi'.")
    amenity_type: Optional[str] = Field(default=None, description="The type of amenity to search for, e.g., 'hospital', 'cafe'. This is optional; omit it for a general search of all amenities.")

@tool("city_wide_amenity_search", args_schema=CityWideSearchInput)
def find_amenities_in_city(city_or_district: str, amenity_type: Optional[str] = None) -> str:
    """
    Use this tool to find amenities within an entire city or district.
    If the user provides a specific amenity_type (e.g., 'hospital'), it will search for that type.
    If the amenity_type is NOT provided, it will perform a general search for all available amenities in that city.
    """
    # First, find the bounding box for the specified city
    for level in ["8", "7", "6", "5"]:
        query_city_bounds = f'[out:json][timeout:30]; relation["name"="{city_or_district}"]["admin_level"="{level}"]; out bb;'
        try:
            response = requests.post(OVERPASS_API_URL, data={'data': query_city_bounds})
            response.raise_for_status()
            elements = response.json().get("elements", [])
            if len(elements) > 1:
                names = list(set([el.get("tags", {}).get("name", city_or_district) for el in elements]))
                return f"Error: Ambiguous city name. Found multiple locations for '{city_or_district}'. Please ask the user to be more specific. Did they mean one of: {', '.join(names)}?"
            if len(elements) == 1:
                bounds = elements[0]["bounds"]
                bbox = (bounds["minlat"], bounds["minlon"], bounds["maxlat"], bounds["maxlon"])
                break
        except requests.RequestException as e:
            return f"Network error while finding city: {e}"
        time.sleep(1) # Be nice to the API
    else:
        return f"Error: Could not find a bounding box for the city '{city_or_district}'."

    min_lat, min_lon, max_lat, max_lon = bbox

    # Second, build the query for amenities dynamically
    if amenity_type:
        # If amenity is specified, search for that specific key-value pair.
        amenity_filter = f'["amenity"="{amenity_type}"]'
        search_description = f"'{amenity_type}' facilities"
    else:
        # If amenity is NOT specified, search for any node/way that simply has an "amenity" tag.
        amenity_filter = '["amenity"]'
        search_description = "amenities"

    query_amenities = f'[out:json][timeout:90];(node{amenity_filter}({min_lat},{min_lon},{max_lat},{max_lon});way{amenity_filter}({min_lat},{min_lon},{max_lat},{max_lon}););out center;'
    
    try:
        response_amenities = requests.post(OVERPASS_API_URL, data={'data': query_amenities})
        response_amenities.raise_for_status()
        elements = response_amenities.json().get("elements", [])
    except requests.RequestException as e:
        return f"Network error while searching for amenities: {e}"

    if not elements:
        return f"Success: Found the city '{city_or_district}', but no {search_description} were found inside its boundaries."

    # Process the results into a clean DataFrame
    df = pd.json_normalize(elements)
    # Extract name and amenity type for better results, then drop unnamed locations
    df['name'] = df.get('tags.name')
    df['amenity'] = df.get('tags.amenity')
    df = df[['name', 'amenity']].dropna(subset=['name'])

    # Return a JSON string with the search parameters and the results
    return json.dumps({
        "search_city": city_or_district,
        "amenity_type_searched": amenity_type or "all",
        "results": df.to_dict('records')
    })


# --- Tool 2: For searching near a specific point (UNCHANGED) ---
class PointOfInterestSearchInput(BaseModel):
    """Input schema for searching amenities near a specific point of interest."""
    point_of_interest: str = Field(description="The specific landmark or building to search near, e.g., 'Eiffel Tower'.")
    amenity_type: str = Field(description="The type of amenity to search for, e.g., 'hospital', 'cafe'.")

@tool("point_of_interest_amenity_search", args_schema=PointOfInterestSearchInput)
def find_amenities_near_point(point_of_interest: str, amenity_type: str) -> str:
    """Use this tool ONLY when a user asks to find something near a specific named landmark or building (NOT a whole city)."""
    # First, find the coordinates of the point of interest
    query_coords = f'[out:json][timeout:30]; nwr["name"="{point_of_interest}"]; out center;'
    try:
        response_coords = requests.post(OVERPASS_API_URL, data={'data': query_coords})
        response_coords.raise_for_status()
        elements = response_coords.json().get("elements", [])
    except requests.RequestException as e:
        return f"Network error while finding point of interest: {e}"

    if not elements:
        return f"Error: Could not find a location named '{point_of_interest}'."
    
    # Handle different geometry types from Overpass
    element = elements[0]
    center = element.get('center', {})
    lat, lon = center.get('lat'), center.get('lon')
    if not lat:
        lat, lon = element.get('lat'), element.get('lon')

    if not lat or not lon:
        return f"Error: Found '{point_of_interest}' but could not determine its exact coordinates."

    # Second, search for amenities around that point
    query_amenities = f'[out:json][timeout:60]; node(around:2000,{lat},{lon})["amenity"="{amenity_type}"]; out body;'
    try:
        response_amenities = requests.post(OVERPASS_API_URL, data={'data': query_amenities})
        response_amenities.raise_for_status()
        elements = response_amenities.json().get("elements", [])
    except requests.RequestException as e:
        return f"Network error while searching for amenities near point: {e}"

    if not elements:
        return f"Success: Found '{point_of_interest}', but no '{amenity_type}' facilities were found within a 2km radius."

    # Process and return the results
    df = pd.json_normalize(elements).rename(columns={'tags.name': 'name'}).filter(items=['name']).dropna()
    return json.dumps({
        "search_poi": point_of_interest,
        "amenity_type_searched": amenity_type,
        "results": df.to_dict('records')
    })