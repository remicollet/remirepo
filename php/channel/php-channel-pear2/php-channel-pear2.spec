%global channel pear2.php.net

Name:           php-channel-pear2
# Use Provided REST version 
Version:        1.3
Release:        1
Summary:        Adds pear2.php.net channel to PEAR

Group:          Development/Languages
License:        Public domain
URL:            http://pear2.php.net/
Source0:        http://pear2.php.net/channel.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.4.7

Requires:       php-pear(PEAR)
Provides:       php-channel(%{channel})

%description
This package adds the pear2.php.net channel which allows PEAR packages
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
* Sun Feb 26 2012 Remi Collet <remi@fedoraproject.org> - 1.3-1
- initial RPM.


