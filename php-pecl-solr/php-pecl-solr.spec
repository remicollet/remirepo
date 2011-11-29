%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}

%global pecl_name solr
%global svnver    320130

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           php-pecl-solr
Version:        1.0.1
Release:        4.svn%{?svnver}%{?dist}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

%if 0%{?svnver}
# svn export -r 320130 https://svn.php.net/repository/pecl/solr/trunk solr
# tar czf solr-svn320130.tgz solr
Source0:        solr-svn320130.tgz
%else
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
%endif
Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  php-devel, php-pear, curl-devel, libxml2-devel

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}
Requires:       php-xml >= 5.2.3
Provides:       php-pecl(%{pecl_name}) = %{version}, php-%{pecl_name} = %{version}

# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{php_extdir}/.*\\.so$
%global __provides_exclude_from %__provides_exclude_from|%{php_ztsextdir}/.*\\.so$


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


%prep
%setup -c -q

%if 0%{?svnver}
mv %{pecl_name}/package.xml .
mv %{pecl_name} %{pecl_name}-%{version}
%endif

%{__php} -n %{SOURCE2} package.xml >CHANGELOG

cd %{pecl_name}-%{version}
extver=$(sed -n '/#define PHP_SOLR_DOTTED_VERSION/{s/.* "//;s/".*$//;p}' php_solr_version.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

chmod -x README.* \
         CREDITS \
         LICENSE \
         TODO \
         docs/documentation.php \
         *.c \
         *.h
cd ..

cat > %{pecl_name}.ini << 'EOF'
; Enable Solr extension module
extension=%{pecl_name}.so
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-%{version}-zts


%build
cd %{pecl_name}-%{version}
%{php_bindir}/phpize
%configure  --with-php-config=%{php_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-%{version}-zts
%{php_ztsbindir}/phpize
%configure  --with-php-config=%{php_ztsbindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}

make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

make -C %{pecl_name}-%{version}-zts \
     install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
rm -rf %{buildroot}


%check
cd %{pecl_name}-%{version}
ln -s %{php_extdir}/curl.so modules/
ln -s %{php_extdir}/json.so modules/

TEST_PHP_ARGS="-n -d extension_dir=$PWD/modules -d extension=curl.so -d extension=json.so -d extension=%{pecl_name}.so" \
   REPORT_EXIT_STATUS=1 \
   NO_INTERACTION=1 \
   TEST_PHP_EXECUTABLE=%{_bindir}/php \
   %{_bindir}/php \
   run-tests.php


%files
%defattr(-, root, root, -)
%doc CHANGELOG
%doc %{pecl_name}-%{version}/CREDITS
%doc %{pecl_name}-%{version}/README.ABOUT_SOLR_EXTENSION
%doc %{pecl_name}-%{version}/README.CONTRIBUTORS
%doc %{pecl_name}-%{version}/README.MEMORY_ALLOCATION
%doc %{pecl_name}-%{version}/README.SUBMITTING_CONTRIBUTIONS
%doc %{pecl_name}-%{version}/TODO
%doc %{pecl_name}-%{version}/LICENSE
%doc %{pecl_name}-%{version}/docs/documentation.php
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
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

* Fri May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-2
- consitent use of pecl_name macro
- add %%check
- fixes some typos
- thanks Remi :)

* Fri May 13 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.10-1
- update to latest release

* Tue Apr 27 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-2
- Add missing Requires
- Remove conditionnal 'php_zend_api' 'pecl_install' no longer required
- %%define no longer must be used
- Thanks to Remi :)

* Mon Apr 26 2010 Johan Cwiklinski <johan AT x-tnd DOT be> 0.9.9-1
- Initial packaging
