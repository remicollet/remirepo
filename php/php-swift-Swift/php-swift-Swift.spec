%{!?__pear: %global __pear %{_bindir}/pear}
%global pear_name Swift

Name:           php-swift-Swift
Version:        5.1.0
Release:        1%{?dist}
Summary:        Free Feature-rich PHP Mailer

Group:          Development/Libraries
License:        MIT
URL:            http://www.swiftmailer.org/
Source0:        http://pear.swiftmailer.org/get/Swift-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-channel(pear.swiftmailer.org)
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.2.4
Requires:       php-pear(PEAR)
Requires:       php-channel(pear.swiftmailer.org)
# from phpcompatinfo report on version 5.1.0
Requires:       php-bcmath
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-mhash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl

# optional but not yet available https://github.com/xdecock/php-opendkim

Provides:       php-pear(pear.swiftmailer.org/%{pear_name}) = %{version}

%description
Swift Mailer integrates into any web app written in PHP 5, offering a 
flexible and elegant object-oriented approach to sending emails with 
a multitude of features.


%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{pear_name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{pear_name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

mkdir -p %{buildroot}%{pear_phpdir}/tmp
mv %{buildroot}%{pear_phpdir}/*.php \
   %{buildroot}%{pear_phpdir}/Swift \
   %{buildroot}%{pear_phpdir}/dependency_maps \
   %{buildroot}%{pear_phpdir}/tmp
mv %{buildroot}%{pear_phpdir}/tmp %{buildroot}%{pear_phpdir}/Swift

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{pear_name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{pear_name}.xml
%{pear_phpdir}/%{pear_name}

%changelog
* Tue Mar 18 2014 Remi Collet <remi@fedoraproject.org> - 5.1.0-1
- Update to 5.1.0 (stable)
- add dependencies on bcmath, mcrypt and mhash

* Tue Dec 03 2013 Remi Collet <remi@fedoraproject.org> - 5.0.3-1
- Update to 5.0.3 (stable)

* Fri Aug 30 2013 Remi Collet <remi@fedoraproject.org> - 5.0.2-1
- Update to 5.0.2

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1

* Sat May 25 2013 Remi Collet <remi@fedoraproject.org> - 5.0.0-1
- Update to 5.0.0 (relicense under MIT)

* Thu Apr 11 2013 Remi Collet <remi@fedoraproject.org> - 4.3.1-1
- Update to 4.3.1

* Tue Jan  8 2013 Remi Collet <RPMS@FamilleCollet.com> - 4.3.0-1
- upstream 4.3.0

* Fri Oct 26 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.2.2-1
- upstream 4.2.2

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.2.1-1
- upstream 4.2.1, backport for remi repository

* Fri Jul 13 2012 Christof Damian <christof@damian.net> - 4.2.1-1
- upstream 4.2.1

* Sun Apr 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.7-1
- upstream 4.1.7, rebuild for remi repository

* Sat Apr 28 2012 Christof Damian <christof@damian.net> - 4.1.7-1
- upstream 4.1.7

* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.6-1
- upstream 4.1.6, rebuild for remi repository

* Sat Mar 24 2012 Christof Damian <christof@damian.net> - 4.1.6-1
- upstream 4.1.6

* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 4.1.5-1
- upstream 4.1.5, rebuild for remi repository

* Sat Mar  3 2012 Christof Damian <christof@damian.net> - 4.1.5-1
- upstream 4.1.5

* Tue Nov 01 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.1.3-1
- rebuild for remi repository

* Fri Oct 28 2011 Christof Damian <christof@damian.net> - 4.1.3-1
- upstream 4.1.3

* Sat Jul 16 2011 Remi Collet <RPMS@FamilleCollet.com> - 4.1.1-1
- rebuild for remi repository
- doc in /usr/share/doc/pear

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 4.1.1-1
- upstream 4.1.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 13 2010 Remi Collet <RPMS@FamilleCollet.com> - 4.0.6-1
- rebuild for remi repository

* Wed May 12 2010 Christof Damian <christof@damian.net> - 4.0.6-1
- upstream 4.0.6 (bugfixes)

* Tue Dec 1 2009 Christof Damian <christof@damian.net> 4.0.5-1
- initial rpm
