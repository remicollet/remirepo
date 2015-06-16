# remirepo spec file for php-wikimedia-utfnormal, from Fedora
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global git_tag_rev bb892a53a76116ad0982445a849043687cb6e778

Name:		php-wikimedia-utfnormal
Version:	1.0.2
Release:	1%{?dist}
Summary:	Unicode normalization functions
Group:		Development/Libraries

License:	GPLv2+
URL:		http://www.mediawiki.org/wiki/Utfnormal
Source0:	http://git.wikimedia.org/zip/?r=utfnormal.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz
Source1:	gpl-2.0.txt

Buildarch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	%{_bindir}/phpunit
BuildRequires:	%{_bindir}/phpab

Requires:	php(language) >= 5.3.3
# From phpcompatinfo report for 1.0.2
Requires:	php-intl
Requires:	php-pcre
Requires:	php-spl

Provides:	php-composer(wikimedia/utfnormal) = %{version}


%description
utfnormal is a library that contains unicode normalization functions. It was
split out of MediaWiki core during the 1.25 development cycle.


%prep
%setup -qc %{name}-%{version}

cp -p %{SOURCE1} COPYING


%build
: Generate an simple "classmap" autoloader
%{_bindir}/phpab \
    --output src/autoload.php \
    src


%install
rm -rf %{buildroot}

mkdir -pm 0755 %{buildroot}%{_datadir}/php/UtfNormal
cp -rp src/* %{buildroot}%{_datadir}/php/UtfNormal


%check
: Run upstream test suite
%{_bindir}/phpunit \
    --bootstrap=%{buildroot}%{_datadir}/php/UtfNormal/autoload.php \
    --verbose


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc composer.json README.md
%{_datadir}/php/UtfNormal


%changelog
* Tue Jun 16 2015 Remi Collet <remi@remirepo.net> - 1.0.2-1
- add backport stuff for remirepo
- run test suite during build

* Mon Jun 15 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.2-1
- Initial package

