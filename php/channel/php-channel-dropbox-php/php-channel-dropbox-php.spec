%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channelname pear.dropbox-php.com

Name:           php-channel-dropbox-php
Version:        1.3
Release:        3%{?dist}
Summary:        Adds the Dropbox-PHP channel to PEAR

License:        Public Domain
URL:            http://www.dropbox-php.com/
Source0:        http://%{channelname}/channel.xml

BuildArch:  noarch
BuildRequires:  php-pear(PEAR)
Requires:   php-pear(PEAR)
Requires(post):     %{__pear}
Requires(postun):   %{__pear}
Provides:   php-channel(%{channelname})

%description
This package adds the Dropbox-PHP channel which allows PEAR packages
from this channel to be installed.

%prep
%setup -q -c -T


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
* Thu Feb 28 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.3-3
- channelname: pear.dropbox-php.com

* Wed Feb 27 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.3-2
- install channel.xml as %%{name}

* Tue Feb 19 2013 Gregor Tätzner <brummbq@fedoraproject.org> - 1.3-1
- Initial package