#!/bin/bash

# 取得認證
printf "$PASSWORD"|kinit admin
klist
