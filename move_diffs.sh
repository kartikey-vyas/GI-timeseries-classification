#!/bin/bash
for i in {1..60}
do
    scp mahuika:project/p4p/data/features/achat_${i}_diffs_eff.h5 data/features/
done
