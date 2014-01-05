%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channelname phpseclib.sourceforge.net

Name:       php-channel-phpseclib
Version:    1.3
Release:    1%{?dist}
Summary:    Adds the phpseclib channel to PEAR

Group:      Development/Languages
License:    Public Domain
URL:        http://phpseclib.sourceforge.net/
Source0:    http://phpseclib.sourceforge.net/channel.xml

BuildArch:           noarch
BuildRequires:       php-pear
Requires:            php-pear(PEAR)
Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Provides:            php-channel(%{channelname})

%description
This package adds the phpseclib channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T
# fix line endings
sed -i 's/\r$//' %{SOURCE0}


%build
# Empty build section, nothing to build


%install
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml


%post
if [ $1 -eq  1 ] ; then
%{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
%{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
%{__pear} channel-delete %{channelname} > /dev/null || :
fi


%files
%{pear_xmldir}/%{name}.xml


%changelog
* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 1.3-1
- version using the rest version
- drop use of tabs
- drop unnecessary versioning of the buildrequires


* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 1.0-1
- initial package

