from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
 select ?s1 as ?link, ( bif:search_excerpt ( bif:vector ( '35(t)', 'PZ' ) , ?o1 ) ) as ?content, ?sc, ?rank, ?g where 
  { 
    { 
      { 
        select ?s1, ( ?sc * 3e-1 ) as ?sc, ?o1, ( sql:rnk_scale ( <LONG::IRI_RANK> ( ?s1 ) ) ) as ?rank, ?g where 
        { 
          quad map virtrdf:DefaultQuadMap 
          { 
            graph ?g 
            { 
              ?s1 ?s1textp ?o1 .
              ?o1 bif:contains ' ( "35(t)" AND "PZ" ) ' option ( score ?sc ) .
              
            }
           }
         }
      }
     }
   }
  
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

#pprint(results)

for result in results["results"]["bindings"]:
    print("Result: " + result["link"]["value"] + "\t\tRank: " + result["rank"]["value"])
    sparql.setQuery("""
    
    select distinct ?desc
    where {
      <""" + result["link"]["value"] + """> dbpedia-owl:abstract ?desc
    }
      """)
    
    #select * where {
    #<http://dbpedia.org/resource/Panzer_35(t)>
    #?s ?p
    #}
    
    try:
      data = sparql.query().convert()
      for l in data["results"]["bindings"]:
	print l["desc"]["value"]
    except Exception, e:
      print"Can't retrieve data %s" % str(e)
