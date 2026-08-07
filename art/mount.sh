#!/bin/sh
set -ex

mkdir -p mnt/modern_interiors
fuse-zip -o ro 'Modern_Interiors_Free_v2.2.zip' mnt/modern_interiors

mkdir -p mnt/sprout
fuse-zip -o ro "Sprout Lands - Sprites - Basic pack.zip" mnt/sprout

mkdir -p mnt/sprout_sorry
fuse-zip -o ro "Sprout Sorry pack.zip" mnt/sprout_sorry

mkdir -p mnt/sprout_ui
fuse-zip -o ro "Sprout Lands - UI Pack - Basic pack.zip" mnt/sprout_ui