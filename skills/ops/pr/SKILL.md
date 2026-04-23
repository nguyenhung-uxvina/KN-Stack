Clean up the code, stage changes, and prepare a pull request.

1. Run linters/formatters if configured in the project (check package.json scripts, pyproject.toml, etc.)
2. Fix any lint errors or formatting issues
3. Review all changed files with `git diff` — look for debug code, console.logs, TODOs, commented-out blocks
4. Clean up anything that shouldn't be committed
5. Stage the relevant files (prefer specific files over `git add -A`)
6. Show me a summary of what will be committed and a draft PR title + description
7. Wait for my approval before creating the commit or PR

If $ARGUMENTS is provided, use it as the target branch or PR title hint.
