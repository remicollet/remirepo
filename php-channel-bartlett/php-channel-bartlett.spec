%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global channel bartlett.laurent-laville.org

Name:           php-channel-bartlett
# Use REST version
Version:        1.3
Release:        1%{?dist}
Summary:        Adds bartlett channel to PEAR

Group:          Development/Languages
License:        BSD
URL:            http://%{channel}/
Source0:        http://%{channel}/channel.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2

Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-channel(%{channel})

%description
This package adds the bartlett channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete %{channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.3-1
- Initial Release

