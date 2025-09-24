Geospatial Chatbot is an AI-powered system designed to answer geospatial queries accurately. It integrates structured geospatial datasets with advanced reasoning algorithms, enabling users to retrieve insights such as flood risk zones, nearby infrastructure, terrain features, and other spatial information.

Table of Contents

1. Overview
2. Key Features
3. Architecture
4. Technologies and Tools
5. Installation and Setup
6. Usage
7. Project Structure
8. Contributing
9. License
10. Acknowledgements

Overview
The Geospatial Chatbot leverages structured geospatial data to answer complex spatial queries. By combining AI reasoning using Chain-of-Thought with rich geospatial datasets such as OpenStreetMap and Bhoonidhi, the system provides precise location-based insights, terrain analysis, and automated reasoning across multiple datasets. The project is modular, extensible, and easy to integrate into other geospatial platforms or applications.

Key Features

* Natural language query support allowing users to input questions in plain language.
* Structured data reasoning using AI-driven logic.
* Terrain analysis including elevation, slope, flow accumulation, and other attributes.
* Proximity queries to identify nearest highways, rivers, or infrastructure.
* Extensible framework for adding new datasets or reasoning logic.

Architecture
User Input (Query) -> Chatbot Agent -> Data Fetch and Processing Layer (OSM/Bhoonidhi datasets) -> AI Reasoning Engine (Chain-of-Thought Logic) -> Structured Output / Response

Flow

1. User inputs a geospatial question.
2. Chatbot parses the query and identifies required datasets.
3. Data is retrieved and processed.
4. AI reasoning engine synthesizes a response.
5. User receives a precise, actionable answer.

Technologies and Tools

* Python 3.x for backend and core logic.
* Pandas and GeoPandas for handling tabular and geospatial data.
* Rasterio and WhiteboxTools for Digital Elevation Model analysis.
* LangChain and LLM frameworks for AI reasoning.
* OpenStreetMap and Bhoonidhi geospatial datasets.

Installation and Setup

1. Clone the repository
   git clone [https://github.com/sanskar1104srivastava/geospatial\_chatbot.git](https://github.com/sanskar1104srivastava/geospatial_chatbot.git)
   cd geospatial\_chatbot

2. Set up a virtual environment
   python -m venv venv
   source venv/bin/activate (Windows: venv\Scripts\activate)

3. Install dependencies
   pip install -r requirements.txt

4. Run the chatbot
   python main.py

Usage
Once running, users can input queries such as:

* Where is the lowest flood risk area?
* Which highway is nearest to this location?
* Show terrain features for latitude 28.6139, longitude 77.2090

Expected Output
Structured responses providing spatial insights, calculated metrics, and references to the underlying geospatial data.

Project Structure
geospatial\_chatbot/
agent/ - Core chatbot logic and AI reasoning engine
tools/ - Utility scripts for preprocessing and analysis
config.py - Configuration settings
main.py - Entry point to launch chatbot
requirements.txt - Python dependencies
tempCodeRunnerFile.py - Temporary/test scripts

Contributing

1. Fork the repository.
2. Create a new branch: git checkout -b feature/YourFeature
3. Commit your changes: git commit -m "Add feature: description"
4. Push to your branch: git push origin feature/YourFeature
5. Open a Pull Request and describe your changes.



Acknowledgements
OpenStreetMap and Bhoonidhi for geospatial datasets. LangChain and other AI frameworks for reasoning support. WhiteboxTools and Rasterio for DEM and terrain analysis.
