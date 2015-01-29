#OPP (Open Panzer Pedia)
Project for InfoIasi Master Studies @ [WADE] (http://thor.info.uaic.ro/~busaco/teach/courses/wade/)

##Description
Realizarea unei platforme care, pe baza informatiilor din DBpedia, wikipedia, forumuri de specialitate, sa modeleze si sa exploateze cunostiintele referitoare la unitatile militare,
arme si tehnologii folosite in jocul [OpenPanzer] (http://openpanzer.net), generand o enciclopedie cu informatii detaliate.

In joc exista peste 5000 de unitati militare, repartizate in 21 de categorii pentru cele 30 de tari disponibile in joc, participante in al doilea razboi mondial.
Ele sunt prezentate in jargon militar (eg [PSW 222] (http://dbpedia.org/c/8IXQNV), [Pz 35(t)] (http://dbpedia.org/c/8FJO57) )  ceea ce, pentru utilizatorul obisnuit,
nu ofera nici o informatie istorica reala, diminuand contextul istoric al jocului.
Cu ajutorul informatiilor din dbpedia si alte surse putem oferi jucatorului suficienta informatie pentru a intelege mai bine capacitatile unitatilor.

Optional sistemul va pune la dispozitie o interfata publica pentru a completa sau adauga informatii despre unitatile existente.

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
    eureka3511:oppedia-rdf torp$ db51_verify __db.001 
    db51_verify: Lock table is out of available locker entries
    Segmentation fault: 11

This crashes, but it does indeed lose all the locks :) 
With enough time at hand:

    db5.3_deadlock -a m -t 1


##Documentation:
[Rest Client Guide] (http://nicupavel.github.io/opp/)

[Video] (https://www.youtube.com/watch?v=idAuOLPRvMs)

[SlideShare] (http://www.slideshare.net/nottorp/opp-archi)

##Current issues:
- Looking for units with DBpedia queries doesn't work very well as most of the unit name/designations are found in wikipedia
text below table of content which isn't scraped by dbpedia. Beside that building a better text regex it's limited by SPARQL functionality

- The workaround for DBpedia queries is to use Google search and extract wikipedia.org pages. This still needs improvement for text searched ex:
    - Some artillery pieces will benefit from expanding 100mm M10/42 to 100mm M10 1942
    - Some Flak pieces will benefit from expanding FlaKPz to Flak Panzer and in general Pz to be expanded to Panzer
    - Infantry like 40 Infantry will benefit from removing the year number in front
    - Some of the wikipedia pages found by Google aren't found in dbpedia.org
    - Google queries results are limited

- RDFLib has an issue when retrieving all results from a resource stored locally, filtered by language
- Unicode issues when passing links from google results to dbpedia sparql queries


##Running
    cd src
    python ./restServer.py &
    python ./opp.py

