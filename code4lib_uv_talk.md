# uv talk notes

(code4lib-2026)

**(title-slide)**


## What is `uv`?

Hi, I'm Birkin Diana, a developer for the Brown University Library. This talk is about an open-source tool I've come to love, `uv`. 

**(uv slide)**

`uv` does a lot of things, but I've found it most useful to think of it as a python package-manager, and, more broadly, as a tool for managing python environments. 

Just so we're on the same page: to clarify two terms... 

**(terms slide)**

- **"python-package"**: i think of a python-package as a bundle of code that does some -thing-. python comes with lots of useful bundles-of-code, or packages, built-in. So if you want to have your code make web-requests, or work with xml, python contains built-in packages for each of those; you don't have to install anything beyond python. But there are _lots_ of _really_ useful third-party python-packages that can be installed.
- **"virtual-environment"**: project-A, from two years ago, might have been built with python-3.8, using a third-party xml package version-ABC. And project-B, that you're working on now, may be using python-3.12, using the same third-party xml package, but version-XYZ. virtual-environments are a way to organize these python/package environments in a way that don't interfere with one another.

Ok -- in this talk, I'll share two main things: 

**(in-this-talk slide)**

- First, how our dev-team _started_ using `uv` for our development projects -- and how we now use it. 

- Second, how how a feature of `uv` offers a way developers can work with colleagues to come up with really useful tools for end-users who _are_ interested in working with code-based tools -- but are _not_ that interested in nuances of installations and virtual-environments and package-management.

---

_(2/2:00 (done-by))_


**(FIRST slide)**

## How we started using `uv`

**(our-uv-start slide)**

The standard, ubiquitous way folk work with python-packages and virtual-environments has been via the tool `pip`. `uv` has an entire pip-compatibility mode so that practically everything you've done with pip -- you can do, in almost the exact-same-way -- via uv.

So if you have a virtual-environment activated, instead of using the standard:

`pip install pymarc`

...you could use:

`uv pip install pymarc`

And if you have a "requirements.txt" file, listing the packages you're project needs, you can run a `uv` command very similar to:

`pip install -r /path/to/requirments.txt`

...that will populate your activated virtual-environment in nearly exactly the same way.

Because we were so comfortable with pip, that's how we started using `uv`. Yes, `uv` is faster, and yes, some of the ways `uv` does things under-the-hood are more elegant -- but it wasn't a tremendous savings.
If you're cautious and conservative, this will make you feel more comfortable about using `uv`. But my recommendation: don't do this.

---
_(1:30/3:30)_


## How we're now using `uv`

**(our-current-usage slide)**

The way we now use `uv` centers on a file named `pyproject.toml`. This isn't a `uv`-specifict thing -- it's a standard python specification (PEP 621 and others).

**(pyproject.toml example)**

Here's one of our typical pyproject.toml files.

In the interests of time, I'm only going to point out two things in this file:

(1) _requires-python_

...where a python-version is specified.

(2) _dependencies_

If you use a standard pip requirements-file, the `dependencies` section will look very familiar: (Like with a requirements file, you don't have to use version-numbers, and if you do, there are different options.)

Ok -- let's say I `cd` into this project. 

**(run_tests slide)**

Let's say I've set this project up a couple of days ago, but haven't done anything regarding a virtual environment yet. I see the run_tests.py file and want to run it -- i often start work on a project that way. To paraphrase a line from "A Muppet Christmas Carol": _"Now, once again, I must ask you to remember that I do _not_ have a virtual-environment. That one thing you must remember, or nothing that follows will seem wondrous."_

I try to run the tests...

**(run_tests.py-attempt slide)**

...and they run! And remember all those dependencies!

The kind-of-awesome significance of that: you think about your code, and what you want to do, and the virtual-enviroment stuff is auto-magically taken care of.

Here's what happening, under-the-hood:
- `uv` either updates (or creates) a `uv.lock` file, showing detailed info of _all_ dependencies (not just the ones listed in the pyproject.toml file, but their dependencies as well). (This is very much like the file `pip-compile` creates.)
- next, `uv` sets up an invisible `.venv` directory -- and activates it.
- it then updates that `.venv` directory with whatever version of python is specified -- and with all the dependencies listed in the `uv.lock` file.
- it does all of that in the blink of an eye.
- and then `uv` runs that run_tests.py file -- in the context of the `.venv`'s virtual-environment.

Here's our code-deployment script...

**(deploy-script slide)**

the highlights...

- we cd to the project-directory

- we run a `uv` sync command -- this one line fully updates the virtual-environment from the pyproject.toml file -- via an updated uv.lock file -- _superfast_

**(a venv-deploy-becomes slide)**

What this means is that if you're deploying a branch -- using this approach -- to experiment with a new version of python, or a new version of django, or a new version of some other package -- or going back to the main branch afterwards -- you don't have to think -- at all -- about managing the virtual-environment. Your deploy is exactly the same as a code-only deploy; your code-changes to the pyproject.toml file auto-flow into an updated, active virtual-environment seamlessly, and very, very quickly.

---
_(3:30/7:00)_


**(PIVOT slide)**

## pivot -- helping others

What I've shared so far has been about how `uv` can be really useful for _development_. 

**(scenarios slide)**

This second-half of the talk is about features `uv` offers that simplify working with code for _end-users_, and our colleagues that work with end-users.

The problem being addressed:

Many of us have had the experience of wanting to run workshop for users on something like how to access APIs -- only to experience getting bogged down in the set-up-process -- of installing a certain version of python, and then installing dependencies in a virtual-environment. That can be dispiriting for end-users. Sometimes a jupyter-notebook or a google-colab setup can minimize this. But `uv` can also be very useful for this, too.

Everything that follows _does_ assume end-users have installed `uv`. Most installation-instructions are just one-liners -- but it _is_ a requirement for what follows.


## Inline-script-metadata -- intro.

**(api-workshop slide)**

Imagine you're doing a workshop for folk wanting to learn about APIs, and how to access them. You want to show them useful code to access the API, and you want them to be able to run this on their own computers so that they can more easily experiment during and after the workshop.

Ok -- you give your users this sample API-access code.

...and then, you ask them to `cd` to the directory where that file is, and then run it...

**(output slide)**

...and it works. 

You point out how the code accessed the url, then parsed the json response, and printed the result. You've focused on API concepts and code.

What you haven't done is spent _any_ time with your users on set-up and installation -- but not because this is hidden, and they'll have to figure out good-practices later -- but because this is the way `uv` works.

Your workshop attendees have just been able to run a python script without _explitly_ installing python, or a virtual-environment, or dependencies.

**(inline-script-metadata slide)**

The magic is in the inline-script-metadata at the top. Like the pyproject.toml file mentioned previously -- this is not a `uv` specific feature, but an official python-specification (PEP 723). 

Under-the-hood, uv is doing something very similar to what was shown before:
- it downloads the version of python if it's not already available
- it figures the dependencies and sub-dependencies needed
- it downloads ones that aren't already available and installs them into a virtual-environment
- it activates and populates the virtual-environment
- it does all this invisibly to the user, in an invisible ephemeral virtual-environment -- with caching, so subsequent venv preparation is blazingly fast
- finally,it runs the api-script in the context of that virtual-environment

SKIP-FOR-TIME? **(need-envar-secrets? slide)**

One aside: What if your script needs a secret-api-key? We developers would likely use a `.env` file and load the python-package `python-dotenv`. But you can tell your workshop-attendees to create a file named "secret_stuff.txt", put in `API_KEY = "whatever"`

...and then run the script like before, passing in a path-argument.

...and `uv` will make envars available from that file.

---
_(3:30/10:30)_

If both `pyproject.toml` and `inline-script-metadata` can manage the virtual-envionmnet, what to use when? 

**(I.S.Metadata-vs-PP.toml?)**

A brief answer: use `pyproject.toml` for projects, and `inline-script-metadata` for single-file scripts. There are grey areas; pyproject.toml offers many more features -- but that's a workable rule.


## Inline-script-metadata -- gists.

Ok -- as we've seen, inline-script-metadata is the key info for how useful `uv` can be for end-users. But for colleagues working with end-users, `uv` also allows remote-execution of code that can be super-useful for sharing scripts that end-users can run easily, from their own computers. I'll show a few examples.

**(InlScrMetadata-gists slide)**

First, uv can directly run code in gists, providing great opportunities to share code with end-users.

---
_(0:30/11:00)_


## Inline-script-metadata -- github repo.

But maybe you don't want to share lots of individual gist-urls (where the url doesn't convey meaning) with your workshop users. Wouldn't it be nice to group useful files together in a github repo, and share repo-script links?

**(InlScrMetadata-github-repo slide)**

Well you _can_ do that, but it's not ideal... Here's an example from a little utilities-repo of mine -- this particular utility-script just outputs random-IDs in a way I like. I'm not going to go over this in the interests of time.

The url does contain more meaning -- but you have to use the "raw" github-url, and can't be described as "friendly".

---
_(0:30/11:30)_


## Inline-script-metadata -- github-pages.

The _ideal_ would be a way to bundle together a bunch of useful scripts to share, in a repo, but with a friendly interface. 

**(InlScrMetadata-github.io-pages slide)**

A combination of `uv` and github.io-pages offers just this.

We have a small github-repo of tools for end-users -- for working with the Brown Digital Repository public APIs.

But we don't offer that repo-url, but instead offer a much nicer website url. This is part of a long useful landing-page.

**(example-website slide)**

This much friendlier website is auto-created from the repo via just three _one-time_ steps:

**(three-steps slide)**

- you create an `index.md` file (which automatically becomes the landing-page html)  -- in our repo's "README.md" file we direct folk to this file
- you change one repository setting 
- you click "Save"

In a few minutes, reloading the page will show the url to your new website, auto-built and, ongoing -- auto-updated from the repo.

Your colleagues can give that link to the workshop-users, and that landing page is easily updatable by your team or your colleagues -- via the `index.md` file. 

**(example-website-2 slide)**

In that `index.md`file, you can mix explanatory material with code and "Usage" instructions...

**(nice-script-urls slide)**

...containing friendly-url `uv` commands like the one shown here. This particular tool takes a collection-pid argument and calculates the size of all the items in the given collection. Yet again -- the focus is on concepts and code and usability -- not on environment-particulars.

---
_(2/14:00)_


## Closing

**(closing slide)**

To sum up, I love `uv` for two main reasons:

- For our team's development work, it makes deploys affecting the virtual-environment no different than code-deploys, which greatly simplifies experimentation and package-upgrades.

- It can simplify the process of sharing code with end-users -- we can work with colleagues who do trainings to come up with scripts that end-users can bookmark and experiment with -- while minimizing discouraging setup-friction.

There's a lot more that `uv` does, but these are the highlights for me. I hope you enjoy using it for your own dev-projects -- and sharing with colleagues its end-user features. Please feel free to ping me with questions. Thanks.

---
_(1/15:00)_
