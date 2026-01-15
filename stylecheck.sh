#!/bin/bash

pushd "${VIRTUAL_ENV}/.." > /dev/null

source "${VIRTUAL_ENV}/bin/activate"

python -m black --line-length 100 xcresult tests

python -m pylint --rcfile=pylintrc xcresult tests

python -m mypy --ignore-missing-imports xcresult/ tests/

python -m pyright

popd > /dev/null

