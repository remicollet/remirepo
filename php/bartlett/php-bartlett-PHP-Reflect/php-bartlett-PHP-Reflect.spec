%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channel   bartlett.laurent-laville.org
%global pear_name PHP_Reflect

%if 0%{?fedora} >= 12 || 0%{?rhel} >= 6
%global withhtmldoc 1
%else
%global withhtmldoc 0
%endif


Name:           php-bartlett-PHP-Reflect
Version:        1.5.0
Release:        2%{?dist}
Summary:        Adds the ability to reverse-engineer PHP

Group:          Development/Libraries
License:        BSD
URL:            http://bartlett.laurent-laville.org/
Source0:        http://%{channel}/get/%{pear_name}-%{version}%{?prever}.tgz

# Don't install .js (unused)
Patch1:         PHP_Reflect-deljs.patch
# Install generated doc using pear command
Patch2:         PHP_Reflect-addhtml.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.0
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
%if %{withhtmldoc}
# to build HTML documentation
BuildRequires:  asciidoc >= 8.4.0
BuildRequires:  source-highlight
%endif

Requires:       php-pear(PEAR) >= 1.9.0
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channel})
Requires:       php-pcre
Requires:       php-spl
Requires:       php-tokenizer

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants and more, by connecting php callbacks to other tokens.

%if %{withhtmldoc}
HTML Documentation:  %{pear_docdir}/%{pear_name}/docs/index.html
%else
Documentation: http://php5.laurent-laville.org/reflect/manual/current/en/
%endif


%prep
%setup -q -c

# Package is V2
cd %{pear_name}-%{version}%{?prever}
mv -f ../package.xml %{name}.xml

%patch1 -p1 -b .deljs
%if %{withhtmldoc}
%patch2 -p1 -b .addhtml
%endif


%build
cd %{pear_name}-%{version}%{?prever}

%if %{withhtmldoc}
for page in index INSTALL CHANGELOG LICENSE phpreflect-book \
            sources/scanFile sources/scanFunctionArguments \
            sources/Token sources/Autoload sources/Reflect ; do
    asciidoc  -a linkcss -a icons -a theme=flask -a toc2 -n --safe \
              -o $PWD/docs/$page.html  $PWD/docs/$page.txt || :
    [ -f $PWD/docs/$page.html ] || exit 1
done
%endif


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}%{?prever}

%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}



%check
cd %{pear_name}-%{version}%{?prever}

# Version 1.3.0 : OK (34 tests, 55 assertions)
%{_bindir}/phpunit \
  -d date.timezone=UTC \
  --bootstrap %{buildroot}%{pear_phpdir}/Bartlett/PHP/Reflect/Autoload.php \
  tests


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett
%{pear_testdir}/PHP_Reflect


%changelog
* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-2
- generate documentation using asciidoc, without phing

* Mon Nov 26 2012 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Version 1.5.0 (stable) - API 1.5.0 (stable)
- drop documentation build

* Tue Oct 30 2012 Remi Collet <remi@fedoraproject.org> - 1.4.3-1
- Version 1.4.3 (stable) - API 1.4.0 (stable)

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-2
- rebuildt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.4.2-1
- Version 1.4.2 (stable) - API 1.4.0 (stable)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-2
- bump release

* Fri Feb 17 2012 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Version 1.3.0 (stable) - API 1.3.0 (stable)

* Sun Feb 05 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.1.0-1
- Version 1.1.0 (stable) - API 1.1.0 (stable)

* Mon Sep 19 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-2
- remove unused .js and improve installation of generated doc
- use buildroot macro

* Mon Jul 18 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.2-1
- Version 1.0.2 (stable) - API 1.0.0 (stable)

* Sat Jun 16 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.0 (stable)

* Sat Jun 02 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-1
- Version 1.0.0 (stable) - API 1.0.0 (stable)
- add HTML documentation

* Tue Apr 26 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.0-0.1.RC1
- Version 1.0.0RC1 (beta) - API 1.0.0 (beta)

* Sat Apr 17 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.7.0-1
- Version 0.7.0 (beta) - API 0.7.0 (beta)

* Mon Apr 11 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.6.0-1
- Version 0.6.0 (beta) - API 0.6.0 (beta)

* Wed Apr 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.1-1
- Version 0.5.1 (beta) - API 0.5.0 (beta)

* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.5.0 (beta) - API 0.5.0 (beta)

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

