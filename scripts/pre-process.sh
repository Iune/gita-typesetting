#!/bin/bash

python_script_location="python/transliterate.py"
source_directory="transliteration"
output_directory="latex/sections"

generate_latex() {
    local file_name=$1
    local chapter=$2
    local input_scheme=$3
    local output_language=$4
    local display_headers=$5
    local split_first_sloka=$6

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
    local output_file_name="$output_directory/$output_language/$file_name.tex"

    echo "Generating .tex file for $input_file_name at $output_file_name"

    python $python_script_location \
    $input_file_name \
    --input-scheme $input_scheme \
    --output-scheme $output_language \
    --file $output_file_name \
    --chapter $chapter \
    $headers_arg \
    $split_first_sloka_arg
}

generate_chapters() {
    local language=$1

    generate_latex "opening-slokas" "0" "itrans" $language false false
    generate_latex "closing-slokas" "0" "itrans" $language false false
    generate_latex "chapter-2" "2" "itrans" $language true false
}

generate_chapters "telugu"
# generate_chapters "devanagari"
