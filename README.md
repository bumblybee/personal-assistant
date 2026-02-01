# Personal Assistant

Personal assistant MCP server. WIP.

## Setup

```bash
uv sync
uv run db.py  # Initialize database
```

## Claude Desktop Config

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "assistant": {
      "command": "/path/to/uv",
      "args": [
        "run",
        "--project",
        "/path/to/personal_assistant",
        "python",
        "/path/to/personal_assistant/server.py"
      ],
      "cwd": "/path/to/personal_assistant"
    }
  }
}
```

## Tools

- `save_note` - Save a note with optional tag
- `get_notes` - List recent notes
- `search_notes` - Search notes by content
- `delete_note` - Delete a note by ID
- `add_reminder` - Create a reminder with optional time
- `get_reminders` - List pending reminders
- `complete_reminder` - Mark reminder as done
