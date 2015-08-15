## Reproducibility with CI

### Instructions for Reproducing Analysis

1. Fork repo
2. Sign up for [circle.ci](http://www.circleci.com), meaning that you should authenticate to allow Circle.ci to access your github, select your user or organization, and then select the newly forked repo and click "build."

### Details

1. Custom python setup commands go in config.py
2. All anayses go in "analysis" folder and must start with "test"
3. Output should go into "output folder"


### Notes
 - The repo should have a python module that handles setting things up. This would include:
    - download functions and specified locations for the user to look for the data
    - functions to "initialize" a repo (put it into the correct format)
 - we can possibly set up an interactive browser to connect to (circle.ci uses selenium via xvfb)
 - pushing content back to gh-pages? Would require authentication, likely one step too much.
 - Circle.ci will "time out" if there is no output >10 minutes (something to keep in mind)
 - There should be a nice way to direct user to output interface, keep updated wrt timing, etc.
