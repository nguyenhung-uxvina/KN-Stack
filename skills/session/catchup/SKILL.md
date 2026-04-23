Read the progress file and resume work from where the last session left off.

1. Read `progress.md` in the current project directory (or $ARGUMENTS if a specific path is given)
2. Read any files referenced in "Current State" or "Next Steps" to rebuild context
3. Summarize what was done previously and what's next
4. Begin working on the first item in "Next Steps"

If no progress file is found, say so and ask what to work on.
