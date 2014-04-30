%global gh_commit    acd690379117b042d1c8af1fafd61bde001bf6bb
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-file-iterator
%global php_home     %{_datadir}/php
%global pear_name    File_Iterator
%global pear_channel pear.phpunit.de
# Circular dependency with phpunit
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-phpunit-File-Iterator
Version:        1.3.4
Release:        3%{?dist}.1
Summary:        FilterIterator implementation that filters files based on a list of suffixes

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3

# From composer.json
Requires:       php(language) >= 5.3.3
# From phpcompatinfo report for 1.3.4
Requires:       php-pcre
Requires:       php-spl

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
FilterIterator implementation that filters files based on a list of suffixes.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

rm File/Iterator/Autoload.php.in


%build
# Empty build section, most likely nothing required.

# If upstream drop Autoload.php, command to generate it
#phpab \
#  --output   File/Iterator/Autoload.php \
#  --template File/Iterator/Autoload.php.in \
#  File


%install
rm -rf      %{buildroot}
mkdir -p    %{buildroot}%{php_home}
cp -pr File %{buildroot}%{php_home}


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc ChangeLog.markdown README.markdown LICENSE composer.json
%{php_home}/*


%changelog
* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-3
- cleanup pear registry

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 1.3.4-2
- get sources from github

* Fri Oct 11 2013 Remi Collet <remi@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4
- raise dependencies: php 5.3.3, pear 1.9.4

* Sat Oct  6 2012 Remi Collet <remi@fedoraproject.org> - 1.3.3-1
- upstream 1.3.3

* Sun Sep 23 2012 Remi Collet <remi@fedoraproject.org> - 1.3.2-1
- upstream 1.3.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Version 1.3.1 (stable) - API 1.3.0 (stable)
- unmacro current command
- remove pear version hack

* Mon Jan 16 2012 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- upstream 1.3.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov  2 2011 Christof Damian <christof@damian.net> - 1.3.0-1
- upstream 1.3.0

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- upstream 1.3.0

* Fri Mar  4 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.6-1
- upstream 1.2.6
- rebuild for remi repository

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 1.2.6-1
- upstream 1.2.6

* Mon Feb 28 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.2.4-1
- upstream 1.2.4
- rebuild for remi repository

* Mon Feb 28 2011 Christof Damian <cdamian@robin.gotham.krass.com> - 1.2.4-1
- upstream 1.2.4

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 18 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.3-1
- upstream 1.2.3
- rebuild for remi repository

* Fri Sep 17 2010 Christof Damian <christof@damian.net> - 1.2.3-1
- upstream 1.2.3

* Thu Jul 22 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.2-2
- rebuild for remi repository

* Thu Jul 22 2010 Christof Damian <christof@damian.net> - 1.2.2-2
- fix minimum pear requirement

* Thu Jul 22 2010 Christof Damian <christof@damian.net> - 1.2.2-1
- upstream 1.2.2, bugfix

* Sun May  9 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.1-1
- rebuild for remi repository

* Sat May  8 2010 Christof Damian <christof@damian.net> - 1.2.1-1
- upstream 1.2.1

* Wed Feb 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.2.0-1
- rebuild for remi repository

* Tue Feb  9 2010 Christof Damian <christof@damian.net> - 1.2.0-1
- upstream 1.2.0
- increased php-common requirements to 5.2.7
- increased php-pear requirement
- use global instead of define
- use channel macro in postun

* Fri Dec 18 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.1.1-2
- rebuild for remi repository

* Thu Dec 17 2009 Christof Damian <christof@damian.net> 1.1.1-2
- version 1.1.1 lowered the php requirement

* Thu Dec 17 2009 Christof Damian <christof@damian.net> 1.1.1-1
- upstream 1.1.1

* Thu Dec 17 2009 Remi Collet <RPMS@FamilleCollet.com> - 1.1.0-4
- rebuild for remi repository

* Mon Nov 30 2009 Christof Damian <christof@damian.net> 1.1.0-4
- own pear directories

* Sat Nov 28 2009 Christof Damian <christof@damian.net> 1.1.0-3
- fixed php-pear buildrequire
- just require php-common

* Thu Nov 26 2009 Christof Damian <christof@damian.net> 1.1.0-2
- fix package.xml to work with older pear versions

* Wed Nov 25 2009 Christof Damian <christof@damian.net> 1.1.0-1
- Initial packaging
