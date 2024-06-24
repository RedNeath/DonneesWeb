#!/bin/bash
python sax_handler.py input.xml output.xml

python domSansXpath.py

python dom_and_xpath.py
