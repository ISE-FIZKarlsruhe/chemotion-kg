# Chemotion-KG

**Chemotion Knowledge Graph (Chemotion-KG)** is a structured, FAIR-compliant graph database connecting chemical reactions, compounds, and metadata for AI-driven research and interoperability.

## Getting Started

For testing, you can run:

```shell
docker run -it -p 8000:8000 -e DEBUG=1 -e DATA_LOAD_PATHS=/data/ -e MOUNT=/chemotion-kg/ chemotion-kg
