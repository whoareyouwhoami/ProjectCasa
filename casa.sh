#!/bin/bash

display_info() {
  echo "Project CASA

  Usage:
    zsh casa.sh --options

  Options:
    --type_one     # First option
    --type_two     # Second option
    --type_three   # Third option


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
  local i=1

  while test $i -le ${#ARGS[@]}; do
    local j=$((i+1))

    case ${ARGS[i]} in
      --) break;;

      --type_one)
        args_check "type_one" ${ARGS[$j]}
        i=$j;;

      --type_two)
        args_check "type_two" ${ARGS[$j]}
        i=$j;;

      --type_three)
        args_check "type_three" ${ARGS[$j]}
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
