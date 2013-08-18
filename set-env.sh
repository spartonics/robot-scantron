#!/usr/bin/env bash

function get_root()
{
    local REPOROOT
    REPOROOT=$(readlink -f ${BASH_SOURCE[0]})
    REPOROOT=${REPOROOT%/*}
    echo "$REPOROOT"
}

export PYTHONPATH="$(get_root):$PYTHONPATH"
