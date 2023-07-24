cloudify-plugin-template
========================

[![Build Status](https://travis-ci.org/cloudify-cosmo/cloudify-plugin-template.svg?branch=master)](https://travis-ci.org/cloudify-cosmo/cloudify-plugin-template)

Cloudify plugin project template.

## Usage

See [writing your own plugin](https://docs.cloudify.co/latest/developer/writing_plugins/)

## Tests

To run the example plugin tests, the included `dev-requirements.txt` should be installed.

```
pip install -r dev-requirements.txt
```

# wagon build 

docker run -v /Users/aryanraghav/dell-poc/cloudify-plugin-equinix/:/packaging cloudifyplatform/cloudify-ubuntu-18-04-py3-wagon-builder                   