# spec file for php-channel-horde
#
# Copyright (c) 2012-2015 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{?scl:         %scl_package        php-channel-horde}
%{!?__pear:     %global __pear      %{_bindir}/pear}
%global pear_channel pear.horde.org

Name:           %{?scl_prefix}php-channel-horde
Version:        1.0
Release:        2%{?dist}
Summary:        Adds %{pear_channel} channel to PEAR

Group:          Development/Languages
License:        Public Domain
URL:            http://www.horde.org/
Source0:        http://%{pear_channel}/channel.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  %{?scl_prefix}php-pear

Requires:       %{?scl_prefix}php-pear(PEAR)
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       %{?scl_prefix}php-channel(%{pear_channel})

%description
This package adds the %{pear_channel} channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf %{buildroot}
install -Dpm 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{name}.xml


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
   %{__pear} channel-delete %{pear_channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Mon Sep 15 2014 Remi Collet <remi@fedoraproject.org> - 1.0-2
- allow SCL build

* Mon Feb 20 2012 Remi Collet <remi@fedoraproject.org> - 1.0-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0-1
- Initial package
