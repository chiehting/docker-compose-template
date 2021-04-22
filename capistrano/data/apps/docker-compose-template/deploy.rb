# deploy.rb file shared between all the stages of a certain app

set :application, 'docker-compose-template'
set :repo_url, 'https://github.com/chiehting/docker-compose-template.git'
ask :branch, 'main'
set :deploy_to, '/opt/docker-compose-template'
