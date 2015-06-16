%global git_tag_rev bb892a53a76116ad0982445a849043687cb6e778

Name:		php-wikimedia-utfnormal
Version:	1.0.2
Release:	1%{?dist}
Summary:	Unicode normalization functions

License:	GPLv2+
URL:		http://www.mediawiki.org/wiki/Utfnormal
Source0:	http://git.wikimedia.org/zip/?r=utfnormal.git&format=xz&h=%{git_tag_rev}#/%{name}-%{version}.tar.xz
Source1:	gpl-2.0.txt

Buildarch:	noarch

Requires:	php(language) >= 5.3.3

Provides:	php-composer(wikimedia/utfnormal) = %{version}


%description
utfnormal is a library that contains unicode normalization functions. It was
split out of MediaWiki core during the 1.25 development cycle.


%prep
%setup -qc %{name}-%{version}


%build


%install
cp -p %{SOURCE1} COPYING
mkdir -pm 0755 %{buildroot}%{_datadir}/php/UtfNormal
cp -rp src/* %{buildroot}%{_datadir}/php/UtfNormal


%files
%license COPYING
%doc composer.json README.md
%{_datadir}/php/UtfNormal


%changelog
* Mon Jun 15 2015 Michael Cronenworth <mike@cchtml.com> - 1.0.2-1
- Initial package

