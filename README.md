# Munch API

An API for accessing data regarding texts written by Edvard Munch.  
The API is provided as a service to the following project: [munch_search](https://github.com/amelie-fri/munch_search)

## Getting Started

To get started, please get a copy of this repository on your local drive and make sure the necessary software is installed.  

### `docker-compose build`
The command builds the `munch_api` docker image needed for the **munch_search** application.

### `docker-compose up`
Runs the application as a separate service (for testing purposes).  

Two APIs are provided.
The following URL leads to a list of all files/parents found by the application.
`http://localhost:5000/N`  

The response is a JSON object with one key: `data`. `data` is an array containing filenames/parents.
For example:
{
    "data": [
        "MM_N3701.xml",
        "No-MM_N3700.xml"
    ]
} 

The following URL is provided in order to retrieve the parsed data from the parent:  
`http://localhost:5000/N/<parentfilename.xml>`  

### Prerequisites
The installation of Docker is necessary for this project. Docker is available here:
https://www.docker.com/get-started 

### Preparing the data 

Data located in `./_data/N` will be parsed and analysed.
The data is not a part of the repository and has to be acquired separately.  

In order to move all the relevant data from subfolders of `./_data/N` execute:
`python app/prepareData.py`  

In order to get an overview of the data, or for testing the application, run
`python app/analyseData.py`  
A progress bar will indicate the progress. 

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Contact
**Amelie Fritsch** - https://github.com/amelie-fri

Project Link: https://github.com/amelie-fri/munch-api

## Acknowledgments
- Maximilian Konzack [Parsing TEI XML documents with Python](https://komax.github.io/blog/text/python/xml/parsing_tei_xml_python/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [FlaskRESTful](https://flask-restful.readthedocs.io/en/latest/)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)
- [lxml](https://lxml.de/)
- [Docker](https://www.docker.com/)
