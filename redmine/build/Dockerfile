FROM ruby:2.6-slim-buster

# explicitly set uid/gid to guarantee that it won't change in the future
# the values 999:999 are identical to the current user/group id assigned
RUN groupadd -r -g 999 redmine && useradd -r -g redmine -u 999 redmine

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		ca-certificates \
		wget \
		\
		bzr \
		git \
		mercurial \
		openssh-client \
		subversion \
                build-essential \
		\
# https://github.com/docker-library/redmine/issues/132
# (without "gsfonts" we get "Magick::ImageMagickError (non-conforming drawing primitive definition `text' @ error/draw.c/DrawImage/3265):")
		gsfonts \
		imagemagick \
	; \
	rm -rf /var/lib/apt/lists/*

RUN set -eux; \
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		dirmngr \
		gnupg \
	; \
	rm -rf /var/lib/apt/lists/*; \
	\
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	\
# grab gosu for easy step-down from root
# https://github.com/tianon/gosu/releases
	export GOSU_VERSION='1.11'; \
	wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
	gpgconf --kill all; \
	rm -r "$GNUPGHOME" /usr/local/bin/gosu.asc; \
	chmod +x /usr/local/bin/gosu; \
	gosu nobody true; \
	\
# grab tini for signal processing and zombie killing
# https://github.com/krallin/tini/releases
	export TINI_VERSION='0.18.0'; \
	wget -O /usr/local/bin/tini "https://github.com/krallin/tini/releases/download/v$TINI_VERSION/tini-$dpkgArch"; \
	wget -O /usr/local/bin/tini.asc "https://github.com/krallin/tini/releases/download/v$TINI_VERSION/tini-$dpkgArch.asc"; \
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --batch --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 595E85A6B1B4779EA4DAAEC70B588DFF0527A9B7; \
	gpg --batch --verify /usr/local/bin/tini.asc /usr/local/bin/tini; \
	gpgconf --kill all; \
	rm -r "$GNUPGHOME" /usr/local/bin/tini.asc; \
	chmod +x /usr/local/bin/tini; \
	tini -h; \
	\
# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

ENV RAILS_ENV production
WORKDIR /usr/src/redmine

# https://github.com/docker-library/redmine/issues/138#issuecomment-438834176
# (bundler needs this for running as an arbitrary user)
ENV HOME /home/redmine
RUN set -eux; \
	[ ! -d "$HOME" ]; \
	mkdir -p "$HOME"; \
	chown redmine:redmine "$HOME"; \
	chmod 1777 "$HOME"

ENV REDMINE_VERSION 4.2.3
ENV REDMINE_DOWNLOAD_SHA256 72f633dc954217948558889ca85325fe6410cd18a2d8b39358e5d75932a47a0c

RUN set -eux; \
	wget -O redmine.tar.gz "https://www.redmine.org/releases/redmine-${REDMINE_VERSION}.tar.gz"; \
	echo "$REDMINE_DOWNLOAD_SHA256 *redmine.tar.gz" | sha256sum -c -; \
	tar -xf redmine.tar.gz --strip-components=1; \
	rm redmine.tar.gz files/delete.me log/delete.me; \
	mkdir -p log public/plugin_assets sqlite tmp/pdf tmp/pids; \
	chown -R redmine:redmine ./; \
# log to STDOUT (https://github.com/docker-library/redmine/issues/108)
	echo 'config.logger = Logger.new(STDOUT)' > config/additional_environment.rb; \
# fix permissions for running as an arbitrary user
	chmod -R ugo=rwX config db sqlite; \
	find log tmp -type d -exec chmod 1777 '{}' +

RUN set -eux; \
	\
	savedAptMark="$(apt-mark showmanual)"; \
	apt-get update; \
	apt-get install -y --no-install-recommends \
		freetds-dev \
		gcc \
		libmagickcore-dev \
		libmagickwand-dev \
		libmariadbclient-dev \
		libpq-dev \
		libsqlite3-dev \
		make \
		patch \
	; \
	rm -rf /var/lib/apt/lists/*; \
	\
	gosu redmine bundle install --jobs "$(nproc)" --without development test; \
	for adapter in mysql2 postgresql sqlserver sqlite3; do \
		echo "$RAILS_ENV:" > ./config/database.yml; \
		echo "  adapter: $adapter" >> ./config/database.yml; \
		gosu redmine bundle install --jobs "$(nproc)" --without development test; \
		cp Gemfile.lock "Gemfile.lock.${adapter}"; \
	done; \
	rm ./config/database.yml; \
# fix permissions for running as an arbitrary user
	chmod -R ugo=rwX Gemfile.lock "$GEM_HOME"; \
	rm -rf ~redmine/.bundle; \
	\
# reset apt-mark's "manual" list so that "purge --auto-remove" will remove all build dependencies
	apt-mark auto '.*' > /dev/null; \
	[ -z "$savedAptMark" ] || apt-mark manual $savedAptMark; \
	find /usr/local -type f -executable -exec ldd '{}' ';' \
		| awk '/=>/ { print $(NF-1) }' \
		| sort -u \
		| grep -v '^/usr/local/' \
		| xargs -r dpkg-query --search \
		| cut -d: -f1 \
		| sort -u \
		| xargs -r apt-mark manual \
	; \
	apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

VOLUME /usr/src/redmine/files
COPY docker-entrypoint.sh /
RUN set -eux; \
	chmod 1777 /docker-entrypoint.sh; \
  chown redmine:redmine /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 3000
CMD ["rails", "server", "-b", "0.0.0.0"]
