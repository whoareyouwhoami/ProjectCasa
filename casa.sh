#!/bin/bash

display_info() {
  echo "Project CASA

  Usage:
    sh casa.sh --options

  Options:
    --apt_name     # Apartment name
    --apt_area     # Apartment area
    --type_one     # First option

  Note:


(C) Copyright 2020, Team Casa Production
"
}


args_check() {
  local VALUE="${2:-}"

	if [[ -z "$VALUE" ]]; then
		echo "Missing value for variable $1"
		exit 1
	else
	  # test
	  echo "$1: $VALUE"
	fi

	if [[ ${VALUE:0:2} == "--" ]]; then
		echo "Invalid option $VALUE passed for $1"
		exit 1
	fi

	# Returning value
	eval $1=\"$VALUE\"
}

args_parse() {
  local i=0

  while test $i -lt ${#ARGS[@]}; do
    local j=$((i+1))

    case ${ARGS[i]} in
      --) break;;
      --type_one)
        args_check "type_one" ${ARGS[$j]}
        i=$j;;
      --apt_name)
        args_check "apt_name" ${ARGS[$j]}
        i=$j;;
      --apt_area)
        args_check "apt_area" ${ARGS[$j]}
        i=$j;;
      *) echo "ERROR PARSING: ${ARGS[$i]}";;
    esac

    i=$((i+1))
  done
}

# If nothing is passed or "--help" is passed, show how this script is used
if [[ $# -eq 0 || "$1" == "--help" ]]; then
    display_info
    exit 0
fi

# Passed arguments
ARGS=("$@")

# Parsing arguments
args_parse

# Predict
echo "\n===== Let's Predict! ====="
RESULT=$(python3 Modeling/model.py  '당산반도유보라팰리스' 108)
