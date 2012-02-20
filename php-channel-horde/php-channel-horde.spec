Name:           php-channel-horde
Version:        1.0
Release:        1%{?dist}
Summary:        Adds pear.horde.org channel to PEAR

Group:          Development/Languages
License:        Public Domain
URL:            http://pear.horde.org/
Source0:        http://pear.horde.org/channel.xml

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR)
Requires(post): /usr/bin/pear
Requires(postun): /usr/bin/pear
Provides:       php-channel(pear.horde.org)

%description
This package adds the pear.horde.org channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/pear.horde.org.xml


%clean
rm -rf $RPM_BUILD_ROOT


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/pear.horde.org.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/pear.horde.org.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete pear.horde.org > /dev/null || :
fi


%files
%{pear_xmldir}/pear.horde.org.xml

%changelog
* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0-1
- Initial package
