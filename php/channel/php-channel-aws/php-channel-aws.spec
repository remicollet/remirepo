%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channelname pear.amazonwebservices.com

Name:       php-channel-aws
Version:    1.3
Release:    3%{?dist}
Summary:    Adds the Amazon Web Services channel to PEAR

Group:      Development/Languages
License:    Public Domain
URL:        http://aws.amazon.com/sdkforphp
Source0:    http://pear.amazonwebservices.com/channel.xml

BuildArch:  noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:   php-pear(PEAR)
Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Provides:   php-channel(%{channelname})

%description
This package adds the Amazon Web Services channel which allows PEAR packages
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
%{pear_xmldir}/%{channelname}.xml


%changelog
* Mon Dec 17 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.3-3
- fix mixed use of tabs and spaces
- eliminate macro in the changelog
* Thu Nov 13 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.3-2
- set licence to public domain
- fix channel name in global from http://pear.amazonwebservices.com/ to pear.amazonwebservices.com
- remove clean section.
* Tue Sep 11 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.3-1
- initial package
