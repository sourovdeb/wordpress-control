# WP AI Studio — VS Code Extension

Control your WordPress site with AI directly from VS Code. Generate posts, manage scheduling, chat with your site.

## Features

- **Multi-provider AI**: DeepSeek (recommended, cheapest), Ollama (free/local), Anthropic API
- **Post generation**: AI writes full HTML blog posts with SEO metadata, tags, excerpts
- **Approval mode**: Review before publishing — never auto-post without your sign-off
- **Scheduling**: Schedule posts to publish at a specific date/time
- **Live chat**: Ask your AI assistant to plan content strategy, suggest topics, improve SEO
- **Post management**: List, filter, and delete drafts/scheduled posts

## Installation

1. Clone this repo or download the zip
2. Open VS Code → `Extensions` sidebar → `...` menu → `Install from VSIX` (or load unpacked)
3. Open the Command Palette (`Ctrl+Shift+P`) → `WP AI: Open Studio`

## Configuration

In the WP AI Studio Settings tab, configure:

| Setting | Description |
|---------|-------------|
| WordPress URL | Your site URL, e.g. `https://sourovdeb.com` |
| Username | Your WordPress username |
| App Password | Generated in WP Admin → Users → Application Passwords |
| Plugin Key | Your `sourov-ai-controller` plugin secret key |
| AI Provider | `deepseek` (recommended), `ollama`, or `anthropic` |
| API Key | The key for your chosen provider |

## AI Provider Comparison

| Provider | Cost | Privacy | Speed | Setup |
|----------|------|---------|-------|-------|
| DeepSeek | ~$0.001/1K tokens (cheapest) | Cloud | Fast | API key |
| Ollama | Free (local) | 100% private | Depends on hardware | Install locally |
| Anthropic API | ~$0.003–0.015/1K tokens | Cloud | Fast | API key |

**Recommended**: Start with DeepSeek for the best cost/quality ratio. Switch to Ollama if privacy is critical.

## Getting API Keys

- **DeepSeek**: platform.deepseek.com → API Keys
- **Anthropic**: console.anthropic.com → API Keys
- **Ollama**: Free — install from ollama.ai, run `ollama serve`

## WordPress Plugin Required

This extension works with the `sourov-ai-controller` WordPress plugin (custom REST API endpoints). The plugin must be installed on your site.

## Security

- No API keys are hardcoded — all stored in VS Code user settings
- All settings are local to your machine
- The extension does NOT send data to any third-party except your chosen AI provider

## License

MIT
