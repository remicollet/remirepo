%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Summary:           Adds the PearPlex channel to PEAR
Name:              php-channel-pearplex
# Use REST version
Version:           1.3
Release:           2%{?dist}
License:           Public Domain
Group:             Development/Languages
URL:               http://www.pearplex.net/
Source:            http://pear.pearplex.net/channel.xml
Requires:          php-pear(PEAR)
Requires(post):    %{__pear}
Requires(postun):  %{__pear}
Provides:          php-channel(pear.pearplex.net)
BuildRequires:     php-pear >= 1:1.4.9-1.2
BuildArch:         noarch
BuildRoot:         %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This package adds the PearPlex channel which allows PEAR packages
from this channel to be installed.

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT
install -D -p -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq 1 ]; then
  %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
  %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi

%postun
if [ $1 -eq 0 ]; then
  %{__pear} channel-delete pear.pearplex.net > /dev/null || :
fi

%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml

%changelog
* Sun Aug 21 2011 Remi Collet <RPMS@FamilleCollet.com> 1.3-2
- rebuild for remi repository

* Sun Jul 31 2011 Robert Scheck <robert@fedoraproject.org> 1.3-2
- Corrected undefined macro in %%postun scriptlet (#725914 #c1)

* Wed Jul 27 2011 Robert Scheck <robert@fedoraproject.org> 1.3-1
- Upgrade to 1.3
- Initial spec file for Fedora and Red Hat Enterprise Linux
