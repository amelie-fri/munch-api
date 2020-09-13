# Munch API

This project is creating an API for accessing the content of the textual works of Edvard Munch.
The API is provided as a service for the following project: [Munch Search](https://github.com/amelie-fri/munch_search)

## Getting Started

To get started, please get a copy of this repository on your local drive and make sure the necessary software is installed.  

### `docker-compose build`
This will build the `munch_api` docker image needed for the **Munch Search** Application.

### `docker-compose up`
To run the application as a separate service (for testing purposes).  

Two APIs are provided with this application:  
`http://localhost:5000/N`  
provides a list of all the files/parents found by the application.  

The response is a json object with one key: `data`. `data` is a array with filenames/parent e.g.   
{
    "data": [
        "MM_N3701.xml",
        "No-MM_N3700.xml"
    ]
} 

The following API is provided in order to retrieve the parsed data from the parent:  
`http://localhost:5000/N/<parentfilename.xml>`  

### Prerequisites
Docker necessary in order to use this project. Docker is available from:
https://www.docker.com/get-started

Python version 3.6 or above is needed and available from:  
https://www.python.org/downloads/  
The Python Package Index (PyPI) is included by default in python version 3.4 and above.  
execute the following command in the command line to install the additional Python libraries needed for the project:  
`pip install -r requirements.txt`  

### Preparing the data 

The project will parse and analyse data located in `./_data/N`  
The data is not a part of the repository and has to be aquired separately.  

In order to move all the relevant data from subfolders of `./_data/N` execute:
`python app/prepareData.py`  

In order to get an overview of the data, or for testing the application, run
`python app/analyseData.py`  
A progress bar will indicate the progress. 

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
**Amelie Fritsch** - https://github.com/amelie-fri

Project Link: https://github.com/your_username/repo_name

## Acknowledgments
- Maximilian Konzack [Parsing TEI XML documents with Python](https://komax.github.io/blog/text/python/xml/parsing_tei_xml_python/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [FlaskRESTful](https://flask-restful.readthedocs.io/en/latest/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://lxml.de/)
- [Docker](https://www.docker.com/)
