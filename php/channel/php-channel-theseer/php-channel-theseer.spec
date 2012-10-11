%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global channel pear.netpirates.net

Name:           php-channel-theseer
# Use REST version
Version:        1.3
Release:        1%{?dist}
Summary:        Adds theseer channel to PEAR

Group:          Development/Languages
License:        BSD
URL:            http://%{channel}/
Source0:        http://%{channel}/channel.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires:       php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-channel(%{channel})

%description
This package adds the pear.netpirates.net (theseer) channel which allows
PEAR packages from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{name}.xml


%clean
rm -rf %{buildroot}


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
* Wed Feb 25 2011 Remi Collet <remi@fedoraproject.org> - 1.3-1
- Initial Release

