# uv talk notes

(code4lib-2026)


## What is `uv`?

_(2/2:00 (done-by))_

Hi, I'm Birkin Diana, a developer for the Brown University Library. This talk is about a tool I've come to love, `uv`. `uv` does a lot of things, but I've found it most useful to think of it as a python package-manager, and, more broadly, as a tool for managing python environments. 

Just so we're on the same page: to clarify two terms... 
- term: "python-package": i think of a python-package as a bundle of code that does something. python comes with lots of useful bundles-of-code, or packages, built-in. So if you want to have your code make web-requests, or work with xml, python contains built-in packages for each of those; you don't have to install anything beyond python. But there are _lots_ of _really_ useful third-party python-packages that can be installed.
- term: "virtual-environment": project-A, from two years ago, might have been built with python-3.8, using a third-party xml python-package version-ABC. And project-B, that you're working on now, may be using python-3.12, using the same third-party xml python-package, but version-XYZ. virtual-environments are a way to organize these python/package environments in a way that don't interfere with one another.

Ok -- in this talk, I'll share two main things: 
- First, how our dev-team _started_ using `uv` -- and how we now use it -- for our projects. 
- Second, how how a feature of `uv` offers a way developers can work with colleagues to come up with really useful tools for end-users who _are_ interested in working with code-based tools -- but are _not_ that interested in nuances of installations and virtual-environments and package-management.

---


## How we started using `uv`

_(1:30/3:30)_

The standard, ubiquitous way folk work with python-packages and virtual-environments has been via the tool `pip`. `uv` has an entire pip-compatibility mode so that practically everything you've done with pip -- you can do, in almost the exact-same-way -- via uv.

So if you have a virtual-environment activated, instead of using the standard:

`pip install pymarc`

...you could use:

`uv pip install pymarc`

And if you have a "requirements.txt" file, listing the basic packages you're project needs, you can run a `uv` command very similar to:

`pip install -r /path/to/requirments.txt`

...that will populate your activated virtual-environment in nearly exactly the same way.

Because we were so comfortable with pip, that's how we started using `uv`. Yes, `uv` is faster, and yes, some of the ways `uv` does things under-the-hood are more elegant -- but it wasn't a tremendous savings. But we proceeded with this because of some other features I'll mention later.

If you're cautious and conservative, this will make you feel more comfortable about using `uv`. But my recommendation: don't do this.

---


## How we're now using `uv`

_(3:30/7:00)_

The way we now use `uv` centers on a file named `pyproject.toml`. This isn't a `uv`-specifict thing -- it's a standard python specification (PEP 621 and others).

Here's one of our typical pyproject.toml files:
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/main/pyproject.toml>

In the interests of time, I'm only going to point out two things in this file:

(1) **requires-python**
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/a5abcecb99dcf323930dfd765d86059178c8b3b5/pyproject.toml#L6>

(2) **dependencies**
<https://github.com/Brown-University-Library/bdr_uploader_hub_project/blob/a5abcecb99dcf323930dfd765d86059178c8b3b5/pyproject.toml#L7-L14>

If you use a standard pip requirements-file, the `dependencies` section will look very familiar: (Like with a requirements file, you don't have to use version-numbers, and if you do, there are different options.)

Ok -- let's say I `cd` into this project. Let's say I see the ./run_tests.py file and want to run it. And let's say I do _not_ have any virtual environment set up. To paraphrase a line from the "Muppet Christmas Carol": _"Now, once again, I must ask you to remember that I do _not_ have a virtual-environment. That one thing you must remember, or nothing that follows will seem wondrous."_


I try to run the tests, via:
`uv run ./run_tests.py`.


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

The kind-of-awesome significance of that: you think about your code, and what you want to do, and the virtual-enviroment stuff is auto-magically taken care of.

Here's what happening, under-the-hood:
- `uv` either updates (or creates) a `uv.lock` file, showing detailed info of _all_ dependencies (not just the ones listed in the pyproject.toml file, but their dependencies as well). (This is very much like the file `pip-compile` creates.)
- it then creates an invisible `.venv` directory.
- it then updates that `.venv` directory with whatever version of python is specified -- and with all the dependencies listed in the `uv.lock` file.
- it then activates that virtual-environment.
- it does all of that in the blink of an eye.
- it then runs that test-file -- in the context of the `.venv`'s virtual-environment.


To wrap this up -- because I want to get to the really fun stuff...

Here's our code-deployment script:
<https://github.com/Brown-University-Library/code_update_script/blob/main/uv_tomlized_code_update_script_CALLEE.sh>

the highlights...
- we cd to the project-directory: <https://github.com/Brown-University-Library/code_update_script/blob/753fb9cb806e0add69e4513899dd8455deee0cc6/uv_tomlized_code_update_script_CALLEE.sh#L55>
- this one line updates the virtual-environment, _superfast_: <https://github.com/Brown-University-Library/code_update_script/blob/753fb9cb806e0add69e4513899dd8455deee0cc6/uv_tomlized_code_update_script_CALLEE.sh#L61>

What this means is that if you're deploying a branch -- using this approach -- to experiment with a new version of python, or a new version of django, or a new version of an xml package -- or going back to the main branch afterwards -- you don't have to think -- at all -- about managing the virtual-environment. Your deploy is exactly the same as a code-only deploy; your code-changes to the pyproject.toml file auto-flow into an updated, active virtual-environment seamlessly, and very, very quickly.

---


## pivot -- helping others

What I've shared so far has been about how `uv` can be really useful for _development_. This second-half of the talk is about features `uv` offers that simplify working with code for _end-users_. 

(Credit to [Simon Willison][SW] for inspiring all of this.)

[SW]: <https://simonwillison.net/>


## Inline-script-metadata -- intro.

_(3:30/10:30)_

Imagine you're doing a workshop for folk wanting to learn about APIs, and how to access them. You want to show them useful code to access the API, and you want them to be able to run this on their own computers so that they can more easily experiment during and after the workshop.

Many of us have had the experience of wanting to cover something in a workshop -- only to experience getting bogged down in the set-up-process -- of installing a certain version of python, and then installing dependencies in a virtual-environment. That can be dispiriting for end-users. Sometimes a jupyter-notebook or a google-colab setup can minimize this. But `uv` can also be very useful for this, too.

Everything that follows _does_ assume end-users have installed `uv`. Most installation-instructions are just one-liners -- but it _is_ a requirement for what follows.

Ok -- you show your users this sample code:

(`code4lib_2026_uv_talk/api_example_01.py`)

...and ask them to `cd` to the directory where that file is, and then run:

`uv run ./api_example_01.py`

The output:
```
% uv run ./api_example_01.py
Primary Title: Abe Lincoln as a babe, as a boy and youth
```

Your workshop attendees have just been able to run a python script without installing python, or a virtual-environment, or dependencies. And you can focus on the API-concepts you want to.

The magic is in the inline-script-metadata at the top. Like the pyproject.toml file mentioned previously -- this is not a `uv` specific feature, but an official python-specification (PEP 723). 

Under-the-hood, uv is doing something very similar to what was shown before:
- it downloads the version of python if it's not already available
- it figures the dependencies and sub-dependencies needed
- it downloads ones that aren't already available and installs them into a virtual-environment
- it activates the virtual-environment
- it does all this invisibly to the user, in an ephemeral virtual-environment (with caching, so subsequent venv preparation is blazingly fast)
- finally,it runs the script in the context of that virtual-environment

One minoraddition: What if your script needs a secret-api-key? We developers would likely use a `.env` file and load the python-package `python-dotenv`. But you can tell your workshop-attendees to create a file named "secret_stuff.txt", put in `API_KEY = "whatever"`

...and then run `uv run --env-file "/path/to/scret_stuff.txt" ./api_example_01.py`

...and `uv` will make envars available from that file.

---


## Inline-script-metadata -- gists.
    - 0:30/11:00

The elves making `uv` didn't stop there, they enabled such scripts to be run _remotely_, like this:

`uv run "https://gist.github.com/birkin/8c10e338f266555e53ac2f3a496e4153"`

...making it easier to share code with end-users.

---


## Inline-script-metadata -- github repo.

_(0:30/11:30)_

But maybe you don't want to share lots of individual gist-urls (where the url doesn't convey meaning) with your workshop users. Wouldn't it be nice to group useful files together in a github repo, and share repo-script links?

You _can_ do that, but you have to use the "raw" github-url. Here's an example from an experimental "[utilities][ut]" repo:

```
% uv run "https://raw.githubusercontent.com/birkin/utilities-project/refs/heads/main/random_id_maker.py"
N2G7RCx4zV

% uv run "https://raw.githubusercontent.com/birkin/utilities-project/refs/heads/main/random_id_maker.py" --length 20
UxJmwDkHbaeRnNXTkyWH
```

[ut]: <https://github.com/birkin/utilities-project/blob/main/random_id_maker.py>

---


## Inline-script-metadata -- github-pages.

_(2/14:00)_

But the _ideal_ would be a way to bundle together a bunch of useful scripts to share, in a friendly useful way. A combination of `uv` and github-pages offers just this.

Here's an experimental github-repo of tools for working with the Brown Digital Repository (BDR) public API:
<https://github.com/Brown-University-Library/bdr-api-tools>

But we offer to end-users the much nicer website:
<https://brown-university-library.github.io/bdr-api-tools/>

The much friendlier website is auto-created from the repo via three steps:
- create an [index.md][idx] file  -- the repo's "README.md" file points to this.
- go to the repo's `Settings --> Pages` setting 
- under "Branch", change "None" to "main" -- and leave the default "/(root)" -- and click "Save"

In a few minutes, reloading the page will show, under the "GitHub Pages" title, the message: _"Your site is live at https://brown-university-library.github.io/bdr-api-tools/"_.

You can give that link to your users, and that landing page is completely under your control, from the `index.md` file. In that file, you can mix explanatory material with "try it" instructions -- containing friendly-url `uv` commands like:

```
% uv run https://brown-university-library.github.io/bdr-api-tools/calc_collection_size.py --collection-pid bdr:bwehb8b8
 
Collection: bdr:bwehb8b8
Title: Brown University Open Data Collection
Items found: 970
Items with size counted: 970
Total bytes: 266861380584
Human: 248.53 GB
```

[idx]: <https://github.com/Brown-University-Library/bdr-api-tools/blob/main/index.md>

---


## Closing

_(1/15:00)_

To sum up, I love `uv` for two main reasons:

- For our team's development work, it makes deploys affecting the virtual-environment no different than code-deploys, which greatly simplifies experimentation and package-upgrades.

- It can simplify the process of sharing code with end-users -- we can work with colleagues who do trainings to come up with scripts that end-users can bookmark and experiment with -- while minimizing discouraging setup-friction.

There's a lot more that `uv` does, but these are the highlights for me. I hope you enjoy using it for your own dev-projects -- and sharing with colleagues its end-user features. Please feel free to ping me with questions. Thanks.

---
