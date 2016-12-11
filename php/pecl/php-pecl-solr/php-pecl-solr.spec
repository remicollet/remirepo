# remirepo spec file for php-pecl-solr
# with SCL compatibility, from Fedora:
#
# Fedora spec file for php-pecl-solr
#
# Copyright (c) 2011-2016 Remi Collet
# Copyright (c) 2010 Johan Cwiklinski
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%if 0%{?scl:1}
%if "%{scl}" == "rh-php56"
%global sub_prefix more-php56-
%else
%global sub_prefix %{scl_prefix}
%endif
%endif

%{?scl:          %scl_package         php-pecl-solr}

%global pecl_name solr
%global with_zts  0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
# After curl, json
%global ini_name  %{pecl_name}.ini
%else
# After 20-curl, 40-json
%global ini_name  50-%{pecl_name}.ini
%endif

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           %{?sub_prefix}php-pecl-solr
Version:        1.1.1
Release:        4%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-curl
BuildRequires:  %{?scl_prefix}php-json
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-curl%{?_isa}
Requires:       %{?scl_prefix}php-json%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}          = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-%{pecl_name}%{?_isa}  = %{version}-%{release}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1} && 0%{?rhel}
# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php53u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php54-pecl-%{pecl_name}  <= %{version}
Obsoletes:     php54w-pecl-%{pecl_name} <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php55w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php56w-pecl-%{pecl_name} <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-pecl-%{pecl_name} <= %{version}
Obsoletes:     php70w-pecl-%{pecl_name} <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Feature-rich library that allows PHP developers to communicate easily and
efficiently with Apache Solr server instances using an object-oriented API.

It effectively simplifies the process of interacting with Apache Solr using
PHP5 and it already comes with built-in readiness for the latest features
added in Solr 3.1. The extension has features such as built-in,
serializable query string builder objects which effectively simplifies the
manipulation of name-value pair request parameters across repeated requests.
The response from the Solr server is also automatically parsed into native php
objects whose properties can be accessed as array keys or object properties
without any additional configuration on the client-side. Its advanced HTTP
client reuses the same connection across multiple requests and provides
built-in support for connecting to Solr servers secured behind HTTP
Authentication or HTTP proxy servers. It is also able to connect to
SSL-enabled containers.

More info on PHP-Solr can be found at:
http://www.php.net/manual/en/book.solr.php

Warning: PECL Solr 1 is not compatible with Solr Server >= 4.0.
PECL Solr 2 is available in php-pecl-solr2 package.

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl})}.


%description -l fr
Bibliothèque riche en fonctionnalités qui permet aux développeurs PHP
de communiquer facilement et efficacement avec des instances du serveur
Apache Solr en utilisant une API orientée objet.

Cela simplifie réellement le processus d'interaction avec Apache Solr en
utilisant PHP5 et fournit dores et déjà des facilités pour les dernières
fonctionnalités ajoutées dans Solr 3.1. L'extension possède des
fonctionnalités telles qu'un constructeur de requêtes embarqué et sérialisable
qui simplifie réellement la manipulation des couples de paramètres  nom-valeur
entre différentes requêtes. La réponse de Solr est également analysée
automatiquement en objets php natifs dont les propriétés sont accessibles
en tant que clés de tableaux ou en tant que propriétés d'objets sans la moindre
configuration supplémentaire sur le client. Son client HTTP avancé utilise 
la même connexion entre différentes requêtes et fournit un support embarqué
pour la connexion aux serveurs Solr protégés par authentification HTTP ou
par un serveur mandataire. Il est également possible de se connecter à des 
serveurs via SSL.

Plus d'informations sur PHP-Solr sur:
http://www.php.net/manual/fr/book.solr.php

Attention: PECL Solr 1 n'est pas compatible avec un serveur Solr >= 4.0.
PECL Solr 2 est disponible dans le paquet php-pecl-solr2.

Paquet construit pour PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: en Software Collection (%{scl})}.


%prep
%setup -c -q
mv %{pecl_name}-%{version}%{?prever} NTS

# Don't install/register tests
sed -e 's/role="test"/role="src"/' \
    %{?_licensedir:-e '/LICENSE/s/role="doc"/role="src"/' } \
    -i package.xml

cd NTS

# Check version
extver=$(sed -n '/#define PHP_SOLR_VERSION /{s/.* "//;s/".*$//;p}' php_solr_version.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable Solr extension module
extension=%{pecl_name}.so
EOF

%if %{with_zts}
cp -r NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}


# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in LICENSE $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%check
DEP="-d extension=curl.so -d extension=json.so"
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $DEP \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{__php} \
   %{__php} -n \
   run-tests.php

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $DEP \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

TEST_PHP_ARGS="-n $DEP -d extension=$PWD/modules/%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{__ztsphp} \
   %{__ztsphp} -n \
   run-tests.php
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root, -)
%{?_licensedir:%license NTS/LICENSE}
%doc %{pecl_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Tue Mar  8 2016 Remi Collet <remi@fedoraproject.org> - 1.1.1-4
- adapt for F24

* Tue Jun 23 2015 Remi Collet <rcollet@redhat.com> - 1.1.1-3
- allow build against rh-php56 (as more-php56)
- drop runtime dependency on pear, new scriptlets
- don't install/register tests

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-2.1
- Fedora 21 SCL mass rebuild

* Mon Aug 25 2014 Remi Collet <rcollet@redhat.com> - 1.1.1-2
- improve SCL build

* Fri Jun 20 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (stable)

* Thu Jun 19 2014 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0 (stable)

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-9
- add numerical prefix to extension configuration file (php 5.6)

* Tue Mar 25 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-8
- allow SCL build

* Sun Mar  9 2014 Remi Collet <remi@fedoraproject.org> - 1.0.2-7
- cleanups
- install doc in pecl_docdir
- install tests in pecl_testdir

* Sun Oct 21 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-4
- rebuild

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-2
- php 5.4 build

* Tue Nov 29 2011 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- update to 1.0.2

* Mon Nov 28 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-4.svn320130
- svn snapshot (test suite is now ok)

* Wed Nov 16 2011 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- build against php 5.4
- ignore test result because of https://bugs.php.net/60313

* Thu Oct 06 2011 Remi Collet <Fedora@FamilleCollet.com> - 1.0.1-2
- ZTS extension
- spec cleanups

* Fri Jun 10 2011 Remi Collet <Fedora@famillecollet.com> - 1.0.1-1
- Version 1.0.1 (stable) - API 1.0.1 (stable)
- run test suite after build

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jun 23 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.11-1
- update to latest release

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-2
- consitent use of pecl_name macro
- add %%check
- fixes some typos
- thanks Remi :)

* Thu May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-1
- update to latest release

* Tue Apr 27 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-2
- Add missing Requires
- Remove conditionnal 'php_zend_api' 'pecl_install' no longer required
- %%define no longer must be used
- Thanks to Remi :)

* Mon Apr 26 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-1
- Initial packaging
