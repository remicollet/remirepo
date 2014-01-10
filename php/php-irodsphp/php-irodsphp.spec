%global packagename irodsphp

Name:      php-%{packagename}
Version:   3.3.0
Release:   0.3.beta1%{?dist}
Summary:   PHP client API for iRODS

Group:     Development/Libraries
License:   BSD
URL:       https://code.renci.org/gf/project/irodsphp/
Source0:   https://code.renci.org/gf/download/frsrelease/167/1674/php-%{version}-beta1.zip
Patch0:    php-irodsphp-3.3.0-configpath.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

Requires:  php(language) >= 5.1.2
# phpcompatinfo (computed from v3.3.0-beta1)
Requires:  php-date
Requires:  php-dom
Requires:  php-simplexml
Requires:  php-libxml
Requires:  php-pcre
Requires:  php-spl

# Gratefully borrowed from Debian
%description
PRODS is a PHP client API for iRODS (http://www.irods.org). It talks to
an iRODS server directly via sockets with a native iRODS XML protocol.

%prep
%setup -q -c %{name}
# wrong-file-end-of-line-encoding just about everywhere
find -name \*.php | xargs sed -i 's/\r$//'
find -name \*.txt | xargs sed -i 's/\r$//'
find -name \*.ini | xargs sed -i 's/\r$//'
# strip a stray source control dir and docbook source file
rm -rf prods/tutorials/Prods/.svn
rm -f prods/tutorials/Prods/Prods.pkg
%patch0 -p1 -b .configpath

%build
# no build required

%install
rm -rf %{buildroot}

# For now, just installing the key bit of prods. If anyone sees value
# in packaging the tests or the webapp...I'm not stopping you.

mkdir -p %{buildroot}%{_datadir}/php/%{packagename}/prods
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
cp -pr prods/src %{buildroot}%{_datadir}/php/%{packagename}/prods
mv %{buildroot}%{_datadir}/php/%{packagename}/prods/src/prods.ini %{buildroot}%{_sysconfdir}/%{name}
rm -f %{buildroot}%{_datadir}/php/%{packagename}/prods/src/LICENSE.txt %{buildroot}%{_datadir}/php/%{packagename}/prods/src/release_notes.txt


%clean
rm -rf %{buildroot}


%check
# Needs a reference iRODS instance to test sensibly, which we don't
# have

%files
%defattr(-,root,root,-)
%doc prods/src/LICENSE.txt prods/release_notes.txt prods/tutorials prods/utilities
%{_datadir}/php/%{packagename}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/prods.ini

%changelog
* Fri Jan 10 2014 Remi Collet <rrpms@fedoraproject.org> - 3.3.0-0.3.beta1
- backport for remi repo.

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 3.3.0-0.3.beta1
- fix up the requires per review
- drop the complex naming and just call it php-irodsphp
- make the naming and paths a bit more consistent

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 3.3.0-0.2.beta1
- package tutorials and utilities as docs
- relocate configuration file to /etc/irods-prods/prods.ini
- fix line endings with sed, in prep
- layout matches upstream (and Debian) more closely

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 3.3.0-0.1.beta1
- Initial package

