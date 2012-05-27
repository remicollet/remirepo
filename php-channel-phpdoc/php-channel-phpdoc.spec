%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-channel-phpdoc
# Use REST version (from channel.xml)
Version:	1.3
Release:	3%{?dist}
Summary:	Adds phpdoc channel to PEAR

Group:		Development/Languages
License:	Public Domain
URL:		http://phpdoc.org/
Source0:	http://pear.phpdoc.org/channel.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2
Requires:	php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-channel(pear.phpdoc.org)

%description
This package adds the phpdoc channel which allows
PEAR packages from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.phpdoc.org.xml


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/pear.phpdoc.org.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/pear.phpdoc.org.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete pear.phpdoc.org > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Mon May 21 2012 Christof Damian <christof@damian.net> - 1.3-3
- replaced channel.xml with correct one

* Mon May 21 2012 Christof Damian <christof@damian.net> - 1.3-2
- fixes for review:
- remove php-cli from requires
- change license to Public Domain
- clean unneeded macros (rm, install, mkdir)

* Sat Mar 24 2012 Christof Damian <christof@damian.net> - 1.3-1
- Initial RPM release.
