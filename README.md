# Poetry Import Requirements (plugin)
***
> A super quick plugin I wrote for Poetry that adds a command to install from a requirements.txt file.  This is helpful for when you want to migrate a project over to poetry.
***

# Installing

As of now (May 13, 2020) the plugin system has been merged to master, but has **not** been released to PyPi (1.2.0a1). When the plugin system has been released, i'll publish this plugin to PyPi.

# Usage

```bash
poetry install-from-requirements <path-to-requirements.txt>

# dry run
poetry install-from-requirements --dry-run requirements.txt

```

# Tests

No tests at this time.