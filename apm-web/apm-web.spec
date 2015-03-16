# spec file for apm-web
#
# Copyright (c) 2015 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_owner     patrickallaert
%global gh_name      php-apm-web
%global gh_commit    d7425e00f2f6b3004c21c46d1d6e097fbd78d033
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%if 0%{?fedora} >= 21
# support for apache / nginx / php-fpm
%global with_phpfpm 1
%else
%global with_phpfpm 0
%endif

Name:          apm-web
Version:       2.0.0
Release:       3%{?dist}
Summary:       APM (Alternative PHP Monitor) web frontend

Group:         Applications/Internet
License:       PHP
URL:           https://github.com/%{gh_owner}/%{gh_name}
Source0:       %{url}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz

# Webserver configuration files
Source1:        %{name}.httpd
Source2:        %{name}.nginx

# Temporary fix for https://github.com/patrickallaert/php-apm-web/issues/1
Source3:        https://raw.githubusercontent.com/patrickallaert/php-apm/master/LICENSE

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%if %{with_phpfpm}
Requires:       webserver
Requires:       nginx-filesystem
Requires:       httpd-filesystem
Requires:       php(httpd)
%else
Requires:       httpd
Requires:       mod_php
%endif
# From phpcompatinfo analysis
Requires:       php(language) > 5.3
Requires:       php-date
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo

# This is not a library, but a web-app, so doesn't really make sense
Provides:       php-composer(patrickallaert/php-apm-web) = %{version}


%description
APM (Alternative PHP Monitor) is a monitoring extension enabling native
Application Performance Management (APM) for PHP.

This is the web frontend that enables visualizing the data gathered by
that extension.

The php-pecl-apm package provides the extension.


%prep
%setup -q -n %{gh_name}-%{gh_commit}

: Fix configuration path
sed -e 's:"config/db.php":"%{_sysconfdir}/apm-web/db.php":' \
    -i model/repository.php

: Create webserver configuration files
sed -e 's:@ALIAS@:%{name}:g' \
    -e 's:@SHARE@:%{_datadir}:g' \
    %{SOURCE1} > %{name}.httpd

%if %{with_phpfpm}
sed -e 's:@ALIAS@:%{name}:g' \
    -e 's:@SHARE@:%{_datadir}:g' \
    %{SOURCE2} > %{name}.nginx
%endif

cp %{SOURCE3} .


%build
# Nothing


%install
install -d %{buildroot}%{_datadir}/%{name}
cp -pr css img js model plugins views *php \
   %{buildroot}%{_datadir}/%{name}

# Apache config
install -D -m 644 %{name}.httpd \
   %{buildroot}%{_sysconfdir}/httpd/conf.d/%{name}.conf

%if %{with_phpfpm}
# Nginx config
install -Dpm 0644 %{name}.nginx \
   %{buildroot}/%{_sysconfdir}/nginx/default.d/%{name}.conf
%endif

# Application config
install -D -m 644 -p config/db.php \
 %{buildroot}%{_sysconfdir}/%{name}/db.php


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
# Need to restrict access, as it contains a clear password
%attr(750,root,apache) %dir %{_sysconfdir}/%{name}
%attr(640,root,apache) %config(noreplace) %{_sysconfdir}/%{name}/db.php
%{_datadir}/%{name}
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%if %{with_phpfpm}
%config(noreplace) %{_sysconfdir}/nginx/default.d/%{name}.conf
%endif


%changelog
* Sat Feb 21 2015 Remi Collet <remi@fedoraproject.org> - 2.0.0-3
- initial package, version 2.0.0 (split off php-pecl-apm)