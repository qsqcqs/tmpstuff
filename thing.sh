#!/bin/bash
source bin/activate
#.8 is an asspull

image_path=/home/qsqcqs/Videos/Closeup-concrete-cracks.webp
out=`python id.py $image_path .8 | sed -E "s/Results saved to //g" | sed -E "s/\\x1b\[[01]m//g"`
echo $out
python bot.py $out
