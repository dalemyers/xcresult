#!/bin/bash

pushd "${VIRTUAL_ENV}/.." > /dev/null

source "${VIRTUAL_ENV}/bin/activate"

python -m black --line-length 100 xcresult tests generator

python -m pylint --rcfile=pylintrc xcresult tests generator

python -m mypy --ignore-missing-imports xcresult/ tests/

popd > /dev/null

