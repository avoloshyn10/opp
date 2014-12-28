Realizarea unei platforme care, pe baza informatiilor din DBpedia, wikipedia, forumuri de specialitate, sa modeleze si sa exploateze cunostiintele referitoare la unitatile militare, arme si tehnologii folosite in jocul OpenPanzer (http://openpanzer.net), generand o enciclopedie cu informatii detaliate. 

In joc exista peste 5000 de unitati militare, repartizate in 21 de categorii pentru cele 30 de tari disponibile in joc, participante in al doilea razboi mondial.
Ele sunt prezentate in jargon militar (eg PSW 222 [http://dbpedia.org/c/8IXQNV], Pz 35(t)a[http://dbpedia.org/c/8FJO57] )  ceea ce, pentru utilizatorul obisnuit, nu ofera nici o informatie istorica reala, diminuand contextul istoric al jocului.
Cu ajutorul informatiilor din dbpedia si alte surse putem oferi jucatorului suficienta informatie pentru a intelege mai bine capacitatile unitatilor.

Optional sistemul va pune la dispozitie o interfata publica pentru a completa sau adauga informatii despre unitatile existente.

Implementation concerns (informal):
- folosim direct entry-urile dbpedia, sau o copie a informatiilor?
- rdf-ul dbpedia sau propriul rdf pentru adaugarea de informatii suplimentare inexistente pe dbpedia? Probabil doar dbpedia pt inceput, apoi propriul rdf in versiunea 2


Packages:
sudo easy_install RDFLib
sudo easy_install SPARQLWrapper

MacOS:
sudo port install db51
sudo ln -sf /opt/local/include/db51/ /opt/local/lib/db51/include
sudo ln -sf /opt/local/lib/db51/ /opt/local/lib/db51/lib
sudo BERKELEYDB_DIR=/opt/local/lib/db51 ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future easy_install bsddb3


Introductory presentation at:
http://www.slideshare.net/nottorp/opp-archi
