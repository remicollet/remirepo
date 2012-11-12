%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channelname pear.sabredav.org

Name:       php-channel-sabredav
Version:    1.3
Release:    3%{?dist}
Summary:    Adds the SabreDAV channel to PEAR

Group:      Development/Languages
License:    Public Domain
URL:        http://code.google.com/p/sabredav
Source0:    http://pear.sabredav.org/channel.xml

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch
BuildRequires: php-pear

Requires:   php-pear(PEAR)
Requires(post):     %{__pear}
Requires(postun):   %{__pear}

Provides:   php-channel(%{channelname})


%description
This package adds the SabreDAV channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{channelname}.xml


%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/%{channelname}.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/%{channelname}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete %{channelname} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{channelname}.xml


%changelog
* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.3-3
- backport for remi repo

* Mon Oct 01 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.3-3
- remove rm -rf %%BUILDROOT from install
- change licence to public domain
* Sun Sep 12 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.3-2
- removed uneaded %%clean section and submited for package review
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.3-1
- initial package
