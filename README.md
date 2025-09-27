# InsightNet

A global insight tool for local routing models. It offers both a CLI and an API, enabling flexible interaction.

## Getting Started

### Prerequisites
- Python 3.9+
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/)

### Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/zachathanasiadis/InsightNet.git
   cd InsightNet
   ```

2. **Install dependencies**
   ```sh
   poetry install
   ```

## Sample Files

The repository includes example files to help you get started:

- `sample_graphs/` – Contains example input graph JSON files for testing the CLI.
- `sample_requests/` – Contains example API request JSON files for testing the API.

## Usage (CLI)
**Run the CLI tool with:**

```sh
python -m insightnet \
  --input-json path/to/input.json \
  --current-state edge,node \
  --output path/to/output.csv
```

**Required Arguments:**
- `--input-json` (`-i`): Path to the input JSON file containing the routing model and graph data.
- `--current-state` (`-s`): The edge and node of the state to be queried, separated by a comma.
- `--output` (`-o`): Output file path with extension (`.csv`, `.json`, `.jsonl`, `.dot`).

**Required CLI Input JSON Fields:**
- `routing_model` *(string)*: The name of the routing model.
- `nodes` *(list of strings)*: List of node names.
- `edge_to_node_mapping` *(list)*: Each item specifies an edge and the nodes it connects:
  - `edge` *(int)*: Edge identifier.
  - `nodes` *(list of strings)*: Nodes connected by this edge.
- `routing_table` *(list)*: Each item specifies the routing rules for a node.

### Example
**Example Command:**
```sh
python -m insightnet -i sample_graphs/graph4.json -s 2,A -o results/output.jsonl
```
**Example Output (`results/output.jsonl`):**
```json
{"path": [[2, "A"], [null, "B"]], "alive_edges": [2], "failed_edges": [3]}
{"path": [[2, "A"], [2, "B"], [null, "A"]], "alive_edges": [2], "failed_edges": [1, 3]}
{"path": [[2, "A"], [3, "B"], [null, "C"]], "alive_edges": [2, 3], "failed_edges": [1]}
{"path": [[2, "A"], [3, "B"], [3, "C"], [null, "B"]], "alive_edges": [2, 3], "failed_edges": [1]}
{"path": [[2, "A"], [3, "B"], [3, "C"], [2, "B"], [null, "A"]], "alive_edges": [2, 3], "failed_edges": [1]}
```
## Usage (API)
**Run the API with Docker**
1. **Build the Docker image:**
   ```sh
   docker build -t insightnet-api .
   ```

2. **Run the API container:**
   ```sh
   docker run -p 8000:8000 insightnet-api
   ```

The API will be available at [http://localhost:8000](http://localhost:8000).


**Endpoint:**

- `POST /infer`


**Required Request Body Fields:**

- `routing_model` *(string)*: The name of the routing model.
- `nodes` *(list of strings)*: List of node names.
- `edge_to_node_mapping` *(list)*: Each item specifies an edge and the nodes it connects:
  - `edge` *(int)*: Edge identifier.
  - `nodes` *(list of strings)*: Nodes connected by this edge.
- `routing_table` *(list)*: Each item specifies the routing rules for a node.
- `current_state` *(string)*: State to be queried, formatted as `"edge,node"`.

### Example
**Example Request:**

```sh
curl -X POST "http://localhost:8000/infer" \
  -H "Content-Type: application/json" \
  -d @sample_requests/request1.json
```
**Example Response:**

```json
{
  "results": [
    {
      "path": [[1,"v1"],[null,"v2"]],
      "alive_edges": [1],
      "failed_edges": [2]
    },
    {
      "path": [[1,"v1"],[1,"v2"],[null,"v1"]],
      "alive_edges": [1],
      "failed_edges": [2]
    },
    {
      "path": [[1,"v1"],[2,"v2"],[null,"v3"]],
      "alive_edges": [1,2],
      "failed_edges": []
    },
    {
      "path": [[1,"v1"],[2,"v2"],[2,"v3"],[null,"v2"]],
      "alive_edges": [1,2],
      "failed_edges": []
    },
    {
      "path": [[1,"v1"],[2,"v2"],[2,"v3"],[1,"v2"],[null,"v1"]],
      "alive_edges": [1,2],
      "failed_edges": []
    }
  ]
}
```
## Authors

- **Zacharias Athanasiadis** ([Github](https://www.github.com/zachathanasiadis))


## Acknowledgements

- **Csaba Györgyi** ([Github](https://www.github.com/gycsaba96)) – Project advisor, for guidance and feedback throughout the development of InsightNet.
