#!/bin/bash

mkdir -p dist
cp public/gita.pdf dist/
echo "/ /gita.pdf 302" > dist/_redirects
