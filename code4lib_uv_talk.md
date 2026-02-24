# uv talk notes

## todo

- put together initial outline
- confirm how long
- find previous notes

---


## outline

### What is `uv`?
    - 2/2:00 (done-by)
    - me
	- it's a python package-manager
	- not covered?

Hi, I'm Birkin Diana, a developer for the Brown University Library. This talk is about a tool I've come to love, `uv`. `uv` does a lot of things, but I've found it most useful to think of it as a python package-manager, and, more broadly, as a tool for managing python environments. 

Just so we're on the same page: to clarify two terms... 
- a python-package: it's a bundle of code that does something. python comes with lots of useful bundles-of-code, or packages, built-in. So if you want to have your code make web-requests or work with xml, you don't have to install anything beyond python. But there are _lots_ of _really_ useful third-party python-packages, like pymarc, from code4libber ed summers, for working with marc-records -- that can be installed.
- virtual-environment: project-A, from two years ago, might have been built with python-3.8, using a third-party xml python-package version-ABC. project-B, that you're working on now, may be using python-3.12, using the same third-party xml python-package, but version-XYZ. virtual-environments are a way to organize these python/package environments in a way that don't interfere with one another.

Ok -- in this talk, I'll share how our dev-team _started_ using `uv` -- and now uses it -- for our projects. And also how a feature of `uv` offers a way developers can work with other colleagues to come up with really useful tools for others who have no interest in programming/packages/development.

---


### How we started using `uv`
    - 1:30/3:30
	- "pip"-compatibility mode

The standard, ubiquitous way folk work with python-packages and virtual-environments has been via the tool `pip`. `uv` has an entire pip-compatibility mode so that everything you've done with pip -- you can do, in almost the exact-same-way -- via uv.

So if you have a virtual-environment activated, instead of using the standard:

`pip install pymarc`

...you could use:

`uv pip install pymarc`

And if you have a "requirements.in" file, listing the basic packages you're project needs, you can run a `uv` command very similar to:

`pip install -r /path/to/requirments.in`

...that will populate your activated virtual-environment in nearly exactly the same way.

Because we were so comfortable with pip, that's how we started using `uv`. Yes, `uv` is faster, and yes, some of the ways `uv` does things under-the-hood are more elegant -- but it wasn't a tremendous savings. But we proceeded with this because of some other features I'll mention later.

If you're cautious and conservative, this will make you feel more comfortable about using `uv`. But my recommendation: don't do this.

---


### How we're now using `uv`
    - 4/8:00
	- pyproject.toml
	- ci-compatible
	- package-upgrade? new-branch; no problem, due to dependencies-as-code (with our code-update script)
        - on the one-hand, this is obvious, but it's not to be dismissed. Compare to the way we used to create alternate venvs, and point an env simlink to the currently active file -- and switch that when working with different branches.
    - experimentation: auto-package updater.


---


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
