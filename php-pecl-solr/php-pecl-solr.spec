%{!?__pecl:     %{expand: %%global __pecl     %{_bindir}/pecl}}
%{!?php_extdir: %{expand: %%global php_extdir %(php-config --extension-dir)}}

%global pecl_name solr

Summary:        Object oriented API to Apache Solr
Summary(fr):    API orientée objet pour Apache Solr
Name:           php-pecl-solr
Version:        1.0.1
Release:        1%{?dist}
License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/solr

Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source2:        xml2changelog

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Provides:       php-pecl(%{pecl_name}) = %{version}, php-%{pecl_name} = %{version}
BuildRequires:  php-devel, php-pear, curl-devel, libxml2-devel
Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:     php(zend-abi) = %{php_zend_api}
Requires:     php(api) = %{php_core_api}
Requires:     php-xml >= 5.2.3

%{?filter_setup:
%filter_provides_in %{php_extdir}/.*\.so$
%filter_setup
}


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
%{_bindir}/php -n %{SOURCE2} package.xml >CHANGELOG

cd %{pecl_name}-%{version}
chmod -x README.* \
         CREDITS \
         LICENSE \
         TODO \
         docs/documentation.php \
         *.c \
         *.h


%build
cd %{pecl_name}-%{version}
phpize
%configure
%{__make} %{?_smp_mflags}


%install
cd %{pecl_name}-%{version}
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
mkdir -p %{buildroot}%{_sysconfdir}/php.d
cat > %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini << 'EOF'
; Enable Solr extension module
extension=%{pecl_name}.so
EOF

# Install XML package description
mkdir -p %{buildroot}%{pecl_xmldir}
install -p -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%clean
%{__rm} -rf %{buildroot}


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
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
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
