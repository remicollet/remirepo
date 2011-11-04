%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name     PHP_CodeSniffer
%global pear_version  1.3.1

Name:           php-pear-PHP-CodeSniffer
Version:        %{pear_version}
Release:        1%{?dist}
Summary:        PHP coding standards enforcement tool

Group:          Development/Tools
License:        BSD
URL:            http://pear.php.net/package/PHP_CodeSniffer
Source0:        http://pear.php.net/get/%{pear_name}-%{pear_version}.tgz
#Source1:        PHP_CodeSniffer-licence.txt
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
Requires:       php-pear(PEAR)
Requires:       php-common >= 5.1.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.phpunit.de/PHP_Timer) >= 1.0.0
Provides:       php-pear(%{pear_name}) = %{version}
Provides:       phpcs = %{version}
Obsoletes:      phpcs < %{version}

%description
PHP_CodeSniffer provides functionality to verify that code conforms to
certain standards, such as PEAR, or user-defined.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{pear_version}/%{pear_name}.xml

cd %{pear_name}-%{pear_version}

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

%build
# Empty build section, 


%install
cd %{pear_name}-%{pear_version}
rm -rf $RPM_BUILD_ROOT docdir

PHPRC=./php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}.xml

# Move documentation
mkdir -p docdir
mv $RPM_BUILD_ROOT%{pear_datadir}/%{pear_name}/*.sample.conf docdir/

# Remove phpcs-svn-pre-commit: we'll add it to docs
mv  -f $RPM_BUILD_ROOT%{_bindir}/scripts/phpcs-svn-pre-commit .
chmod 0644 phpcs-svn-pre-commit
rm -rf $RPM_BUILD_ROOT%{_bindir}/scripts

#cp %{SOURCE1} .

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

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
#%doc %{pear_name}-%{pear_version}/PHP_CodeSniffer-licence.txt 
%doc %{pear_name}-%{pear_version}/phpcs-svn-pre-commit
%doc %{pear_name}-%{pear_version}/docdir/*
%{pear_xmldir}/%{pear_name}.xml
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/PHP
%{_bindir}/phpcs

%changelog
* Fri Nov 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-1
- upstream 1.3.1, rebuild for remi repository

* Thu Nov  3 2011 Christof Damian <christof@damian.net> - 1.3.1-1
- upstream 1.3.1

* Thu Mar 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0final-1
- rebuild for remi repository

* Fri Mar 18 2011 Christof Damian <christof@damian.net> - 1.3.0final-1
- fix my version foo until 1.3.1

* Fri Mar 18 2011 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0 final

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.3.0-2.RC1
- rebuild for remi repository

* Sat Dec  4 2010 Christof Damian <christof@damian.net> - 1.3.0-2.RC1
- fix version number 
- fix timezone warnings

* Fri Sep  3 2010 Christof Damian <christof@damian.net> - 1.3.0RC1-1
- upstream 1.3.0RC1

* Thu Jul 15 2010 Christof Damian <christof@damian.net> - 1.3.0a1-1
- upstream 1.3.0a1

* Fri Jan 29 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-1
- rebuild for remi repository

* Wed Jan 27 2010 Christof Damian <christof@damian.net> 1.2.2-1
- upstream 1.2.2 ( bug:559170 )
- move phpcs into main package ( bug: 517775 )
- add php-common version requirement

* Thu Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repository

* Tue Nov 17 2009 Christof Damian <christof@damian.net> - 1.2.1-1
- Upstream 1.2.1

* Sat Sep 26 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- rebuild for remi repository

* Sat Sep 19 2009 Christof Damian <christof@damian.net> - 1.2.0-1
- Upstream 1.2.0

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-1
- rebuild for remi repository

* Thu Mar 05 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.1.0-1
- Belatedly update to 1.1.0 final.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.2.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jun 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.1.0-0.1.RC2
- Upstream 1.1.0RC2

* Sun Feb 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 1.0.1-1
- Upstream 1.0.1
- Move sample config into docs

* Fri Aug 17 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.8.0-1
- Upstream 0.8.0

* Mon Jun 11 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.7.0-1
- Upstream 0.7.0
- Drop Requirement on php-common (php-pear pulls that in)

* Mon Jun 11 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.6.0-1
- Upstream 0.6.0
- Fix owner on phpcs

* Tue Apr 17 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.5.0-1
- Upstream 0.5.0

* Tue Feb 20 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.4.0-1
- Upstream 0.4.0

* Mon Jan 29 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.3.0-1
- Rename to php-pear-PHP-CodeSniffer
- Own all dirs we create
- Require php-common > 5.1.0

* Mon Jan 29 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.3.0-1
- Split phpcs into a separate package (so we don't require php-cli)

* Fri Jan 12 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.3.0-0.1
- Upstream 0.3.0

* Mon Oct 23 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.2.0-0.1
- Upstream 0.2.0

* Mon Sep 25 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.1.1-0.1
- Upstream update.

* Fri Sep 22 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.1.0-0.1
- Initial packaging.
