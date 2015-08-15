## Reproducibility with CI

### Instructions for Reproducing Analysis

1. Fork repo
2. Sign up for [circle.ci](http://www.circleci.com), meaning that you should authenticate to allow Circle.ci to access your github, select your user or organization, and then select the newly forked repo and click "build."

### Details

1. Custom python setup commands go in config.py
2. All anayses go in "analysis" folder and must start with "test"
3. Output should go into "output folder"
