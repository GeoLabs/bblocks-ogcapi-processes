#!/bin/bash
# Process building blocks
if [ -f '.volumes' ]; then
  VOLUMES=$(while read -r line; do
    if [[ "${line}" != /* ]]; then
      echo -n "-v ${PWD}/${line} "
    else
      echo -n "-v $line "
    fi
  done < .volumes)
fi
docker run --platform linux/amd64 -it --pull=always --rm --entrypoint /venv/bin/python --workdir /workspace -v "$(pwd):/workspace" ${VOLUMES} \
  ghcr.io/opengeospatial/bblocks-postprocess \
  /workspace/scripts/build_official_sources.py \
  --clean true --base-url http://localhost:9090/register/ "$@"
