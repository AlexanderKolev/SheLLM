# SheLLM

## Setup

```bash
cp .env.example .env # Update .env with your configuration.
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

## Tests

Test following cases/scenarios:

- [ ] Test if it works while in SSH and if remote server will save history.
- [ ] Test how long history can be used/contextualized.
- [ ] Test if it works with different shells.
- [ ] Test if it handles errors.
- [ ] Test in tmux.
- [ ] Test in screen.
- [ ] Test context handling.

## Known Issues

- [ ] SheLLM does not handle error exits properly.
- [ ] SheLLM does not handle streaming output properly.
- [ ] SheLLM does not handle TAB completion for commands.
- [ ] SheLLM's context should take the last output with higher priority and not the previous commands.

## Roadmap

- [x] Add support for ChatGPT.
- [ ] Add Groq support.
- [ ] Add configuration support (LLM type, LLM model config per command type, token, history size, trigger chars, execute command without confirmation).
- [ ] Add wrapper for screen (auto start and stop).
- [x] Remove SheLLM prompts from history (intercept).
- [ ] Add detailed SheLLM history (with timestamps) for each session.
- [ ] Add local logging for full terminal context for future embeddings optimization.
- [ ] Add mechanism to handle streaming output (e.g. tail -f, top, etc.).
- [ ] Add TAB completion for commands.
- [ ] Proper handling of error exits.
