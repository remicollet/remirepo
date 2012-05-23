%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-channel-digitalsandwich
# Use REST version (from channel.xml)
Version:	1.3
Release:	2%{?dist}
Summary:	Adds digitalsandwich channel to PEAR

Group:		Development/Languages
License:	Public Domain
URL:		http://digitalsandwich.com/
Source0:	http://pear.digitalsandwich.com/channel.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2
Requires:	php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-channel(pear.digitalsandwich.com)

%description
This package adds the digitalsandwich channel which allows
PEAR packages from this channel to be installed.

%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.digitalsandwich.com.xml


%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/pear.digitalsandwich.com.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/pear.digitalsandwich.com.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete pear.digitalsandwich.com > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Mon May 21 2012 Christof Damian <christof@damian.net> - 1.3-2
- fixes for review:
- remove php-cli from requires
- change license to Public Domain
- clean unneeded macros (rm, install, mkdir)

* Wed May  2 2012 Christof Damian <christof@damian.net> - 1.3-1
- initial release

