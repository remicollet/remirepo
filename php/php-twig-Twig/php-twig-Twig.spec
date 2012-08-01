%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.twig-project.org
%global pear_name    %(echo %{name} | sed -e 's/^php-twig-//' -e 's/-/_/g')

Name:             php-twig-Twig
Version:          1.9.1
Release:          1%{?dist}
Summary:          Twig is a modern template engine for PHP

Group:            Development/Libraries
License:          BSD
URL:              http://twig.sensiolabs.org
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.2.4
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-date
Requires:         php-dom
Requires:         php-hash
Requires:         php-iconv
Requires:         php-json
Requires:         php-mbstring
Requires:         php-pcre
Requires:         php-reflection
Requires:         php-spl

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The flexible, fast, and secure template engine for PHP.

* Fast: Twig compiles templates down to plain optimized PHP code. The
  overhead compared to regular PHP code was reduced to the very minimum.

* Secure: Twig has a sandbox mode to evaluate untrusted template code. This
  allows Twig to be used as a template language for applications where users
  may modify the template design.

* Flexible: Twig is powered by a flexible lexer and parser. This allows the
  developer to define its own custom tags and filters, and create its own
  DSL.


%prep
%setup -q -c
# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


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
%{pear_phpdir}/%{pear_name}


%changelog
* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> 1.9.1-1
- Update to 1.9.1, backport for remi repository

* Tue Jul 31 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.9.1-1
- Updated to upstream version 1.9.1

* Tue Jul 17 2012 Remi Collet <RPMS@FamilleCollet.com> 1.9.0-1
- Update to 1.9.0, backport for remi repository

* Sun Jul 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.9.0-1
- Updated to upstream version 1.9.0
- Added php-hash require
- Minor syntax updates

* Sun Jun 09 2012 Remi Collet <RPMS@FamilleCollet.com> 1.8.2-1
- rebuild for remi repository

* Thu May 31 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.8.2-1
- Updated to upstream version 1.8.2
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed %%clean section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.8.1-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-ctype, php-date, php-dom, php-iconv, php-json, php-mbstring,
  php-pcre, php-reflection, php-spl
- Removed %%defattr from %%files section

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.8.1-1
- Updated to upstream version 1.8.1
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Fri Apr 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.7.0-1
- Initial package
