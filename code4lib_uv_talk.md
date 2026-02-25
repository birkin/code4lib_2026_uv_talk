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
    - 3:30/7:00
	- pyproject.toml
	- ci-compatible
	- package-upgrade? new-branch; no problem, due to dependencies-as-code (with our code-update script)
        - on the one-hand, this is obvious, but it's not to be dismissed. Compare to the way we used to create alternate venvs, and point an env simlink to the currently active file -- and switch that when working with different branches.
    - experimentation: auto-package updater.

The way we now use `uv` centers on a file named `pyproject.toml`. This isn't a `uv`-specifict thing -- it's a python standard.

Here's one of our typical pyproject.toml files:
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/main/pyproject.toml>

In the interests of time, I'm only going to point out two things in this file:

(1) **requires-python**
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/a5abcecb99dcf323930dfd765d86059178c8b3b5/pyproject.toml#L6>

(2) **dependencies**
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/a5abcecb99dcf323930dfd765d86059178c8b3b5/pyproject.toml#L7-L14>

If you use a requirements-file, the `dependencies` section will look very familiar: (Like with a requirements file, you don't have to use version-numbers, and if you do, there are different options.)

Ok -- let's say I `cd` into this project. And let's say I do _not_ have any virtual environment set up. And let's say I want to run the tests, via:
`uv run ./run_tests.py`.

To paraphrase the "Muppet Christmas Carol" (which paraphrases Dickens):
"Now, once again, I must ask you to remember that I do _not_ have a virtual-environment. That one thing you must remember, or nothing that follows will seem wondrous."

What you'll see...

```
bdr_uploader_hub_project % uv run ./run_tests.py
Found 25 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.........................
----------------------------------------------------------------------
Ran 25 tests in 0.710s

OK
```

Here's what happens, under-the-hood:
- `uv` will update (or create) a `uv.lock` file, showing detailed info of _all_ dependencies (not just the ones listed in the pyproject.toml file, but their dependencies as well). (This is very much like pip's `requirements.txt` file.)
- it will then create an invisible `.venv` directory.
- it will then update that `.venv` directory with whatever version of python is specified -- and with all the dependencies listed in the `uv.lock` file.
- it will then activate that virtual-environment.
- it does all of that in the blink of an eye.
- it will then run the tests, in the context of the `.venv's` virtual-environment.

The kind-of-awesome significance of that: you think about your code, and what you want to do, and the virtual-enviroment stuff is auto-magically taken care of.

To wrap this up -- because I want to get to the really fun stuff...

Here's our code-deployment script:
<https://github.com/Brown-University-Library/code_update_script/blob/main/uv_tomlized_code_update_script_CALLEE.sh>

the highlights...
- we cd to the project-directory: <https://github.com/Brown-University-Library/code_update_script/blob/753fb9cb806e0add69e4513899dd8455deee0cc6/uv_tomlized_code_update_script_CALLEE.sh#L55>
- this one line updates the virtual-environment, _superfast_: <https://github.com/Brown-University-Library/code_update_script/blob/753fb9cb806e0add69e4513899dd8455deee0cc6/uv_tomlized_code_update_script_CALLEE.sh#L61>

What this means is that if you're deploying a branch to experiment with a new version of python, or a new version of django, or a new version of an xml package -- you don't have to think -- at all -- about managing the virtual-environment. Your deploy is exactly the same as a code-only deploy; your code-changes to the pyproject.toml file auto-flow into an updated, active virtual-environment seamlessly, and very, very quickly.

---


### helping others

What I've shared so far has been about how uv can be really useful for development. This second-half of the talk is about features `uv` offers that simplify working with code for non-developers. 

#### Inline-script-metadata -- intro.
    - 2/10:00
	- imagine you're doing a demo for folk wanting to understand ways to access an api, or for folk wanting to explore natural-language-processing with spaCy.

Imagine you're doing a workshop for folk wanting to learn about APIs, and how to access them. You want to show them useful code to access the API, and you want them to be able to run this on their own computers so that they can more easily experiment during and after the workshop.

Most of us have likely had the experience of wanting to cover something in a workshop -- only to experience getting bogged down in the set-up-process -- of installing a certain version of python, and then installing dependencies in a virtual-environment. Sometimes a jupyter-notebook or google-colab can minimize this. But `uv` can really be terrific for this, too.

Everything that follows _does_ assume end-users have installed `uv`. I have not found that installation to be onerous -- but it is a requirement for what fillows.

Ok -- you show your users this sample code:

```
```

---


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
