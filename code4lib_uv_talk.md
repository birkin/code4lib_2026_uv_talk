# uv talk notes

## todo

- put together initial outline
- confirm how long
- find previous notes

---


## outline

- What is `uv`?
    - 1/1:00 (done-by)
    - me
	- it's a python package-manager
	- not covered?

- Why do I find it to be so interesting?
    - 1/2:00
	- initially speed
	- now: 
		- venv invisibility (especially venv-related branching)
		- tools for others -- i think many don't know about some aspects of this

- How we started using it, for localdev and production.
    - 2/4:00
	- "pip"-compatibility mode

- How we're now using it, for localdev and production.
    - 4/8:00
	- pyproject.toml
	- ci-compatible
	- package-upgrade? new-branch; no problem, due to dependencies-as-code (with our code-update script)
        - on the one-hand, this is obvious, but it's not to be dismissed. Compare to the way we used to create alternate venvs, and point an env simlink to the currently active file -- and switch that when working with different branches.
    - experimentation: auto-package updater.

Transition from programming to helping others...

- Inline-script-metadata -- intro.
    - 2/10:00
	- imagine you're doing a demo for folk wanting to understand ways to access an api, or for folk wanting to explore natural-language-processing with spaCy.

- Inline-script-metadata -- gists.
    - 1/11:00
	- at some point, astral began supporting gists -- making it easier to share code with those folk above.

- Inline-script-metadata -- utilities.
    - 1/12:00 
	- if you can run gists remotely, you can run collections of scripts remotely -- more useful for finding/organizing/group-versioning.

- Inline-script-metadata -- github-pages.
    - 2/14:00
    - offers a really useful website for your users.

- Summary
    - 1/15:00 (done-by)

---
