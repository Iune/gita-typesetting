#!/bin/bash

script_location="src/index.ts"
source_directory="../resources"
output_directory="../latex/sections"

generate_latex() {
    local file_name=$1
    local chapter=$2
    local display_headers=$3
    local split_first_sloka=$4

    if [[ $display_headers = false ]];
    then 
        local headers_arg="--no-headers"
    else
        local headers_arg=""
    fi

    if [[ $split_first_sloka = true ]];
    then 
        local split_first_sloka_arg="--split-first-sloka"
    else
        local split_first_sloka=""
    fi

    local input_file_name="$source_directory/$file_name.txt"
    local iast_file_name="$output_directory/iast/$file_name.tex"
    local telugu_file_name="$output_directory/telugu/$file_name.tex"

    echo "Generating .tex files for $input_file_name"

    npx ts-node $script_location \
    -s $input_file_name \
    -c $chapter \
    -i $iast_file_name \
    -t $telugu_file_name \
    $headers_arg \
    $split_first_sloka_arg
}

generate_chapters() {
    generate_latex "opening-slokas" "0" false false
    generate_latex "closing-slokas" "0" false false
    generate_latex "chapter-2" "2" true false
}

generate_chapters
