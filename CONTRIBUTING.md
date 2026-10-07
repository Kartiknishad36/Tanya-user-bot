# Contributing to Tanya UserBot

## How to Contribute

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test locally
5. Commit and Push
6. Open a Pull Request

## Adding a New Plugin

Create a file in `plugins/`:

```python
"""
Plugin Name
Commands: .cmd1
"""
from utils.helpers import edit_or_reply, command_pattern
from core.decorators import errors_handler

def register(client):
    @client.on(command_pattern("mycmd(?: |$)(.*)"))
    @errors_handler
    async def handler(event):
        await edit_or_reply(event, "Hello!")
```

Update `plugins/help.py` and `COMMANDS.md`.

Thank you for contributing!
