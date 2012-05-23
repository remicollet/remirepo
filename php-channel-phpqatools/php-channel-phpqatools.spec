%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-channel-phpqatools
# Use REST version (from channel.xml)
Version:	1.3
Release:	3%{?dist}
Summary:	Adds phpqatools channel to PEAR

Group:		Development/Languages
License:	Public Domain
URL:		http://phpqatools.org/
Source0:	http://pear.phpqatools.org/channel.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2
Requires:	php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-channel(pear.phpqatools.org)

%description
This package adds the phpqatools channel which allows
PEAR packages from this channel to be installed.

%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.phpqatools.org.xml


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/pear.phpqatools.org.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/pear.phpqatools.org.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete pear.phpqatools.org > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Mon May 21 2012 Christof Damian <christof@damian.net> - 1.3-3
- removed php-cli require

* Sun May 20 2012 Christof Damian <christof@damian.net> - 1.3-2
- Changed license after talking to Sebastian Bergmann
- removed some command macros

* Tue Apr 24 2012 Christof Damian <christof@damian.net> - 1.3-1
- Initial RPM release.
