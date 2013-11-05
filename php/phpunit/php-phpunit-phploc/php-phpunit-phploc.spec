%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    phploc
%global pear_channel pear.phpunit.de

Name:           php-phpunit-phploc
Version:        2.0.3
Release:        1%{?dist}
Summary:        A tool for quickly measuring the size of a PHP project

Group:          Development/Libraries
License:        BSD
URL:            http://sebastianbergmann.github.com/phploc/
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.4
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.3
Requires:       php-tokenizer
Requires:       php-pear(PEAR) >= 1.9.4
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(pear.symfony.com/Console) >= 2.2.0
Requires:       php-pear(%{pear_channel}/FinderFacade) >= 1.1.0
Requires:       php-pear(%{pear_channel}/Git) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Version) >= 1.0.0
# From phpcompatinfo report for version 2.0.3
Requires:       php-dom
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
phploc is a tool for quickly measuring the size of a PHP project.

The goal of phploc is not not to replace more sophisticated tools such as phpcs,
pdepend, or phpmd, but rather to provide an alternative to them when you just
need to get a quick understanding of a project's size.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf %{buildroot} docdir
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
%{__rm} -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
%{__mkdir} -p %{buildroot}%{pear_xmldir}
%{__install} -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
%{__rm} -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/SebastianBergmann/PHPLOC
%{_bindir}/phploc


%changelog
* Tue Nov 05 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Aug 28 2013 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0
- add requires symfony2/Console, phpunit/Git and phpunit/Version
- drop requires ezc/Console

* Mon Nov 12 2012 Remi Collet <remi@fedoraproject.org> - 1.7.4-1
- Version 1.7.4 (stable) - API 1.7.0 (stable)

* Fri Nov  9 2012 Remi Collet <remi@fedoraproject.org> - 1.7.3-1
- Version 1.7.3 (stable) - API 1.7.0 (stable)

* Thu Oct 18 2012 Remi Collet <remi@fedoraproject.org> - 1.7.2-1
- Version 1.7.2 (stable) - API 1.7.0 (stable)

* Thu Oct 11 2012 Remi Collet <remi@fedoraproject.org> - 1.7.1-1
- Version 1.7.1 (stable) - API 1.7.0 (stable)
- use FinderFacade instead of File_Iterator
- raise dependecies: php >= 5.3.3

* Tue Nov 22 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.4-1
- upstream 1.6.4, rebuild for remi repository

* Sun Nov 20 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.4-1
- upstream 1.6.4

* Thu Nov 03 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.2-1
- upstream 1.6.2, rebuild for remi repository

* Tue Nov  1 2011 Christof Damian <christof@damian.net> - 1.6.2-1
- upstream 1.6.2

* Sat Feb 12 2011 Remi Collet <RPMS@FamilleCollet.com> - 1.6.1-1
- rebuild for remi repository

* Sat Feb 12 2011 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.6.1-1
- upstream 1.6.1

* Fri Feb 12 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.5.1-1
- rebuild for remi repository

* Wed Feb 10 2010 Christof Damian <christof@damian.net> 1.5.1-1
- upstream 1.5.1
- changed requirements
- replaced define macros with global

* Sat Jan 16 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.5.0-2
- rebuild for remi repository

* Thu Jan 14 2010 Christof Damian <christof@damian.net> - 1.5.0-2
- add php 5.2.0 dependency
- remove hack to lower pear requirement

* Sun Jan  3 2010 Christof Damian <christof@damian.net> - 1.5.0-1
- upstream 1.5.0

* Fri Dec 18 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.4.0-2
- /usr/share/pear/PHPLOC wasn't owned

* Fri Dec 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.4.0-1
- rebuild for remi repository

* Sat Dec 12 2009 Christof Damian <christof@damian.net> - 1.4.0-1
- upstream 1.4.0

* Wed Nov 11 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.2.0-2
- rebuild for remi repository

* Sat Nov  7 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-2
- F-(10|11) compatibility

* Tue Oct 13 2009 Guillaume Kulakowski <guillaume DOT kulakowski AT fedoraproject DOT org> - 1.2.0-1
- Initial packaging
