namespace :rake do
  desc "Invoke your awesome rake tasks!"
  task :invoke do
    on roles(:app) do
      within current_path do
        with rails_env: fetch(:stage) do
          execute :rake, ENV['ARGS']
        end
      end
    end
  end

  desc "hello world"
  task :build do
    on roles(:app) do
      within current_path do
          puts "hello world"
      end
    end
  end


end
