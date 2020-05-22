#!/bin/bash


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
        args_check "type_one" $ARGS[j]
        i=$j;;

      --type_two)
        args_check "type_two" $ARGS[j]
        i=$j;;

      --type_three)
        args_check "type_three" $ARGS[j]
        i=$j;;
      *) echo "ERROR PARSING: $ARGS[i]";;
    esac
    i=$((i+1))
  done
}

# Passed arguments
ARGS=("$@")

# Parsing arguments
args_parse
