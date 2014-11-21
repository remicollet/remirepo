#
# RPM spec file for php-psr-http-message
#
# Copyright (c) 2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     php-fig
%global github_name      http-message
%global github_version   0.5.1
%global github_commit    18619eee10ecf266bafe048e5a2922fa20938498

%global composer_vendor  psr
%global composer_project http-message

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:      php-%{composer_vendor}-%{composer_project}
Version:   %{github_version}
Release:   1%{?github_release}%{?dist}
Summary:   Common interface for HTTP messages (PSR-7)

Group:     Development/Libraries
License:   MIT
URL:       https://github.com/%{github_owner}/%{github_name}
Source0:   %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

# phpcompatinfo (computed from version 0.5.1)
Requires:  php(language) >= 5.3.0

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
This package holds all interfaces/classes/traits related to PSR-7.

Note that this is not a HTTP message implementation of its own. It is merely an
interface that describes a HTTP message. See the specification for more details.


%prep
%setup -qn %{github_name}-%{github_commit}

# W: spurious-executable-perm /usr/share/doc/php-psr-http-message/README.md
# W: spurious-executable-perm /usr/share/doc/php-psr-http-message/composer.json
# E: script-without-shebang /usr/share/licenses/php-psr-http-message/LICENSE
# https://github.com/php-fig/http-message/pull/10
chmod a-x README.md composer.json LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}/Psr/Http/Message
cp -rp src/* %{buildroot}%{phpdir}/Psr/Http/Message/


%check
# No tests provided by upstream


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{phpdir}/Psr
%dir %{phpdir}/Psr/Http
     %{phpdir}/Psr/Http/Message


%changelog
* Thu Nov 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.5.1-1
- Updated to 0.5.1 (BZ #1163322)

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 0.4.0-1
- backport for remi repository

* Thu Oct 30 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 0.4.0-1
- Initial package
