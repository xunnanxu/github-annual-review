# github-annual-review

This generates a personal annual report for your 2018 Github contributions.

This is a very preliminary weekend project. Please contribute to this if you are willing to help.

## Feature wish list

- Add i18n support
- Optionally hide tabs for people with no certain data
- NLP repo readme to produce interested topics (e.g. Front-end, Web, ML, Data Processing and more specific topics like React, Tensorflow, OpenCV, Spark etc.)
- Error handling
- Data caching

## Run locally

An github OAuth app is required.

python 3 is required.

```console
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ GH_CLIENT_ID=xx GH_CLIENT_SECRET=xx flask run
```
