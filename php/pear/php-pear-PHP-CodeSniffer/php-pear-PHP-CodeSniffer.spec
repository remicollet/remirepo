# spec file for php-pear-PHP-CodeSniffer
#
# Copyright (c) 2013-2017 Remi Collet
# Copyright (c) 2009-2013 Christof Damian
# Copyright (c) 2006-2009 Konstantin Ryabitsev
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name     PHP_CodeSniffer

Name:           php-pear-PHP-CodeSniffer
Version:        2.8.1
Release:        1%{?dist}
Summary:        PHP coding standards enforcement tool

Group:          Development/Tools
License:        BSD
URL:            http://pear.php.net/package/PHP_CodeSniffer
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

Patch0:         %{pear_name}-role.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear
# to run test suite
BuildRequires:  php-phpunit-PHPUnit >= 3.5.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php-pear(PEAR)
# From phpcompatinfo report for version 2.8.0
Requires:       php-ctype
Requires:       php-date
Requires:       php-dom
Requires:       php-iconv
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-soap
Requires:       php-spl
Requires:       php-tokenizer
Requires:       php-xmlwriter

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-composer(squizlabs/php_codesniffer) = %{version}
Provides:       phpcs = %{version}
Obsoletes:      phpcs < %{version}


%description
PHP_CodeSniffer provides functionality to verify that code conforms to
certain standards, such as PEAR, or user-defined.


%prep
%setup -q -c

# install scripts/phpcs-svn-pre-commit properly
%patch0 -p0 -b .old

cd %{pear_name}-%{version}
mv ../package.xml %{pear_name}.xml


%build
# Empty build section, 


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}

%{__pear} install --nodeps --packagingroot %{buildroot} %{pear_name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{pear_name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/tests

# Version 2.8.0: Tests: 238, Assertions: 92, Skipped: 3.
ret=0
for cmd in php php56 php70 php71; do
   if which $cmd; then
      $cmd %{_bindir}/phpunit AllTests.php || ret=1
   fi
done
exit $ret


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
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/PHP
%{_bindir}/phpcbf
%{_bindir}/phpcs
%{_bindir}/phpcs-svn-pre-commit


%changelog
* Thu Mar 02 2017 Remi Collet <remi@remirepo.net> - 2.8.1-1
- Update to 2.8.1

* Thu Feb 02 2017 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Wed Nov 30 2016 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1

* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Mon Jul 18 2016 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Tue May 31 2016 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Mon Apr 04 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Wed Jan 20 2016 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1 (stable)

* Fri Dec 11 2015 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0 (stable)

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0 (stable)
- run test suite with both PHP 5 and 7 when available

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4 (stable)

* Wed Jun 24 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3 (stable)

* Wed Apr 29 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2 (stable)

* Thu Apr 23 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1 (stable)

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0 (stable)

* Thu Jan 22 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0 (stable)

* Thu Dec 18 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0 (stable)

* Fri Dec 05 2014 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0 (stable)
- add phpcbf and phpcs-svn-pre-commit commands

* Fri Sep 26 2014 Remi Collet <remi@fedoraproject.org> - 1.5.5-1
- Update to 1.5.5 (stable)
- provide php-composer(squizlabs/php_codesniffer)

* Mon Aug 11 2014 Remi Collet <remi@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4 (stable)

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 1.5.3-1
- Update to 1.5.3 (stable)

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2 (stable)

* Thu Dec 12 2013 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1 (stable)

* Thu Nov 28 2013 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0 (stable)

* Tue Nov 26 2013 Remi Collet <remi@fedoraproject.org> - 1.4.8-1
- Update to 1.4.8 (stable)
- add explicity dependencies from phpcompatinfo report

* Thu Sep 26 2013 Remi Collet <remi@fedoraproject.org> - 1.4.7-1
- Update to 1.4.7

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 1.4.6-1
- Update to 1.4.6

* Thu Apr 04 2013 Remi Collet <remi@fedoraproject.org> - 1.4.5-1
- Update to 1.4.5

* Thu Feb 07 2013 Remi Collet <remi@fedoraproject.org> - 1.4.4-1
- Update to 1.4.4

* Tue Dec  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.3-1
- upstream 1.4.3

* Fri Nov  9 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.2-1
- upstream 1.4.2

* Fri Nov  2 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.1-1
- upstream 1.4.1

* Sun Oct  7 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.4.0-1
- upstream 1.4.0

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.3.6-1.2
- rebuilt for new pear_datadir

* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> - 1.3.6-1.1
- rebuilt for new pear_testdir

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.6-1
- upstream 1.3.6

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.5-1
- upstream 1.3.5, backport for remi repo

* Fri Jul 13 2012 Christof Damian <christof@damian.net> - 1.3.5-1
- upstream 1.3.5

* Sun May 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.4-1
- upstream 1.3.4

* Sat May 19 2012 Christof Damian <christof@damian.net> - 1.3.4-1
- upstream 1.3.4

* Fri Mar  2 2012 Christof Damian <christof@damian.net> - 1.3.3-1
- upstream 1.3.3

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.3.3-1
- upstream 1.3.3

* Fri Nov 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.3.1-2
- run test suite in %%check
- remove license as not provided by upstream

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

* Wed Nov 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
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
