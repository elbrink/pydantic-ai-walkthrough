# Pydantic AI walkthrough

## Using this repo

- Install `uv` if you haven't done so already ([docs](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer))
- Run `uv sync` to create a virtiual environment with all the project dependencies
- Create a `.env` file with API keys for the model(s) that you want to use (see [pydanticAI docs](https://ai.pydantic.dev/models/)), that should look like this

```shell
ANTHROPIC_API_KEY=SoMerandomSTRINGfromtheAPI
DEFAULT_MODEL=model-version-name
LOGFIRE_TOKEN=YetAonthERSoMerandomSTRINGfromtheAPI
MCP_SERVER_HOST=127.0.0.1
MCP_SERVER_PORT=8050
```
