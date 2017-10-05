
-------------
Human PPI API
-------------

Overview
--------
The human_ppi API allows the user to import data from the
ConsensusPathDB-human database and serve them through a web API based
on the biothings framework.

Installation
------------

( The Following instructions were adapted from the
BioThings SDK Single Source tutorial - http://docs.biothings.io/en/latest/doc/single_source_tutorial.html )

1.  Install Python 3.5 or higher


2.  Install the Biothings SDK

pip install biothings


3.  Install ElasticSearch locally

BioThings APIs currently serve data from an Elasticsearch index, so Elasticsearch is a requirement.
Install Elasticsearch 2.4 either directly, or as a docker container.


4.  Down the source repository to an appropriate location and start the server.  You must run the web server
from inside of the <human_ppi_location>/src directory for the server to run properly.

cd <human_ppi_location>/src
pip install -r ../requirements_web.txt
python www/index.py --debug --port=8001


5.  Index the ConsensusPathDB_human_PPI file in ElasticSearch using the provided import script.  First you have
to download the data file and place it in an appropriate location (probably in the project directory).

Download the ConsensusPathDB_human_PPI data file and unzip it.
http://consensuspathdb.org/
http://cpdb.molgen.mpg.de/download/ConsensusPathDB_human_PPI.gz

cd <human_ppi_location>/src
python dataload/build_index.py <path_to_file>/ConsensusPathDB_human_PPI>