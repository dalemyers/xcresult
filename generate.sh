#!/bin/bash

pushd "${VIRTUAL_ENV}/.." > /dev/null

source "${VIRTUAL_ENV}/bin/activate"

python generator/__init__.py
python -m black --line-length 100 xcresult/model.py

popd > /dev/null

