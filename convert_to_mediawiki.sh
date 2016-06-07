#!/bin/bash

pandoc -f markdown -t mediawiki whitepaper.md > README.mediawiki
patch README.mediawiki patches/0001-Fix-images.patch
