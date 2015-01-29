#OPP (Open Panzer Pedia)
Project for InfoIasi Master Studies @ [WADE] (http://thor.info.uaic.ro/~busaco/teach/courses/wade/)

##Description
Building a platform that will pull military unit, weapon and technology information out of DBPedia, wikipedia and specific forums for use as an informative encyclopedia inside the [OpenPanzer] (http://openpanzer.net) game.

The game features over 5000 military units that took part in World War II, divided in 21 categories over the 30 countries available in the game. They are identified by their military name (eg [PSW 222] (http://dbpedia.org/c/8IXQNV), [Pz 35(t)] (http://dbpedia.org/c/8FJO57) ). For the average player, this offers no real information, diminishing the historical context of the game. Using the information pulled from dbpedia and other sources we can provide the player with enough information to understand the unit abilities better.

The system provides a simple REST interface with a built in human usable client to improve the automatically scraped information.

## Technical details
We are using the full DBpedia ontology and pulling RDF resources that match our crieria (mainly the rdf:type dbpedia-owl:Weapon flag) in our internal database.
The RDF is parsed and unrelated triplets are not exported, while the relevant information is exported as static JSON for use in the openpanzer game.


##Packages:
    sudo easy_install RDFLib
    sudo easy_install SPARQLWrapper
    sudo easy_install pony
    sudo easy_install bottle
    sudo easy_install beautifulsoup

##MacOS:
    sudo port install db51
    sudo ln -sf /opt/local/include/db51/ /opt/local/lib/db51/include
    sudo ln -sf /opt/local/lib/db51/ /opt/local/lib/db51/lib
    sudo BERKELEYDB_DIR=/opt/local/lib/db51 ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future easy_install bsddb3

##Fix BerkeleyDB out of lock entries
With enough time at hand:

    db5.3_deadlock -a m -t 1


##Documentation:
[Rest Client Guide] (http://nicupavel.github.io/opp/)

[Video] (https://www.youtube.com/watch?v=idAuOLPRvMs)

[Google Docs presentation] (https://docs.google.com/presentation/d/189sFgbS13-jruEzU8nbts4JLGCGxr3YpJLgk7R592f8/edit?usp=sharing)

##Current issues:
- Looking for units with DBpedia queries doesn't work very well as most of the unit name/designations are found in wikipedia text below table of content which isn't scraped by dbpedia.
- Unicode issues when passing links from google results to dbpedia sparql queries


##Running
    cd src
    python ./restServer.py &
