import sys
from rdflib import Graph, Namespace

input_file = sys.argv[1]
output_file = sys.argv[2]

# Namespaces
SCHEMA = Namespace("http://schema.org/")
NFDICORE = Namespace("https://nfdi.fiz-karlsruhe.de/ontology/")
OBO = Namespace("http://purl.obolibrary.org/obo/")
chebi = Namespace("http://purl.obolibrary.org/obo/chebi/")
mwo = Namespace("http://purls.helmholtz-metadaten.de/mwo/")

# Load RDF graph
g = Graph()
g.parse(input_file, format="n3")

# Define SPARQL CONSTRUCT query
construct_query = f"""
PREFIX schema: <http://schema.org/>
PREFIX nfdicore: <https://nfdi.fiz-karlsruhe.de/ontology/>
PREFIX obo: <http://purl.obolibrary.org/obo/>
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
PREFIX chebi: <http://purl.obolibrary.org/obo/chebi/>
PREFIX mwo: <http://purls.helmholtz-metadaten.de/mwo/>

CONSTRUCT {{
  ?dataset a nfdicore:NFDI_0000009 ; # dataset
           nfdicore:NFDI_0001027 ?creator ;
           nfdicore:NFDI_0000191 ?publisher ;
           obo:IAO_0000235 ?descriptionNode ;
           nfdicore:NFDI_0001006 ?identifierNode ;
           nfdicore:NFDI_0000142 ?license ;
           nfdicore:NFDI_0000216 ?technique ;
           obo:IAO_0000235 ?nameNode ;
           obo:IAO_0000235 ?urlNode ;
           nfdicore:NFDI_0001023 ?study ; # is output of
           obo:BFO_0000178 ?catalog . # has continuant part
  
  ?technique a nfdicore:NFDI_0000215 ;
    rdfs:label ?techniqueName ;
    obo:IAO_0000118 ?techniqueAlternateName ;
    obo:IAO_0000235 ?techniqueurlNode ;
    nfdicore:NFDI_0001006 ?techniqueTermCodeNode ;
    obo:BFO_0000178 ?techniqueDefinedTermSet .
    
  ?techniqueurlNode a nfdicore:NFDI_0000223 ; # URL
		nfdicore:NFDI_0001008 ?techniqueurl .
  
  ?techniqueTermCodeNode a nfdicore:NFDI_0000015 ; #identifier
		nfdicore:NFDI_0001007 ?techniqueTermCode .
  
  ?techniqueDefinedTermSet a obo:IAO_0000027 . #data item
           
  ?creator a nfdicore:NFDI_0000004 ;  #person
      obo:IAO_0000235 ?givenNameNode ;
      obo:IAO_0000235 ?familyNameNode ;
      rdfs:label ?fullName ;
      nfdicore:NFDI_0001006 ?orcidNode ;
      obo:BFO_0000056 ?affiliationProcess . #participates in process

  ?givenNameNode  a obo:IAO_0020016 ; #name
            nfdicore:NFDI_0001007 ?givenName . #has value
            
  ?familyNameNode  a obo:IAO_0020017 ; #familyname
            nfdicore:NFDI_0001007 ?familyName . #has value
  
  ?orcidNode a obo:IAO_0000708 ; #orcid
            nfdicore:NFDI_0001008 ?orcidURI ; #uri of orcid
            rdfs:label ?orcid . 
            
  ?affiliationProcess  a nfdicore:NFDI_0000115 ; #contributing process
            obo:BFO_0000057 ?agent ; #has participant
            obo:BFO_0000055 ?role . #realizes role
            
  ?agent a nfdicore:NFDI_0000102 ; #agent
            obo:BFO_0000196 ?role . #bearer of Role
            
  ?role a nfdicore:NFDI_0000118 ; #contributor role
            obo:BFO_0000054 ?affiliationProcess ; #has realization
            obo:BFO_0000197 ?affiliation . #inheres in
  
  ?affiliation  a nfdicore:NFDI_0000003 ; #organization
            rdfs:label ?orgName . #orgName
  
  ?publisher a nfdicore:NFDI_0000003 ; #organization
            obo:IAO_0000235 ?publisherUrlNode ;
            rdfs:label ?publisherName . #publisherName
                
  ?identifierNode  a nfdicore:NFDI_0000015 ; #identifier
            nfdicore:NFDI_0001007 ?identifier . #has value
            
  ?descriptionNode a nfdicore:NFDI_0001018 ; #description
            nfdicore:NFDI_0001007 ?description . #has value
  
  ?nameNode a nfdicore:NFDI_0001019 ; #title
            nfdicore:NFDI_0001007 ?name . #has value
            
  ?urlNode a nfdicore:NFDI_0000223 ; #url
            nfdicore:NFDI_0001008 ?url . #has url
  
  ?publisherUrlNode a nfdicore:NFDI_0000223 ; #url
            nfdicore:NFDI_0001008 ?publisherUrl . #has url
             
  ?catalog a obo:IAO_0000578 . #centrally registered identifier

  ?study a obo:BFO_0000015 ;
            nfdicore:NFDI_0000207 ?studyProfile ; #has standard
            nfdicore:NFDI_0001027 ?studyCreator ; #has standard
            obo:BFO_0000178 ?publishingProcess . # has continuant part
  
  ?publishingProcess a nfdicore:NFDI_0000014 ; #publishing process
            obo:BFO_0000199 ?publishingDateRegion . #occupies temporal region
  
  ?publishingDateRegion a obo:BFO_0000008 ;
            nfdicore:NFDI_0001007 ?datePublished . #has value
  
  ?studyCreator a nfdicore:NFDI_0000004 ;  #person
      obo:IAO_0000235 ?studyCreatorgivenNameNode ;
      obo:IAO_0000235 ?studyCreatorfamilyNameNode ;
      rdfs:label ?studyCreatorfullName ;
      nfdicore:NFDI_0001006 ?studyCreatororcidNode ;
      obo:BFO_0000056 ?studyCreatoraffiliationProcess . #participates in process

          
  ?studyCreatorgivenNameNode  a obo:IAO_0020016 ; #name
            nfdicore:NFDI_0001007 ?studyCreatorgivenName . #has value
            
  ?studyCreatorfamilyNameNode  a obo:IAO_0020017 ; #familyname
            nfdicore:NFDI_0001007 ?studyCreatorfamilyName . #has value
  
  ?studyCreatororcidNode a obo:IAO_0000708 ; #orcid
            nfdicore:NFDI_0001008 ?studyCreatororcidURI ; #uri of orcid
            rdfs:label ?studyCreatororcid . 
            
  ?studyCreatoraffiliationProcess  a nfdicore:NFDI_0000115 ; #contributing process
            obo:BFO_0000057 ?studyCreatoragent ; #has participant
            obo:BFO_0000055 ?studyCreatorrole . #realizes role
            
  ?studyCreatoragent a nfdicore:NFDI_0000102 ; #agent
            obo:BFO_0000196 ?studyCreatorrole . #bearer of Role
            
  ?studyCreatorrole a nfdicore:NFDI_0000118 ; #contributor role
            obo:BFO_0000054 ?studyCreatoraffiliationProcess ; #has realization
            obo:BFO_0000197 ?studyCreatoraffiliation . #inheres in
  
  ?studyCreatoraffiliation  a nfdicore:NFDI_0000003 ; #organization
            rdfs:label ?studyCreatororgName . #orgName
  
  
  ?chemicalSubstance a obo:CHEBI_59999 ; # generic chemical entity
                  rdfs:label ?name ;
                  obo:IAO_0000118 ?inchiNode ;
                  obo:IAO_0000235 ?chemicalurlNode ;
                  nfdicore:NFDI_0001023 ?study ; #part of study
                  nfdicore:NFDI_0001006 ?chemicalidentifierNode ;
                  obo:IAO_0000219 ?imageNode ;
                  obo:BFO_0000129 ?chemicalpartEntity .

  ?inchiNode a obo:IAO_0000028 ;  # textual definition
              rdfs:label ?inchi .

  ?chemicalurlNode a nfdicore:NFDI_0000223 ; # URL
            nfdicore:NFDI_0001008 ?chemicalurl .

  ?chemicalidentifierNode a nfdicore:NFDI_0000015 ; # identifier
            nfdicore:NFDI_0001007 ?chemicalidentifier .
  
  ?imageNode a obo:IAO_0000308 ; #figure
            nfdicore:NFDI_0001008 ?image .
    
  ?chemicalpartEntity a obo:CHEBI_23367 ; # molecular entity
         rdfs:label ?chemicalpartEntityname ;
         obo:IAO_0000235 ?chemicalpartEntitynameiupacNameNode ;
         chebi:inchi ?chemicalpartEntitynameinChI ;
         chebi:inchikey ?chemicalpartEntitynameinChIKey ;
         chebi:smiles ?chemicalpartEntitynamesmiles ;
         chebi:formula ?molecularFormula ;
         obo:BFO_0000196 ?Weight .

  ?chemicalpartEntitynameiupacNameNode a nfdicore:NFDI_0000015 ; # identifier
         nfdicore:NFDI_0001007 ?chemicalpartEntitynameiupacName . #has value
         
  ?Weight a obo:BFO_0000019 ; #quality
    obo:IAO_0000221 ?molecularWeightDatum . # is quality measurement of
  
  ?molecularWeightDatum a obo:IAO_0000109 ; # measurement datum
         mwo:MWO_0001119 ?molecularWeightunitNode ;
         nfdicore:NFDI_0001007 ?molecularWeightvalue .
  
  ?molecularWeightunitNode a obo:IAO_0000003 ; # measurement unit label
         nfdicore:NFDI_0001007 ?molecularWeightunit .
}}

WHERE {{
  ?dataset a schema:Dataset ;
      schema:creator ?creator ;
      schema:publisher ?publisher ;
      schema:description ?description ;
      schema:identifier ?identifier ;
      schema:license ?license ;
      schema:measurementTechnique ?technique ;
      schema:name ?name ;
      schema:url ?url ;
      schema:includedInDataCatalog ?catalog ;
      schema:isPartOf ?study .
  
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?description))) AS ?descriptionNode)
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?identifier))) AS ?identifierNode)
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?name))) AS ?nameNode)
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?url))) AS ?urlNode)

  OPTIONAL {{ 
  ?technique schema:name ?techniqueName ;
    schema:inDefinedTermSet ?techniqueDefinedTermSet ;
    schema:alternateName ?techniqueAlternateName ;
    schema:url ?techniqueurl ;
    schema:termCode ?techniqueTermCode .
  
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?techniqueurl))) AS ?techniqueurlNode)
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?techniqueTermCode))) AS ?techniqueTermCodeNode)
  }}
  
  OPTIONAL {{ 
  ?techniqueDefinedTermSet schema:name ?techniqueDefinedTermSetName .
  }}
  
  OPTIONAL {{ 
  ?publisher a schema:Organization ;
      schema:name ?publisherName ;
      schema:url ?publisherUrl .
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?publisherUrl))) AS ?publisherUrlNode)
  }}
  
  OPTIONAL {{ 
  ?creator a schema:Person ;
      schema:givenName ?givenName ;
      schema:familyName ?familyName ;
      schema:name ?fullName .
    
    OPTIONAL {{
        ?creator schema:identifier ?orcid .
        FILTER(REGEX(STR(?orcid), "^0000-\\\\d{{4}}-\\\\d{{4}}-\\\\d{{3}}[\\\\dX]$"))
        BIND(IRI(CONCAT("https://orcid.org/", STR(?orcid))) AS ?orcidURI)
        BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?orcid))) AS ?orcidNode)

        
      }}
      BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?givenName))) AS ?givenNameNode)
      BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?familyName))) AS ?familyNameNode)
  
  }}
  
  OPTIONAL {{
        ?creator schema:affiliation ?affiliation .
        ?affiliation a schema:Organization ;
            schema:name ?orgName .
      
        BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?orgName))) AS ?affiliationProcess)
        BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?orgName))) AS ?agent)
        BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?orgName))) AS ?role)
    }}
 
  
  OPTIONAL {{
  ?study a schema:Study ;
      dcterms:conformsTo ?studyProfile ;
      schema:about ?chemicalSubstance ;
      schema:creator ?studyCreator ;
      schema:dateCreated ?dateCreated ;
      schema:datePublished ?datePublished ;
      schema:publisher ?publisher .
  
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?datePublished))) AS ?publishingProcess)
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?datePublished))) AS ?publishingDateRegion)
  }}
  
  OPTIONAL {{ 
    ?studyCreator a schema:Person ;
      schema:givenName ?studyCreatorgivenName ;
      schema:familyName ?studyCreatorfamilyName ;
      schema:name ?studyCreatorfullName .
      
    OPTIONAL {{ 
      ?studyCreator schema:identifier ?studyCreatororcid .
      FILTER(REGEX(STR(?studyCreatororcid), "^0000-\\\\d{{4}}-\\\\d{{4}}-\\\\d{{3}}[\\\\dX]$"))
      BIND(IRI(CONCAT("https://orcid.org/", STR(?studyCreatororcid))) AS ?studyCreatororcidURI)

      BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatororcid))) AS ?studyCreatororcidNode)
    }}
    
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatorgiven))) AS ?studyCreatorgivenNameNode)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatorfamily))) AS ?studyCreatorfamilyNameNode)
  }}
  
  OPTIONAL {{
    ?studyCreator schema:affiliation ?studyCreatoraffiliation .
    ?studyCreatoraffiliation a schema:Organization ;
      schema:name ?studyCreatororgName .
      
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatororgName))) AS ?studyCreatoraffiliationProcess)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatororgName))) AS ?studyCreatoragent)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?studyCreatororgName))) AS ?studyCreatorrole)
  }}  

  OPTIONAL {{
    ?chemicalSubstance a schema:ChemicalSubstance ;
      schema:name ?name ;
      schema:alternateName ?inchi ;
      schema:identifier ?chemicalidentifier ;
      schema:url ?chemicalurl ;
      schema:image ?image ;
      schema:hasBioChemEntityPart ?chemicalpartEntity ;
      schema:isPartOf ?study .
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?inchi))) AS ?inchiNode)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?chemicalurl))) AS ?chemicalurlNode)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?chemicalidentifier))) AS ?chemicalidentifierNode)
    BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?image))) AS ?imageNode)
  }}
  
  OPTIONAL {{
    ?chemicalpartEntity a schema:MolecularEntity ;
      schema:name ?chemicalpartEntityname ;
      schema:inChI ?chemicalpartEntitynameinChI ;
      schema:inChIKey ?chemicalpartEntitynameinChIKey ;
      schema:iupacName ?chemicalpartEntitynameiupacName ;
      schema:smiles ?chemicalpartEntitynamesmiles ;
      schema:molecularWeight ?molecularWeight ;
      schema:molecularFormula ?molecularFormula .
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?chemicalpartEntitynameiupacName))) AS ?chemicalpartEntitynameiupacNameNode)
  }}
  
  OPTIONAL {{
  ?molecularWeight a schema:QuantitativeValue ; 
        schema:unitCode ?molecularWeightunit ;
        schema:value ?molecularWeightvalue .
  BIND(IRI(CONCAT("https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/nodes/", ENCODE_FOR_URI(?molecularWeightunit))) AS ?molecularWeightunitNode)
  }}
  
}}

"""    

# Run the transformation
converted_graph = g.query(construct_query).graph

# Bind namespaces
converted_graph.bind("nfdicore", NFDICORE)
converted_graph.bind("obo", OBO)
converted_graph.bind("chebi", chebi)
converted_graph.bind("mwo", mwo)

# Save the result
converted_graph.serialize(destination=output_file, format="n3")
