# RAG Support Agent By Kshitij Pathak

A RAG-based AI support agent that can handle billing, account, technical issues, and complaints.

## Setup

### 1. Environment Variables

The application requires environment variables to be configured. Copy the `env_template.txt` file to `.env` and fill in your values:

```bash
cp env_template.txt .env
```

Then edit the `.env` file with your actual values:

- **OPENAI_API_KEY**: Your OpenAI API key (required)
- **VECTOR_BACKEND**: Choose between `faiss`, `qdrant`, or `pgvector` (default: `faiss`)

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### Command Line Interface
```bash
python main.py
```

#### Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```

## Usage

The agent can handle various types of support queries:
- Billing issues
- Account changes
- Technical problems
- Complaints

## Architecture

- **src/config.py**: Configuration and environment variables
- **src/graph.py**: Main RAG processing logic
- **src/kb_loader.py**: Knowledge base loading
- **src/vector_store.py**: Vector database operations
- **src/nodes.py**: Processing nodes
- **src/prompts.py**: Prompt templates
