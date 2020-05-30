#!/bin/bash

display_info() {
  echo "Project CASA

  Usage:
    sh casa.sh --options

  Required:
    --apt_name     # Apartment name
    --apt_area     # Apartment area
    --predict_num  # Predicting duration

  Optional:
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
#	else
	  # test
#	  echo "$1: $VALUE"
	fi

	if [[ ${VALUE:0:2} == "--" ]]; then
		echo "Invalid option $VALUE passed for $1"
		exit 1
	fi

	# Returning value
	eval $1=\"$VALUE\"
	echo "Evaluating" $1
}

show_warning() {
  MSG=$1
  echo $MSG
  exit 1
}

args_parse() {
  local i=0

  while test $i -lt ${#ARGS[@]}; do
    local j=$((i+1))

    case ${ARGS[i]} in
      --) break;;
      --type_one)
        args_check "TYPE_ONE" ${ARGS[$j]}
        i=$j;;
      --apt_name)
        args_check "APT_NAME" ${ARGS[$j]}
        i=$j;;
      --apt_area)
        args_check "APT_AREA" ${ARGS[$j]}
        i=$j;;
      --predict_num)
        args_check "PREDICT_NUM" ${ARGS[$j]}
        i=$j;;
      *) show_warning "ERROR PARSING: ${ARGS[$i]}";;
    esac

    i=$((i+1))
  done

  # Checking if required options are given
  if [[ -z ${APT_NAME} ]]; then
    show_warning "Apartment name required for --apt_name"
  fi
  if [[ -z ${APT_AREA} ]]; then
    show_warning "Apartment area required for --apt_area"
  fi
  if [[ -z ${PREDICT_NUM} ]]; then
    show_warning "Please specify forecasting months for --predict_num"
  fi
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

RESULT=$(python3 Modeling/model.py ${APT_NAME} ${APT_AREA} ${PREDICT_NUM})

