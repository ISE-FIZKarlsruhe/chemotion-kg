## Competency Questions

This document contains competency questions for Chemotion-KG, along with corresponding SPARQL queries to explore the knowledge graph.

---

## General Questions with SPARQL Queries

### **CQ1: What are all the types of entities (concepts) in the Chemotion-KG?**
This query retrieves a distinct list of all entity types (concepts) present in the knowledge graph.

```sparql
SELECT DISTINCT ?Concept
WHERE {
  [] a ?Concept
}
LIMIT 999
```

---

### **CQ2: How many entities exist for each concept in the Chemotion-KG?**
This query counts the number of entities associated with each concept and orders them by frequency.

```sparql
SELECT ?Concept (COUNT(?entity) AS ?count)
WHERE {
  ?entity a ?Concept .
}
GROUP BY ?Concept
ORDER BY DESC(?count)
LIMIT 999
```

---

### **Explore More**
These queries allow users to analyze and navigate **Chemotion-KG** for **compounds, reactions, research contributions, and more**.

For additional queries or dataset access, visit:
👉 [SPARQL Endpoint](https://ditrare.ise.fiz-karlsruhe.de/chemotion-kg/sparql){:target="_blank"}

---

