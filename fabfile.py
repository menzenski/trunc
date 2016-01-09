# -*- coding: utf-8 -*-

from fabric.api import *
from fabric.contrib.console import confirm

def create_sphinx_pages():
    """
    Create a new branch with Sphinx documentation ready to be published
    using GitHub Pages.

    Example usage:

        $ fab make_sphinx_branch

    Before you can publish your docs, you need to commit them to the repo.

        $ git add .
        $ git commit -am "First commit"

    Then publish the files by pushing them up to GitHub.

        $ git push origin gh-pages

    Then the docs will appear on GitHub at:

        http://<your_account_name>.github.com/<your_repo_name>/

    """
    # create the new branch
    local("git branch gh-pages")
    # move into it
    local("git checkout gh-pages")
    # clear it out
    local("git symbolic-ref HEAD refs/heads/gh-pages")
    local("rm .git/index")
    local("git clean -fdx")
    # install sphinx
    local("pip install sphinx")
    # save the dependencies to the requirements file
    local("pip freeze > requirements.txt")
    # warn the user of a quirk before configuring with Sphinx
    confirm("ANSWER YES to 'Separate source and build directories! [y]'")
    # start up a Sphinx project
    local("sphinx-quickstart")
    # create the .nojekyll file GitHub requires
    local("touch .nojekyll")
    # make the necessary patches to Sphinx's Makefile
    local("echo '' >> Makefile")
    local("echo 'BUILDDIR      = ./' >> Makefile")
    local("echo '' >> Makefile")
    local("echo '\t$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)' >> Makefile")
    local("echo '\t@echo' >> Makefile")
    local("echo '\t@echo \"Build finished. The HTML pages are in $(BUILDDIR) \"' >> Makefile")
    # make the branch for the first time
    local("make html")
