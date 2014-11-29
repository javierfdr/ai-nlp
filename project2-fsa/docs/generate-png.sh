#! /bin/sh
for i in ./*.svg; do inkscape $i --export-png=`echo $i | sed -e 's/svg$/png/'`; done
