#!/bin/bash
rsync -avrz --delete --exclude "*~" --delete-excluded ~/SloanAtlas/www/ howdy:public_html/SloanAtlas/
