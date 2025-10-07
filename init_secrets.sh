#!/bin/bash

mkdir secrets
cd secrets
echo $1 > key.txt
echo $2 > pg_password.txt
