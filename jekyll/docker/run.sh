#!/bin/sh
gem install bundler
bundle install
bundle exec jekyll serve --incremental
