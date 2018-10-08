#!/bin/bash
set -e

exec black --py36 --skip-string-normalization src/
