from __future__ import annotations

from PySide6.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget

from the_prof.app.launcher import AppContext


HELP_TEXT = """
# The Prof Help — Non-Technical Setup

## Why a run may look too fast
If no real language model is connected, The Prof does **not** pretend to have used one. It builds a conservative evidence scaffold and adds a **Model Generation Notice**. To get a richer report, connect at least one model provider.

## Easiest model options
1. **Ollama local, no account**
   - Install Ollama from https://ollama.com/download
   - Open Command Prompt / Terminal and run: `ollama pull llama3.2`
   - Start The Prof and keep Local-only enabled.

2. **Free cloud API key**
   - Open **Providers**.
   - Select Google AI Studio, Groq, OpenRouter, Mistral, Cerebras, NVIDIA NIM, GitHub Models, Hugging Face, Together, or another provider.
   - Click **Open Signup/Login for Selected**.
   - Create/copy an API key from the provider website.
   - Paste it into the matching key field in The Prof.
   - Tick **Allow online API providers** and untick **Local-only**.
   - Click **Save Providers and Keys**.
   - Click **Refresh/Test Availability**.

3. **FreeLLMAPI local router**
   - Advanced but powerful: install FreeLLMAPI, add many provider keys in its own dashboard, then add its unified key in The Prof.
   - In The Prof enable **FreeLLMAPI Local Router**.

## Adding any other API
If a service says it is **OpenAI-compatible**:
- Go to **Providers** → **Add Provider**.
- Enter its base URL, for example `https://provider.example.com/v1`.
- Enter the exact model name from the provider docs.
- Enter an environment/key name such as `MY_PROVIDER_API_KEY`.
- Save, paste the key, enable it, and test.

## Research/source APIs
For papers and facts, enable **Allow online source/API lookup** when creating a project. The Prof currently uses free no-key academic APIs including Semantic Scholar, OpenAlex, Crossref, PubMed, arXiv, and OpenCitations metadata. API Registry also lists many additional free/key/MCP/paid knowledge sources for future or manual integrations.

## Recommended first run
- Providers: Ollama local or Groq/Google/OpenRouter with a valid key.
- New Project: tick **Allow online source/API lookup**.
- Keep **Run gap analysis before drafting** on.
- Click **Create Project and Run**.

## Safety rules
- The Prof will not fabricate citations or data.
- If evidence is missing, it writes `Do not know.`
- Browser-login helpers must not bypass CAPTCHAs, paywalls, rate limits, or provider terms.
""".strip()


class HelpPage(QWidget):
    def __init__(self, context: AppContext) -> None:
        super().__init__()
        self.context = context
        layout = QVBoxLayout(self)
        title = QLabel("Help / Connect Models and APIs")
        title.setObjectName("TitleLabel")
        layout.addWidget(title)
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setMarkdown(HELP_TEXT)
        layout.addWidget(self.text, 1)
