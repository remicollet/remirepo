# spec file for php-channel-nrk
#
# Copyright (c) 2013-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the %changelog entries
#
%global channel pear.nrk.io
Name:           php-channel-nrk
# REST version
Version:        1.3
Release:        1%{?dist}
Summary:        Adds pear.nrk.io channel to PEAR

Group:          Development/Languages
License:        Public Domain
URL:            http://%{channel}/
Source0:        http://%{channel}/channel.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear

Requires:       php-pear(PEAR)
Requires(post): /usr/bin/pear
Requires(postun): /usr/bin/pear

Provides:       php-channel(%{channel})

%description
This package adds the %{channel} channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{channel}.xml


%clean
rm -rf %{buildroot}


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/%{channel}.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/%{channel}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete %{channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{channel}.xml


%changelog
* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 1.3-1
- Initial package
