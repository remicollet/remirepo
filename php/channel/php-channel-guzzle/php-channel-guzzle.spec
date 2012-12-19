%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel guzzlephp.org/pear

Name:             php-channel-guzzle
Version:          1.3
Release:          1%{?dist}
Summary:          Adds %{pear_channel} channel to PEAR

Group:            Development/Libraries
License:          Public Domain
URL:              http://%{pear_channel}
Source0:          http://%{pear_channel}/channel.xml

BuildArch:        noarch
BuildRequires:    php-pear(PEAR)

Requires:         php-pear(PEAR)
Requires(post):   %{__pear}
Requires(postun): %{__pear}

Provides:         php-channel(%{pear_channel})

%description
This package adds the %{pear_channel} channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{SOURCE0} %{buildroot}%{pear_xmldir}/%{name}.xml


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null || :
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete %{pear_channel} > /dev/null || :
fi


%files
%{pear_xmldir}/%{name}.xml


%changelog
* Sat Dec  8 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3-1
- Initial package (version matches channel REST version)
