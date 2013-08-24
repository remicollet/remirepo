%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%define pear_name Auth_OpenID

Name: php-pear-Auth-OpenID
Version: 2.2.2
Release: 7%{?dist}
Summary: PHP OpenID
Group: Development/System
License: ASL 2.0
URL: http://www.janrain.com/openid-enabled
# php-pear-Auth-OpenID is now hosted on github
# https://github.com/openid/php-openid
# downloading the tarball and repacking it from 
# openid-php-openid-2.2.2-0-ga287b2d.tar.gz to php-openid-2.2.2.tar.bz2
Source0: php-openid-%{version}.tar.bz2

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: php-pear >= 1:1.4.9-1.2
BuildRequires: python
Requires: php-pear(PEAR)
Requires(post): php-pear
Requires(postun): php-pear
# Required for testing, but we need PHPUnit 1.x
#Requires: php-pear-PHPUnit >= 1.1.1
# part of the pear spec, but the version makes no sense
#Requires: php-pear-DB >= 1.80
Requires: php-pgsql
Requires: php-mysql
#Requires: php-sqlite
Requires: php-bcmath
Requires: php-pear-Net-Curl
Provides: php-pear(%{pear_name}) = %{version}

# This patch fixes the paths from Auth -> Auth_OpenID
Patch0: php-openid-2.2.2-requires-paths.patch

# Patch for CVE-2013-4701
# https://github.com/openid/php-openid/commit/625c16bb28bb120d262b3f19f89c2c06cb9b0da9
Patch1: php-openid-2.2.2-cve-2013-4701.patch

%description
An implementation of the OpenID single sign-on authentication
protocol.

%prep
%setup -q -n php-openid-%{version}
#
# needed so we can execute packagexml.py
#
chmod +x admin/packagexml.py
admin/packagexml.py %{version} admin/package2.xml README > %{pear_name}.xml

# Fix the paths from Auth -> Auth_OpenID
%patch0 -p1
%patch1 -p1

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{pear_phpdir}/%{pear_name}/OpenID \
         %{buildroot}/%{pear_phpdir}/%{pear_name}/Yadis
pear install --nodeps --packagingroot %{buildroot} %{pear_name}.xml
# The pear install is not yet complete, so we need to manually move in
# some parts
cp -a Auth/*.php %{buildroot}/%{pear_phpdir}/%{pear_name}/
cp -a Auth/OpenID/*.php %{buildroot}/%{pear_phpdir}/%{pear_name}/OpenID/
cp -a Auth/Yadis/*.php %{buildroot}/%{pear_phpdir}/%{pear_name}/Yadis/

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}

%clean
rm -rf %{buildroot}

%post
pear install --nodeps --offline --soft --force --register-only \
  %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  pear uninstall --nodeps --ignore-errors --register-only \
  %{pear_name} >/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc NEWS COPYING README examples

%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/%{pear_name}

%changelog
* Sat Aug 24 2013 Remi Collet <remi@fedoraproject.org> 2.2.2-7
- backport rawhide changes for remi repo

* Fri Aug 23 2013 Kevin Fenzi <kevin@scrye.com> 2.2.2-7
- Patch for CVE-2013-4701

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 22 2013 Kevin Fenzi <kevin@scrye.com> 2.2.2-5
- Fixed pear metadata directory location. Fixes FTBFS bug 914351

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Mar 22 2011 Kurt Seifried <kurt@seifried.org> - 2.2.2-1
- Upgrade to 2.2.2
- Corrected file paths for Fedora
- Corrected chmod +x admin/packagexml.py

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug  1 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.1-6
- Change documentation handling to use %%doc.

* Wed Jul 30 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1.1-5
- Upgrade to 2.1.1.
- Use php_dir instead of data_dir (Rakesh Pandit <rakesh.pandit@gmail.com>)
- Fix CRLF (Peter Lemenkov <lemenkov@gmail.com> & R. Pandit)

* Sun Feb 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.0.1-4
- Update to 2.0.1.
- Change license.
- PEAR install method has regressed, some manual fixes are neccessary.
- No testing done (needs too old PHPUnit).

* Sat Feb 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.3-3
- Update to 1.2.3.
- Dropped PHPUnit 1.x dependency.

* Mon Aug  6 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.2-2
- Update to 1.2.2.

* Thu Feb  1 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 1.2.1-1
- Initial build.

