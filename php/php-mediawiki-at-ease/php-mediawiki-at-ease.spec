# remirepo spec file for php-mediawiki-at-ease, from:
#
# Fedora spec file for php-mediawiki-at-ease
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global git_tag_rev 94c0b84888841d160419f915c2745d9d08fbf0c3

Name:		php-mediawiki-at-ease
Version:	1.1.0
Release:	1%{?dist}
Summary:	Safe replacement to @ for suppressing warnings
Group:		Development/Libraries

License:	GPLv2+
URL:		http://www.mediawiki.org/wiki/at-ease
Source0:	http://git.wikimedia.org/zip/?r=at-ease.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

BuildRequires:	php-phpunit-PHPUnit

Requires:	php(language) >= 5.3.0

Provides:	php-composer(mediawiki/at-ease) = %{version}


%description
at-ease is a PHP library that provides a safe alternative to PHP's @ error 
control operator. See Manual:Coding conventions/PHP#Error handling on why 
we don't use @. The code was originally introduced to MediaWiki in r4261, 
and then split out into a separate library during the MediaWiki 1.26 
development cycle.


%prep
%setup -qc %{name}-%{version}


%build


%install
rm -rf %{buildroot}

mkdir -pm 0755 %{buildroot}%{_datadir}/php/MediaWiki/at-ease
cp -rp src/* %{buildroot}%{_datadir}/php/MediaWiki/at-ease


%check
phpunit -v --bootstrap %{buildroot}%{_datadir}/php/MediaWiki/at-ease/Functions.php


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc composer.json README.md
%{_datadir}/php/MediaWiki


%changelog
* Mon Oct  5 2015 Remi Collet <remi@remirepo.net> - 1.1.0-1
- add backport stuff

* Wed Sep 30 2015 Michael Cronenworth <mike@cchtml.com> - 1.1.0-1
- Initial package

