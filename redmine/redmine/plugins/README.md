# Redmine plugins

Put your Redmine plugins here.

## redmine checklists light

啟動時會自動執行 `rake redmine:plugins:migrate`. 下面為手動執行命令.

[Download plugin](https://www.redmineup.com/license_manager?token=1f4a18cc23cdb44fb0b665bd2b8cb9c6ef35d&utm_source=Main&utm_medium=email&utm_campaign=purchase_download_link_email&utm_term=download_plugin&utm_content=installation_purchase_link)

[Install plugin](https://www.redmineup.com/pages/help/checklists/installing-redmine-checklists-plugin-on-linux)

```bash
bundle install --without development test --no-deployment
bundle exec rake redmine:plugins NAME=redmine_checklists RAILS_ENV=production
touch tmp/restart.txt
```

## redmine gitlab hook
[Download plugin](https://github.com/phlegx/redmine_gitlab_hook.git)