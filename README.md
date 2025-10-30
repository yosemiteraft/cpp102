# cpp102

Small C program for experimenting with scanf/sscanf parsing and basic I/O.

## Files
- `cpp102.c` — main program (loops, reads a line with `fgets`, parses with `sscanf`).
- `pad.txt` — scratch file (optional).

## Build and run (VS Code tasks)
- Build task: "build cpp102"
- Run task: "run cpp102"

## Index the code (call graph)
- Task: "index code" — regenerates a lightweight call graph into `.vscode/code-index.json`.
- CLI alternative:
	- ```bash
		python3 tools/index_c.py . .vscode/code-index.json
		```
	- The JSON file is ignored by Git.

## Build from terminal (macOS)
```bash
clang -g cpp102.c -o cpp102
./cpp102
```

## Notes
- Program prompts: "Enter number followed by unit:" and parses input like `234 E`.
- Adjust parsing format strings in `cpp102.c` to explore edge cases.