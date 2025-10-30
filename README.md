# cpp102

Small C program for experimenting with scanf/sscanf parsing and basic I/O.

## Files
- `cpp102.c` — main program (loops, reads a line with `fgets`, parses with `sscanf`).
- `pad.txt` — scratch file (optional).

## Build and run (VS Code tasks)
- Build task: "build cpp102"
- Run task: "run cpp102"

## Build from terminal (macOS)
```bash
clang -g cpp102.c -o cpp102
./cpp102
```

## Notes
- Program prompts: "Enter number followed by unit:" and parses input like `234 E`.
- Adjust parsing format strings in `cpp102.c` to explore edge cases.