%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Swift

Name:           php-swift-Swift
Version:        4.1.3
Release:        1%{?dist}
Summary:        Free Feature-rich PHP Mailer

Group:          Development/Libraries
License:        LGPLv3
URL:            http://www.swiftmailer.org/
Source0:        http://pear.swiftmailer.org/get/Swift-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-channel(pear.swiftmailer.org)
BuildRequires:  php-pear(PEAR)
Requires:       php >= 5.2.4
Requires:       php-pear(PEAR) >= 1.3.6
Requires:       php-channel(pear.swiftmailer.org)
Requires:       php-pdo
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(pear.swiftmailer.org/%{pear_name}) = %{version}

%description

Swift Mailer integrates into any web app written in PHP 5, offering a 
flexible and elegant object-oriented approach to sending emails with 
a multitude of features.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{pear_name}.xml
cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

mkdir -p $RPM_BUILD_ROOT%{pear_phpdir}/tmp
mv $RPM_BUILD_ROOT%{pear_phpdir}/*.php \
   $RPM_BUILD_ROOT%{pear_phpdir}/Swift \
   $RPM_BUILD_ROOT%{pear_phpdir}/dependency_maps \
   $RPM_BUILD_ROOT%{pear_phpdir}/tmp
mv $RPM_BUILD_ROOT%{pear_phpdir}/tmp $RPM_BUILD_ROOT%{pear_phpdir}/Swift

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{pear_name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


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
