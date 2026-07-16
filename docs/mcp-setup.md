# MCP Setup — AgroManch Knowledge Base in Claude Code / claude.ai

`notebooklm-py` ships an **MCP server**, so once your AgroManch knowledge base
is indexed you can query the verified retrieval layer directly from Claude Code,
Claude Desktop, or (via a tunnel) claude.ai and ChatGPT.

> Architecture note: in AgroManch, NotebookLM is the **retrieval** layer and
> **Gemini** is the generation engine (see [architecture.md](architecture.md)).
> The MCP server is the quickest way to explore what the knowledge base contains
> and to draft content interactively; the production factory runs Gemini over the
> retrieved context via the Python services in `src/agromanch_ai/`.

## 1. Install and authenticate

```bash
uv tool install "notebooklm-py[browser]"   # or: pipx install "notebooklm-py[browser]"
notebooklm login                            # one-time Google sign-in
notebooklm auth check --test                # verify
```

Index the knowledge base once so the notebook has content:

```bash
python scripts/index_knowledge.py
export AGROMANCH_NOTEBOOK_ID=<id printed by the script>
```

## 2. Install the agent skill / MCP server

```bash
notebooklm skill install
# or, via the open skills ecosystem:
npx skills add teng-lin/notebooklm-py
```

This registers the NotebookLM MCP server (local **stdio** transport). For
access from claude.ai / ChatGPT, the project also supports self-hosted remote
deployment behind a Cloudflare or Tailscale tunnel — see the upstream
`notebooklm-py` documentation for the remote setup.

## 3. Point it at the AgroManch notebook

With `AGROMANCH_NOTEBOOK_ID` (or the notebook name **"AgroManch Knowledge
Base"**) set, the MCP tools operate on your indexed agricultural knowledge base.

## 4. Example prompts

Ask questions grounded in the knowledge base:

- *"Explain Fall Armyworm in Hindi for a maize farmer."*
- *"Explain Bacterial Leaf Blight in rice and how to manage it."*
- *"Summarize the ICAR document on wheat nutrient management."*
- *"Recommend the pesticide dose for stem borer in rice from the label documents."*
- *"Explain pesticide dosage and safety for spraying at flowering."*
- *"Create a crop advisory for cotton at flowering with heavy rain expected."*
- *"Which government schemes is a 1.2 ha smallholder in Bihar eligible for?"*

Generate content directly:

- *"Generate an Instagram carousel about drip irrigation benefits."*
- *"Create a WhatsApp farmer message about safe pesticide spraying."*
- *"Generate a YouTube Shorts script on Fall Armyworm control in maize."*
- *"Generate a farmer FAQ about soil testing."*
- *"Write a farmer-friendly blog outline on integrated pest management."*

Every answer is grounded in the indexed documents and returns source
citations — surface them so advice stays auditable.

## 5. When to use the Python API instead

The MCP server is ideal for interactive/agent use. For batch jobs, scheduled
content pipelines, or embedding in the AgroManch backend, call the services in
`src/agromanch_ai/` directly (see [architecture.md](architecture.md) and the
`examples/` scripts).
