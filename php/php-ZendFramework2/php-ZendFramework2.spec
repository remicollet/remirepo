#
# Fedora spec file for php-ZendFramework2
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Remi Collet <remi@fedoraproject.org>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     zendframework
%global github_name      zendframework
%global github_version   2.4.10
%global github_commit    7e5bdc38820aef518c1c49d4b6e8fcb0083b165b

%global composer_vendor  zendframework

%global with_tests 0%{!?_without_tests:1}

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:      php-ZendFramework2
Version:   %{github_version}
Release:   1%{?dist}
Summary:   Zend Framework 2

Group:     Development/Libraries
License:   BSD
URL:       http://framework.zend.com

# GitHub export does not include tests.
# Run php-ZendFramework2-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
%if %{with_tests}
# PHPUnit + autoloader
BuildRequires: %{_bindir}/phpunit
# required by components
BuildRequires: php(language) >= 5.3.23
BuildRequires: php-bcmath
BuildRequires: php-bz2
BuildRequires: php-ctype
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-dba
BuildRequires: php-dom
BuildRequires: php-fileinfo
BuildRequires: php-filter
BuildRequires: php-gd
BuildRequires: php-gmp
BuildRequires: php-hash
BuildRequires: php-iconv
BuildRequires: php-intl
BuildRequires: php-json
BuildRequires: php-ldap
BuildRequires: php-libxml
BuildRequires: php-mbstring
BuildRequires: php-mcrypt
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-simplexml
BuildRequires: php-soap
BuildRequires: php-spl
BuildRequires: php-tidy
BuildRequires: php-tokenizer
BuildRequires: php-xml
BuildRequires: php-xmlreader
BuildRequires: php-xmlwriter
BuildRequires: php-zip
BuildRequires: php-zlib
BuildRequires: php-composer(ircmaxell/random-lib)
BuildRequires: php-composer(mikey179/vfsStream) >= 1.2
BuildRequires: php-composer(%{composer_vendor}/zendxml)
%endif

Requires: php-composer(%{composer_vendor}/zend-authentication)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-barcode)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-captcha)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-code)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-config)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-console)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-crypt)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-debug)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-di)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-dom)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-feed)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-file)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-form)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-inputfilter)      = %{version}
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-ldap)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-loader)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-log)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-mail)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-memory)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-mime)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-modulemanager)    = %{version}
Requires: php-composer(%{composer_vendor}/zend-mvc)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-navigation)       = %{version}
Requires: php-composer(%{composer_vendor}/zend-paginator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-permissions-acl)  = %{version}
Requires: php-composer(%{composer_vendor}/zend-permissions-rbac) = %{version}
Requires: php-composer(%{composer_vendor}/zend-progressbar)      = %{version}
Requires: php-composer(%{composer_vendor}/zend-serializer)       = %{version}
Requires: php-composer(%{composer_vendor}/zend-server)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-soap)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-tag)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-test)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-text)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-version)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-xmlrpc)           = %{version}
Requires: php-composer(%{composer_vendor}/zendxml)

Provides: php-composer(%{composer_vendor}/zendframework) = %{version}


%description
Zend Framework 2 is an open source framework for developing web applications
and services using PHP 5.3+. Zend Framework 2 uses 100% object-oriented code
and utilizes most of the new features of PHP 5.3, namely namespaces, late
static binding, lambda functions and closures.

Zend Framework 2 evolved from Zend Framework 1, a successful PHP framework
with over 15 million downloads.

Note: This meta package installs all base Zend Framework component packages
(Authentication, Barcode, Cache, Captcha, Code, Config, Console, Crypt, Db,
Debug, Di, Dom, Escaper, EventManager, Feed, File, Filter, Form, Http, I18n,
InputFilter, Json, Ldap, Loader, Log, Mail, Math, Memory, Mime, ModuleManager,
Mvc, Navigation, Paginator, Permissions-Acl, Permissions-Rbac, ProgressBar,
Serializer, Server, ServiceManager, Session, Soap, Stdlib, Tag, Test, Text,
Uri, Validator, Version, View, XmlRpc) except the optional Cache-apc and
Cache-memcached packages.

# ##############################################################################

%package   common

Summary:   Zend Framework 2: Common files
Group:     Development/Libraries

Requires:  php(language) >= 5.3.23

# v1 and v2 cannot be installed at the same time
Conflicts: php-ZendFramework < 2

%description common
%{summary}

# ------------------------------------------------------------------------------

%package  Authentication

Summary:  Zend Framework 2: Authentication Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.authentication.intro.html

Requires: %{name}-common    = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-crypt)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-ldap)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-date
Requires: php-hash
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-authentication) = %{version}

%description Authentication
The Zend\Authentication component provides an API for authentication and
includes concrete authentication adapters for common use case scenarios.

Zend\Authentication is concerned only with authentication and not with
authorization. Authentication is loosely defined as determining whether
an entity actually is what it purports to be (i.e., identification),
based on some set of credentials. Authorization, the process of deciding
whether to allow an entity access to, or to perform operations upon, other
entities is outside the scope of Zend\Authentication. For more information
about authorization and access control with Zend Framework, please see the
Zend\Permissions\Acl or Zend\Permissions\Rbac component.

# ------------------------------------------------------------------------------

%package  Barcode

Summary:  Zend Framework 2: Barcode Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.barcode.intro.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
#     zendframework/zendpdf
# phpcompatinfo (computed from version 2.3.1)
Requires: php-dom
Requires: php-gd
Requires: php-iconv
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-barcode) = %{version}

%description Barcode
Zend\Barcode\Barcode provides a generic way to generate barcodes. The
Zend\Barcode component is divided into two subcomponents: barcode objects
and renderers. Objects allow you to create barcodes independently of the
renderer. Renderer allow you to draw barcodes based on the support required.

# ------------------------------------------------------------------------------

%package  Cache

Summary:  Zend Framework 2: Cache Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-cache

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-serializer)       = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

# Removed sub-packages
Obsoletes: %{name}-Cache-apc       < %{version}-%{release}
Provides:  %{name}-Cache-apc       = %{version}-%{release}
Obsoletes: %{name}-Cache-memcached < %{version}-%{release}
Provides:  %{name}-Cache-memcached = %{version}-%{release}

Provides: php-composer(%{composer_vendor}/zend-cache) = %{version}

%description Cache
%{summary}

Optional:
* APC (php-pecl-apc)
* DBA (php-dba)
* Memcache (php-pecl-memcache)
* Memcached (php-pecl-memcached)
* Mongo (php-pecl-mongo)
* Redis (php-pecl-redis)
* XCache (php-xcache)

# ------------------------------------------------------------------------------

%package  Captcha

Summary:  Zend Framework 2: CAPTCHA Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.captcha.intro.html

Requires: %{name}-common    = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-text)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
#     zendframework/zend-resources
#     zendframework/zendservice-recaptcha
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-gd
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-captcha) = %{version}

%description Captcha
CAPTCHA stands for “Completely Automated Public Turing test to tell Computers
and Humans Apart”; it is used as a challenge-response to ensure that the
individual submitting information is a human and not an automated process.
Typically, a CAPTCHA is used with form submissions where authenticated users
are not necessary, but you want to prevent spam submissions.

CAPTCHAs can take a variety of forms, including asking logic questions,
presenting skewed fonts, and presenting multiple images and asking how they
relate. The Zend\Captcha component aims to provide a variety of back ends
that may be utilized either standalone or in conjunction with the Zend\Form
component.

# ------------------------------------------------------------------------------

%package  Code

Summary:  Zend Framework 2: Code Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html

Requires: %{name}-common       = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-doctrine-common  >= 2.1
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-reflection
Requires: php-spl
Requires: php-tokenizer

Provides: php-composer(%{composer_vendor}/zend-code) = %{version}

%description Code
Provides facilities to generate arbitrary code using an object oriented
interface.

# ------------------------------------------------------------------------------

%package  Config

Summary:  Zend Framework 2: Config Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.config.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-libxml
Requires: php-pcre
Requires: php-spl
Requires: php-xmlreader
Requires: php-xmlwriter

Provides: php-composer(%{composer_vendor}/zend-config) = %{version}

%description Config
Zend\Config is designed to simplify access to configuration data within
applications. It provides a nested object property-based user interface
for accessing this configuration data within application code. The
configuration data may come from a variety of media supporting hierarchical
data storage. Currently, Zend\Config provides adapters that read and write
configuration data stored in .ini, JSON, YAML and XML files.

# ------------------------------------------------------------------------------

%package  Console

Summary:  Zend Framework 2: Console Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.console.introduction.html

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-reflection
Requires: php-spl
Requires: php-xml

Provides: php-composer(%{composer_vendor}/zend-console) = %{version}

%description Console
Zend Framework 2 features built-in console support.

When a Zend\Application is run from a console window (a shell window), it will
recognize this fact and prepare Zend\Mvc components to handle the request.
Console support is enabled by default, but to function properly it requires at
least one console route and one action controller to handle the request.

* Console routing allows you to invoke controllers and action depending on
  command line parameters provided by the user.
* Module Manager integration allows ZF2 applications and modules to display
  help and usage information, in case the command line has not been understood
  (no route matched).
* Console-aware action controllers will receive a console request containing
  all named parameters and flags. They are able to send output back to the
  console window.
* Console adapters provide a level of abstraction for interacting with console
  on different operating systems.
* Console prompts can be used to interact with the user by asking him questions
  and retrieving input.

# ------------------------------------------------------------------------------

%package  Crypt

Summary:  Zend Framework 2: Crypt Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.crypt.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-mcrypt
# phpcompatinfo (computed from version 2.3.1)
#     scrypt -- not packaged
Requires: php-hash
Requires: php-openssl
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-crypt) = %{version}

%description Crypt
Zend\Crypt provides support of some cryptographic tools. The available
features are:

* encrypt-then-authenticate using symmetric ciphers (the authentication step is
  provided using HMAC)
* encrypt/decrypt using symmetric and public key algorithm (e.g. RSA algorithm)
* generate digital sign using public key algorithm (e.g. RSA algorithm)
* key exchange using the Diffie-Hellman method
* Key derivation function (e.g. using PBKDF2 algorithm)
* Secure password hash (e.g. using Bcrypt algorithm)
* generate Hash values
* generate HMAC values

The main scope of this component is to offer an easy and secure way to protect
and authenticate sensitive data in PHP. Because the use of cryptography is not
so easy we recommend to use the Zend\Crypt component only if you have a minimum
background on this topic.

# ------------------------------------------------------------------------------

%package  Db

Summary:  Zend Framework 2: DB Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-db

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-pcre
Requires: php-pdo
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-db) = %{version}

%description Db
%{summary}

Optional:
* ibm_db2 (http://pecl.php.net/package/ibm_db2)
* mysqli (php-mysql)
* oci8 (http://pecl.php.net/package/oci8)
* pgsql (php-pgsql)
* sqlsrv (http://pecl.php.net/package/sqlsrv)

# ------------------------------------------------------------------------------

%package  Debug

Summary:  Zend Framework 2: Debug Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html

Requires: %{name}-common  = %{version}-%{release}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre

Provides: php-composer(%{composer_vendor}/zend-debug) = %{version}

%description Debug
%{summary}

Optional: XDebug (php-pecl-xdebug)

# ------------------------------------------------------------------------------

%package  Di

Summary:  Zend Framework 2: DI Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.di.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-code)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-di) = %{version}

%description Di
Dependency Injection (here-in called DI) is a concept that has been talked
about in numerous places over the web. Simply put, we’ll explain the act of
injecting dependencies simply with this below code:

$b = new MovieLister(new MovieFinder());

Above, MovieFinder is a dependency of MovieLister, and MovieFinder was
injected into MovieLister.

# ------------------------------------------------------------------------------

%package  Dom

Summary:  Zend Framework 2: DOM Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.dom.intro.html

Requires: %{name}-common = %{version}-%{release}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-dom
Requires: php-libxml
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-dom) = %{version}

%description Dom
The Zend\Dom component provides tools for working with DOM documents and
structures. Currently, we offer Zend\Dom\Query, which provides a unified
interface for querying DOM documents utilizing both XPath and CSS selectors.

# ------------------------------------------------------------------------------

%package  Escaper

Summary:  Zend Framework 2: Escaper Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.escaper.introduction.html

Requires: %{name}-common = %{version}-%{release}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-iconv
Requires: php-mbstring
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-escaper) = %{version}

%description Escaper
The OWASP Top 10 web security risks study lists Cross-Site Scripting (XSS)
in second place. PHP’s sole functionality against XSS is limited to two
functions of which one is commonly misapplied. Thus, the Zend\Escaper component
was written. It offers developers a way to escape output and defend from XSS
and related vulnerabilities by introducing contextual escaping based on
peer-reviewed rules.

# ------------------------------------------------------------------------------

%package  EventManager

Summary:  Zend Framework 2: EventManager Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.event-manager.event-manager.html

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-eventmanager) = %{version}

%description EventManager
The EventManager is a component designed for the following use cases:

* Implementing simple subject/observer patterns.
* Implementing Aspect-Oriented designs.
* Implementing event-driven architectures.

The basic architecture allows you to attach and detach listeners to named
events, both on a per-instance basis as well as via shared collections;
trigger events; and interrupt execution of listeners.

# ------------------------------------------------------------------------------

%package  Feed

Summary:  Zend Framework 2: Feed Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.feed.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-date
Requires: php-dom
Requires: php-hash
Requires: php-libxml
Requires: php-pcre
Requires: php-spl
Requires: php-tidy

Provides: php-composer(%{composer_vendor}/zend-feed) = %{version}

%description Feed
Zend\Feed provides functionality for consuming RSS and Atom feeds. It provides
a natural syntax for accessing elements of feeds, feed attributes, and entry
attributes. Zend\Feed also has extensive support for modifying feed and entry
structure with the same natural syntax, and turning the result back into XML.
In the future, this modification support could provide support for the Atom
Publishing Protocol.

Zend\Feed consists of Zend\Feed\Reader for reading RSS and Atom feeds,
Zend\Feed\Writer for writing RSS and Atom feeds, and Zend\Feed\PubSubHubbub
for working with Hub servers. Furthermore, both Zend\Feed\Reader and
Zend\Feed\Writer support extensions which allows for working with additional
data in feeds, not covered in the core API but used in conjunction with RSS
and Atom feeds.

# ------------------------------------------------------------------------------

%package  File

Summary:  Zend Framework 2: File Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-file

Requires: %{name}-common    = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-fileinfo
Requires: php-hash
Requires: php-pcre
Requires: php-spl
Requires: php-tokenizer

Provides: php-composer(%{composer_vendor}/zend-file) = %{version}

%description File
%{summary}

# ------------------------------------------------------------------------------

%package  Filter

Summary:  Zend Framework 2: Filter Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.filter.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-crypt)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
# phpcompatinfo (computed from version 2.3.1)
#     rar -- not packaged
Requires: php-bz2
Requires: php-date
Requires: php-iconv
Requires: php-mbstring
Requires: php-openssl
Requires: php-pcre
Requires: php-pecl(LZF)
Requires: php-spl
Requires: php-zip
Requires: php-zlib

Provides: php-composer(%{composer_vendor}/zend-filter) = %{version}

%description Filter
The Zend\Filter component provides a set of commonly needed data filters.
It also provides a simple filter chaining mechanism by which multiple filters
may be applied to a single datum in a user-defined order.

# ------------------------------------------------------------------------------

%package  Form

Summary:  Zend Framework 2: Form Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.form.intro.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-inputfilter)      = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
#     zendframework/zendservice-recaptcha
Requires: php-composer(%{composer_vendor}/zend-captcha)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-code)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-intl
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-form) = %{version}

%description Form
Zend\Form is intended primarily as a bridge between your domain models and the
View Layer. It composes a thin layer of objects representing form elements, an
InputFilter, and a small number of methods for binding data to and from the
form and attached objects.

The Zend\Form component consists of the following objects:

* Elements, which simply consist of a name and attributes.
* Fieldsets, which extend from Elements, but allow composing other fieldsets
  and elements.
* Forms, which extend from Fieldsets (and thus Elements). They provide data
  and object binding, and compose InputFilters. Data binding is done via
  ZendStdlibHydrator.

# ------------------------------------------------------------------------------

%package  Http

Summary:  Zend Framework 2: HTTP Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.http.html

Requires: %{name}-common    = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-loader)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-curl
Requires: php-date
Requires: php-fileinfo
Requires: php-openssl
Requires: php-pcre
Requires: php-spl
Requires: php-zlib

Provides: php-composer(%{composer_vendor}/zend-http) = %{version}

%description Http
Zend\Http is a primary foundational component of Zend Framework. Since much
of what PHP does is web-based, specifically HTTP, it makes sense to have a
performant, extensible, concise and consistent API to do all things HTTP.
In nutshell, there are several parts of Zend\Http:

* Context-less Request and Response classes that expose a fluent API for
  introspecting several aspects of HTTP messages:
  ** Request line information and response status information
  ** Parameters, such as those found in POST and GET
  ** Message Body
  ** Headers
* A Client implementation with various adapters that allow for sending requests
  and introspecting responses.

# ------------------------------------------------------------------------------

%package  I18n

Summary:  Zend Framework 2: i18n Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.i18n.translating.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
#     zendframework/zend-resources
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-config)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
Requires: php-intl
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-date
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-i18n) = %{version}

%description I18n
ZendI18n comes with a complete translation suite which supports all major
formats and includes popular features like plural translations and text
domains. The Translator component is mostly dependency free, except for
the fallback to a default locale, where it relies on the Intl PHP extension.

The translator itself is initialized without any parameters, as any
configuration to it is optional. A translator without any translations
will actually do nothing but just return the given message IDs.

# ------------------------------------------------------------------------------

%package  InputFilter

Summary:  Zend Framework 2: InputFilter Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.input-filter.intro.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-inputfilter) = %{version}

%description InputFilter
The Zend\InputFilter component can be used to filter and validate generic sets
of input data. For instance, you could use it to filter $_GET or $_POST values,
CLI arguments, etc.

# ------------------------------------------------------------------------------

%package  Json

Summary:  Zend Framework 2: JSON Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.json.introduction.html

Requires: %{name}-common  = %{version}-%{release}
Requires: php-composer(%{composer_vendor}/zendxml)
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-server)           = %{version}
Requires: php-composer(%{composer_vendor}/zendxml)
# phpcompatinfo (computed from version 2.3.1)
Requires: php-json
Requires: php-mbstring
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-json) = %{version}

%description Json
Zend\Json provides convenience methods for serializing native PHP to JSON
and decoding JSON to native PHP.

JSON, JavaScript Object Notation, can be used for data interchange between
JavaScript and other languages. Since JSON can be directly evaluated by
JavaScript, it is a more efficient and lightweight format than XML for
exchanging data with JavaScript clients.

In addition, Zend\Json provides a useful way to convert any arbitrary XML
formatted string into a JSON formatted string. This built-in feature will
enable PHP developers to transform the enterprise data encoded in XML format
into JSON format before sending it to browser-based Ajax client applications.
It provides an easy way to do dynamic data conversion on the server-side code
thereby avoiding unnecessary XML parsing in the browser-side applications. It
offers a nice utility function that results in easier application-specific
data processing techniques.

# ------------------------------------------------------------------------------

%package  Ldap

Summary:  Zend Framework 2: LDAP Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.ldap.introduction.html

Requires: %{name}-common       = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-iconv
Requires: php-json
Requires: php-ldap
Requires: php-mbstring
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-ldap) = %{version}

%description Ldap
Zend\Ldap\Ldap is a class for performing LDAP operations including but not
limited to binding, searching and modifying entries in an LDAP directory.

# ------------------------------------------------------------------------------

%package  Loader

Summary:  Zend Framework 2: Loader Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-loader

Requires: %{name}-common = %{version}-%{release}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-bz2
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-loader) = %{version}

%description Loader
%{summary}

# ------------------------------------------------------------------------------

%package  Log

Summary:  Zend Framework 2: Log Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.log.overview.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-console)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-mail)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-dom
Requires: php-json
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-log) = %{version}

%description Log
Zend\Log\Logger is a component for general purpose logging. It supports multiple
log backends, formatting messages sent to the log, and filtering messages from
being logged. These functions are divided into the following objects:

* A Logger (instance of Zend\Log\Logger) is the object that your application
  uses the most. You can have as many Logger objects as you like; they do not
  interact. A Logger object must contain at least one Writer, and can optionally
  contain one or more Filters.
* A Writer (inherits from Zend\Log\Writer\AbstractWriter) is responsible for
  saving data to storage.
* A Filter (implements Zend\Log\Filter\FilterInterface) blocks log data from
  being saved. A filter is applied to an individual writer. Filters can be
  chained.
* A Formatter (implements Zend\Log\Formatter\FormatterInterface) can format the
  log data before it is written by a Writer. Each Writer has exactly one
  Formatter.

Optional: MongoDB (php-pecl-mongo)

# ------------------------------------------------------------------------------

%package  Mail

Summary:  Zend Framework 2: Mail Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.mail.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-crypt)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-loader)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-mime)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-date
Requires: php-iconv
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-mail) = %{version}

%description Mail
Zend\Mail provides generalized functionality to compose and send both text
and MIME-compliant multipart email messages. Mail can be sent with Zend\Mail
via the Mail\Transport\Sendmail, Mail\Transport\Smtp or the Mail\Transport\File
transport. Of course, you can also implement your own transport by implementing
the Mail\Transport\TransportInterface.

# ------------------------------------------------------------------------------

%package  Math

Summary:  Zend Framework 2: Math Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.math.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json (optional)
#     ircmaxell/random-lib
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(ircmaxell/random-lib)
Requires: php-bcmath
# php-gmp causes issues (see BZ #1152440)
#Requires: php-gmp
# phpcompatinfo (computed from version 2.3.1)
Requires: php-mcrypt
Requires: php-openssl
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-math) = %{version}

%description Math
Zend\Math namespace provides general mathematical functions. So far the
supported functionalities are:

* Zend\Math\Rand: A random number generator
* Zend\Math\BigInteger: A library to manage big integers

Optional: php-gmp

# ------------------------------------------------------------------------------

%package  Memory

Summary:  Zend Framework 2: Memory Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html

Requires: %{name}-common = %{version}-%{release}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-memory) = %{version}

%description Memory
%{summary}

# ------------------------------------------------------------------------------

%package  Mime

Summary:  Zend Framework 2: MIME Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.mime.html

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-mail)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-iconv
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-mime) = %{version}

%description Mime
Zend\Mime\Mime is a support class for handling multipart MIME messages. It
is used by Zend\Mail and Zend\Mime\Message and may be used by applications
requiring MIME support.

Optional: %{name}-Mail

# ------------------------------------------------------------------------------

%package  ModuleManager

Summary:  Zend Framework 2: ModuleManager Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.module-manager.intro.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-config)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-console)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-loader)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-modulemanager) = %{version}

%description ModuleManager
Zend Framework 2.0 introduces a new and powerful approach to modules. This new
module system is designed with flexibility, simplicity, and re-usability in
mind. A module may contain just about anything: PHP code, including MVC
functionality; library code; view scripts; and/or public assets such as images,
CSS, and JavaScript.

# ------------------------------------------------------------------------------

%package  Mvc

Summary:  Zend Framework 2: MVC Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.mvc.intro.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-form)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-authentication)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-config)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-console)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-di)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-inputfilter)      = %{version}
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-log)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-modulemanager)    = %{version}
Requires: php-composer(%{composer_vendor}/zend-serializer)       = %{version}
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-text)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-version)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-intl
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-mvc) = %{version}

%description Mvc
Zend\Mvc is a brand new MVC implementation designed from the ground up for
Zend Framework 2, focusing on performance and flexibility.

The MVC layer is built on top of the following components:

* Zend\ServiceManager - Zend Framework provides a set of default service
  definitions set up at Zend\Mvc\Service. The ServiceManager creates and
  configures your application instance and workflow.
* Zend\EventManager - The MVC is event driven. This component is used everywhere
  from initial bootstrapping of the application, through returning response and
  request calls, to setting and retrieving routes and matched routes, as well as
  render views.
* Zend\Http - specifically the request and response objects.
* Zend\Stdlib\DispatchableInterface. All “controllers” are simply dispatchable
  objects.

# ------------------------------------------------------------------------------

%package  Navigation

Summary:  Zend Framework 2: Navigation Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.navigation.intro.html

Requires: %{name}-common          = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-config)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-mvc)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-permissions-acl)  = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-navigation) = %{version}

%description Navigation
Zend\Navigation is a component for managing trees of pointers to web pages.
Simply put: It can be used for creating menus, breadcrumbs, links, and sitemaps,
or serve as a model for other navigation related purposes.

# ------------------------------------------------------------------------------

%package  Paginator

Summary:  Zend Framework 2: Paginator Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.paginator.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-paginator) = %{version}

%description Paginator
Zend\Paginator is a flexible component for paginating collections of data and
presenting that data to users.

The primary design goals of Zend\Paginator are as follows:

* Paginate arbitrary data, not just relational databases
* Fetch only the results that need to be displayed
* Do not force users to adhere to only one way of displaying data or rendering
  pagination controls
* Loosely couple Zend\Paginator to other Zend Framework components so that users
  who wish to use it independently of Zend\View, Zend\Db, etc. can do so

# ------------------------------------------------------------------------------

%package  Permissions-Acl

Summary:  Zend Framework 2: Permissions ACL Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.permissions.acl.intro.html

Requires: %{name}-common = %{version}-%{release}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-permissions-acl) = %{version}

%description Permissions-Acl
The Zend\Permissions\Acl component provides a lightweight and flexible access
control list (ACL) implementation for privileges management. In general, an
application may utilize such ACL‘s to control access to certain protected
objects by other requesting objects.

For the purposes of this documentation:

* a resource is an object to which access is controlled.
* a role is an object that may request access to a Resource.

Put simply, roles request access to resources. For example, if a parking
attendant requests access to a car, then the parking attendant is the requesting
role, and the car is the resource, since access to the car may not be granted
to everyone.

Through the specification and use of an ACL, an application may control how
roles are granted access to resources.

# ------------------------------------------------------------------------------

%package  Permissions-Rbac

Summary:  Zend Framework 2: Permissions RBAC Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.permissions.rbac.intro.html

Requires: %{name}-common = %{version}-%{release}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-permissions-rbac) = %{version}

%description Permissions-Rbac
The Zend\Permissions\Rbac component provides a lightweight role-based access
control implementation based around PHP 5.3’s SPL RecursiveIterator and
RecursiveIteratorIterator. RBAC differs from access control lists (ACL) by
putting the emphasis on roles and their permissions rather than objects
(resources).

# ------------------------------------------------------------------------------

%package  ProgressBar

Summary:  Zend Framework 2: ProgressBar Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.progress-bar.html

Requires: %{name}-common  = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
# phpcompatinfo (computed from version 2.3.1)
#     uploadprogress
Requires: php-date
Requires: php-pcre
Requires: php-pecl(APC)
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-progressbar) = %{version}

%description ProgressBar
Zend\ProgressBar is a component to create and update progress bars in different
environments. It consists of a single backend, which outputs the progress
through one of the multiple adapters. On every update, it takes an absolute
value and optionally a status message, and then calls the adapter with some
precalculated values like percentage and estimated time left.

# ------------------------------------------------------------------------------

%package  Serializer

Summary:  Zend Framework 2: Serializer Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.serializer.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
#     wddx
Requires: php-dom
Requires: php-libxml
Requires: php-pcre
Requires: php-pecl(igbinary)
Requires: php-simplexml
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-serializer) = %{version}

%description Serializer
The Zend\Serializer component provides an adapter based interface to simply
generate storable representation of PHP types by different facilities, and
recover.

Optional: msgpack (php-pecl-msgpack)

# ------------------------------------------------------------------------------

%package  Server

Summary:  Zend Framework 2: Server Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.server.html

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-code)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-server) = %{version}

%description Server
The Zend\Server family of classes provides functionality for the various server
classes, including Zend\XmlRpc\Server and Zend\Json\Server. Zend\Server\Server
provides an interface that mimics PHP 5’s SoapServer class; all server classes
should implement this interface in order to provide a standard server API.

The Zend\Server\Reflection tree provides a standard mechanism for performing
function and class introspection for use as callbacks with the server classes,
and provides data suitable for use with Zend\Server\Server‘s getFunctions()
and loadFunctions() methods.

# ------------------------------------------------------------------------------

%package  ServiceManager

Summary:  Zend Framework 2: ServiceManager Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.service-manager.intro.html

Requires: %{name}-common = %{version}-%{release}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-di)               = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-servicemanager) = %{version}

%description ServiceManager
The Service Locator design pattern is implemented by the Zend\ServiceManager
component. The Service Locator is a service/object locator, tasked with
retrieving other objects.

# ------------------------------------------------------------------------------

%package  Session

Summary:  Zend Framework 2: Session Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-session

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-hash
Requires: php-pcre
Requires: php-session
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-session) = %{version}

%description Session
Manage and preserve session data, a logical complement of cookie data, across
multiple page requests by the same client.

Optional: MongoDB (php-pecl-mongo)

# ------------------------------------------------------------------------------

%package  Soap

Summary:  Zend Framework 2: SOAP Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-soap

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-server)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-curl
Requires: php-dom
Requires: php-libxml
Requires: php-pcre
Requires: php-reflection
Requires: php-simplexml
Requires: php-soap
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-soap) = %{version}

%description Soap
%{summary}

# ------------------------------------------------------------------------------

%package  Stdlib

Summary:  Zend Framework 2: Stdlib Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-stdlib

Requires: %{name}-common         = %{version}-%{release}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-serializer)       = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-iconv
Requires: php-intl
Requires: php-json
Requires: php-mbstring
Requires: php-pcre
Requires: php-reflection
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-stdlib) = %{version}

%description Stdlib
%{summary}

# ------------------------------------------------------------------------------

%package  Tag

Summary:  Zend Framework 2: Tag Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.tag.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-tag) = %{version}

%description Tag
Zend\Tag is a component suite which provides a facility to work with taggable
Items. As its base, it provides two classes to work with Tags, Zend\Tag\Item
and Zend\Tag\ItemList. Additionally, it comes with the interface
Zend\Tag\TaggableInterface, which allows you to use any of your models as a
taggable item in conjunction with Zend\Tag.

Zend\Tag\Item is a basic taggable item implementation which comes with the
essential functionality required to work with the Zend\Tag suite. A taggable
item always consists of a title and a relative weight (e.g. number of
occurrences). It also stores parameters which are used by the different
sub-components of Zend\Tag.

To group multiple items together, Zend\Tag\ItemList exists as an array iterator
and provides additional functionality to calculate absolute weight values based
on the given relative weights of each item in it.

# ------------------------------------------------------------------------------

%package  Test

Summary:  Zend Framework 2: Test Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.test.introduction.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-console)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-dom)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-mvc)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-view)             = %{version}
Requires: php-phpunit-PHPUnit >= 3.7.0
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-test) = %{version}

%description Test
The Zend\Test component provides tools to facilitate unit testing of your Zend
Framework applications. At this time, we offer facilities to enable testing of
your Zend Framework MVC applications.

PHPUnit is the only library supported currently.

# ------------------------------------------------------------------------------

### TODO: Is Zend/Text/Figlet/zend-framework.flf allowed?

%package  Text

Summary:  Zend Framework 2: Text Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/index.html#zend-text

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-text) = %{version}

%description Text
%{summary}

# ------------------------------------------------------------------------------

%package  Uri

Summary:  Zend Framework 2: URI Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.uri.html

Requires: %{name}-common    = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-validator)        = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-uri) = %{version}

%description Uri
Zend\Uri is a component that aids in manipulating and validating Uniform
Resource Identifiers (URIs) [1]. Zend\Uri exists primarily to service other
components, such as Zend\Http\, but is also useful as a standalone utility.

URIs always begin with a scheme, followed by a colon. The construction of the
many different schemes varies significantly. The Zend\Uri component provides
the Zend\Uri\UriFactory that returns a class implementing the
Zend\Uri\UriInterface which specializes in the scheme if such a class is
registered with the Factory.

[1] http://www.ietf.org/rfc/rfc3986.txt

# ------------------------------------------------------------------------------

%package  Validator

Summary:  Zend Framework 2: Validator Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.validator.html

Requires: %{name}-common         = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
#     zendframework/zend-resources
Requires: php-composer(%{composer_vendor}/zend-db)               = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-session)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-ctype
Requires: php-date
Requires: php-fileinfo
Requires: php-hash
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-validator) = %{version}

%description Validator
The Zend\Validator component provides a set of commonly needed validators.
It also provides a simple validator chaining mechanism by which multiple
validators may be applied to a single datum in a user-defined order.

# ------------------------------------------------------------------------------

%package  Version

Summary:  Zend Framework 2: Version Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.version.html

Requires: %{name}-common = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-version) = %{version}

%description Version
Zend\Version provides a class constant Zend\Version\Version::VERSION that
contains a string identifying the version number of your Zend Framework
installation. Zend\Version\Version::VERSION might contain “1.7.4”, for
example.

The static method Zend\Version\Version::compareVersion($version) is based on
the PHP function version_compare(). This method returns -1 if the specified
version is older than the installed Zend Framework version, 0 if they are the
same and +1 if the specified version is newer than the version of the Zend
Framework installation.

# ------------------------------------------------------------------------------

%package  View

Summary:  Zend Framework 2: View Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.view.quick-start.html

Requires: %{name}-common          = %{version}-%{release}
# composer.json
Requires: php-composer(%{composer_vendor}/zend-eventmanager)     = %{version}
Requires: php-composer(%{composer_vendor}/zend-loader)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-authentication)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-escaper)          = %{version}
Requires: php-composer(%{composer_vendor}/zend-feed)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-filter)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-i18n)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-json)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-mvc)              = %{version}
Requires: php-composer(%{composer_vendor}/zend-navigation)       = %{version}
Requires: php-composer(%{composer_vendor}/zend-paginator)        = %{version}
Requires: php-composer(%{composer_vendor}/zend-permissions-acl)  = %{version}
Requires: php-composer(%{composer_vendor}/zend-servicemanager)   = %{version}
Requires: php-composer(%{composer_vendor}/zend-uri)              = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-dom
Requires: php-filter
Requires: php-pcre
Requires: php-spl

Provides: php-composer(%{composer_vendor}/zend-view) = %{version}

%description View
Zend\View provides the “View” layer of Zend Framework 2’s MVC system. It
is a multi-tiered system allowing a variety of mechanisms for extension,
substitution, and more.

# ------------------------------------------------------------------------------

%package  XmlRpc

Summary:  Zend Framework 2: XML-RPC Component
Group:    Development/Libraries
URL:      http://framework.zend.com/manual/2.3/en/modules/zend.xmlrpc.intro.html

Requires: %{name}-common  = %{version}-%{release}
Requires: php-composer(%{composer_vendor}/zendxml)
# composer.json
Requires: php-composer(%{composer_vendor}/zend-http)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-math)             = %{version}
Requires: php-composer(%{composer_vendor}/zend-server)           = %{version}
Requires: php-composer(%{composer_vendor}/zend-stdlib)           = %{version}
Requires: php-composer(%{composer_vendor}/zendxml)
# composer.json (optional)
Requires: php-composer(%{composer_vendor}/zend-cache)            = %{version}
# phpcompatinfo (computed from version 2.3.1)
Requires: php-date
Requires: php-dom
Requires: php-iconv
Requires: php-libxml
Requires: php-pcre
Requires: php-reflection
Requires: php-simplexml
Requires: php-spl
Requires: php-xmlwriter

Provides: php-composer(%{composer_vendor}/zend-xmlrpc) = %{version}

%description XmlRpc
From its home page, XML-RPC is described as a ”...remote procedure calling
using HTTP as the transport and XML as the encoding. XML-RPC is designed to
be as simple as possible, while allowing complex data structures to be
transmitted, processed and returned.”

Zend Framework provides support for both consuming remote XML-RPC services
and building new XML-RPC servers.

[1] http://www.xmlrpc.com/


# ##############################################################################


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee library/Zend/autoload.php
<?php
/*
Simple autoloader for Zend Framework
Inspired from https://github.com/zendframework/ZendSkeletonApplication

Set autoregister_zf     for Zend Framework
Set fallback_autoloader for dependencies which are PSR-0 compliant
*/
require_once __DIR__ . '/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'fallback_autoloader' => true,
        'autoregister_zf' => true
    )
));
AUTOLOAD


%install
mkdir -p %{buildroot}%{_datadir}/php
cp -rp library/* %{buildroot}%{_datadir}/php/

# Symlink package docs to common sub-package docs
mkdir -p %{buildroot}%{_docdir}
%if "%{_pkgdocdir}" == "%{_docdir}/%{name}"
ln -s %{name}-common            %{buildroot}%{_pkgdocdir}
%else
ln -s %{name}-common-%{version} %{buildroot}%{_pkgdocdir}
%endif


%check
%if %{with_tests}
cd tests
: Create autoloader for test suite
cat <<'AUTOLOADER' | tee _autoload.php
<?php
require_once '%{buildroot}%{_datadir}/php/Zend/autoload.php';

Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\\Loader\\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest' => __DIR__ . '/ZendTest',
        )
    )
));
AUTOLOADER

: ignore these for now
rm ZendTest/Mvc/Controller/Plugin/FilePostRedirectGetTest.php

%if 0%{?rhel} == 5
rm ZendTest/Feed/PubSubHubbub/Model/SubscriptionTest.php
rm ZendTest/Session/SaveHandler/DbTableGatewayTest.php
%endif

RET=0
for dir in ZendTest/[A-Z]*
do phpunit $dir || RET=1
done
exit $RET
%endif


%files
# Empty files section, included in sub-package "common"


# ##############################################################################

%files common
%defattr(-,root,root,-)

%{!?_licensedir:%global license %%doc}
%license LICENSE.txt
%doc *.md composer.json
%doc %{_pkgdocdir}

%dir %{_datadir}/php/Zend

# ------------------------------------------------------------------------------

%files Authentication
%defattr(-,root,root,-)

%doc library/Zend/Authentication/*.md
%doc library/Zend/Authentication/composer.json

%{_datadir}/php/Zend/Authentication
%exclude %{_datadir}/php/Zend/Authentication/*.md
%exclude %{_datadir}/php/Zend/Authentication/composer.json

# ------------------------------------------------------------------------------

%files Barcode
%defattr(-,root,root,-)

%doc library/Zend/Barcode/*.md
%doc library/Zend/Barcode/composer.json

%{_datadir}/php/Zend/Barcode
%exclude %{_datadir}/php/Zend/Barcode/*.md
%exclude %{_datadir}/php/Zend/Barcode/composer.json

# ------------------------------------------------------------------------------

%files Cache
%defattr(-,root,root,-)

%doc library/Zend/Cache/*.md
%doc library/Zend/Cache/composer.json

%{_datadir}/php/Zend/Cache
%exclude %{_datadir}/php/Zend/Cache/*.md
%exclude %{_datadir}/php/Zend/Cache/composer.json

# ------------------------------------------------------------------------------

%files Captcha
%defattr(-,root,root,-)

%doc library/Zend/Captcha/*.md
%doc library/Zend/Captcha/composer.json

%{_datadir}/php/Zend/Captcha
%exclude %{_datadir}/php/Zend/Captcha/*.md
%exclude %{_datadir}/php/Zend/Captcha/composer.json

# ------------------------------------------------------------------------------

%files Code
%defattr(-,root,root,-)

%doc library/Zend/Code/*.md
%doc library/Zend/Code/composer.json

%{_datadir}/php/Zend/Code
%exclude %{_datadir}/php/Zend/Code/*.md
%exclude %{_datadir}/php/Zend/Code/composer.json

# ------------------------------------------------------------------------------

%files Config
%defattr(-,root,root,-)

%doc library/Zend/Config/*.md
%doc library/Zend/Config/composer.json

%{_datadir}/php/Zend/Config
%exclude %{_datadir}/php/Zend/Config/*.md
%exclude %{_datadir}/php/Zend/Config/composer.json

# ------------------------------------------------------------------------------

%files Console
%defattr(-,root,root,-)

%doc library/Zend/Console/*.md
%doc library/Zend/Console/composer.json

%{_datadir}/php/Zend/Console
%exclude %{_datadir}/php/Zend/Console/*.md
%exclude %{_datadir}/php/Zend/Console/composer.json

# ------------------------------------------------------------------------------

%files Crypt
%defattr(-,root,root,-)

%doc library/Zend/Crypt/*.md
%doc library/Zend/Crypt/composer.json

%{_datadir}/php/Zend/Crypt
%exclude %{_datadir}/php/Zend/Crypt/*.md
%exclude %{_datadir}/php/Zend/Crypt/composer.json

# ------------------------------------------------------------------------------

%files Db
%defattr(-,root,root,-)

%doc library/Zend/Db/*.md
%doc library/Zend/Db/composer.json

%{_datadir}/php/Zend/Db
%exclude %{_datadir}/php/Zend/Db/*.md
%exclude %{_datadir}/php/Zend/Db/composer.json

# ------------------------------------------------------------------------------

%files Debug
%defattr(-,root,root,-)

%doc library/Zend/Debug/*.md
%doc library/Zend/Debug/composer.json

%{_datadir}/php/Zend/Debug
%exclude %{_datadir}/php/Zend/Debug/*.md
%exclude %{_datadir}/php/Zend/Debug/composer.json

# ------------------------------------------------------------------------------

%files Di
%defattr(-,root,root,-)

%doc library/Zend/Di/*.md
%doc library/Zend/Di/composer.json

%{_datadir}/php/Zend/Di
%exclude %{_datadir}/php/Zend/Di/*.md
%exclude %{_datadir}/php/Zend/Di/composer.json

# ------------------------------------------------------------------------------

%files Dom
%defattr(-,root,root,-)

%doc library/Zend/Dom/*.md
%doc library/Zend/Dom/composer.json

%{_datadir}/php/Zend/Dom
%exclude %{_datadir}/php/Zend/Dom/*.md
%exclude %{_datadir}/php/Zend/Dom/composer.json

# ------------------------------------------------------------------------------

%files Escaper
%defattr(-,root,root,-)

%doc library/Zend/Escaper/*.md
%doc library/Zend/Escaper/composer.json

%{_datadir}/php/Zend/Escaper
%exclude %{_datadir}/php/Zend/Escaper/*.md
%exclude %{_datadir}/php/Zend/Escaper/composer.json

# ------------------------------------------------------------------------------

%files EventManager
%defattr(-,root,root,-)

%doc library/Zend/EventManager/*.md
%doc library/Zend/EventManager/composer.json

%{_datadir}/php/Zend/EventManager
%exclude %{_datadir}/php/Zend/EventManager/*.md
%exclude %{_datadir}/php/Zend/EventManager/composer.json

# ------------------------------------------------------------------------------

%files Feed
%defattr(-,root,root,-)

%doc library/Zend/Feed/*.md
%doc library/Zend/Feed/composer.json

%{_datadir}/php/Zend/Feed
%exclude %{_datadir}/php/Zend/Feed/*.md
%exclude %{_datadir}/php/Zend/Feed/composer.json

# ------------------------------------------------------------------------------

%files File
%defattr(-,root,root,-)

%doc library/Zend/File/*.md
%doc library/Zend/File/composer.json

%{_datadir}/php/Zend/File
%exclude %{_datadir}/php/Zend/File/*.md
%exclude %{_datadir}/php/Zend/File/composer.json

# ------------------------------------------------------------------------------

%files Filter
%defattr(-,root,root,-)

%doc library/Zend/Filter/*.md
%doc library/Zend/Filter/composer.json

%{_datadir}/php/Zend/Filter
%exclude %{_datadir}/php/Zend/Filter/*.md
%exclude %{_datadir}/php/Zend/Filter/composer.json

# ------------------------------------------------------------------------------

%files Form
%defattr(-,root,root,-)

%doc library/Zend/Form/*.md
%doc library/Zend/Form/composer.json

%{_datadir}/php/Zend/Form
%exclude %{_datadir}/php/Zend/Form/*.md
%exclude %{_datadir}/php/Zend/Form/composer.json

# ------------------------------------------------------------------------------

%files Http
%defattr(-,root,root,-)

%doc library/Zend/Http/*.md
%doc library/Zend/Http/composer.json

%{_datadir}/php/Zend/Http
%exclude %{_datadir}/php/Zend/Http/*.md
%exclude %{_datadir}/php/Zend/Http/composer.json

# ------------------------------------------------------------------------------

%files I18n
%defattr(-,root,root,-)

%doc library/Zend/I18n/*.md
%doc library/Zend/I18n/composer.json

%{_datadir}/php/Zend/I18n
%exclude %{_datadir}/php/Zend/I18n/*.md
%exclude %{_datadir}/php/Zend/I18n/composer.json

# ------------------------------------------------------------------------------

%files InputFilter
%defattr(-,root,root,-)

%doc library/Zend/InputFilter/*.md
%doc library/Zend/InputFilter/composer.json

%{_datadir}/php/Zend/InputFilter
%exclude %{_datadir}/php/Zend/InputFilter/*.md
%exclude %{_datadir}/php/Zend/InputFilter/composer.json

# ------------------------------------------------------------------------------

%files Json
%defattr(-,root,root,-)

%doc library/Zend/Json/*.md
%doc library/Zend/Json/composer.json

%{_datadir}/php/Zend/Json
%exclude %{_datadir}/php/Zend/Json/*.md
%exclude %{_datadir}/php/Zend/Json/composer.json

# ------------------------------------------------------------------------------

%files Ldap
%defattr(-,root,root,-)

%doc library/Zend/Ldap/*.md
%doc library/Zend/Ldap/composer.json

%{_datadir}/php/Zend/Ldap
%exclude %{_datadir}/php/Zend/Ldap/*.md
%exclude %{_datadir}/php/Zend/Ldap/composer.json

# ------------------------------------------------------------------------------

%files Loader
%defattr(-,root,root,-)

%doc library/Zend/Loader/*.md
%doc library/Zend/Loader/composer.json

%{_datadir}/php/Zend/autoload.php
%{_datadir}/php/Zend/Loader
%exclude %{_datadir}/php/Zend/Loader/*.md
%exclude %{_datadir}/php/Zend/Loader/composer.json

# ------------------------------------------------------------------------------

%files Log
%defattr(-,root,root,-)

%doc library/Zend/Log/*.md
%doc library/Zend/Log/composer.json

%{_datadir}/php/Zend/Log
%exclude %{_datadir}/php/Zend/Log/*.md
%exclude %{_datadir}/php/Zend/Log/composer.json

# ------------------------------------------------------------------------------

%files Mail
%defattr(-,root,root,-)

%doc library/Zend/Mail/*.md
%doc library/Zend/Mail/composer.json

%{_datadir}/php/Zend/Mail
%exclude %{_datadir}/php/Zend/Mail/*.md
%exclude %{_datadir}/php/Zend/Mail/composer.json

# ------------------------------------------------------------------------------

%files Math
%defattr(-,root,root,-)

%doc library/Zend/Math/*.md
%doc library/Zend/Math/composer.json

%{_datadir}/php/Zend/Math
%exclude %{_datadir}/php/Zend/Math/*.md
%exclude %{_datadir}/php/Zend/Math/composer.json

# ------------------------------------------------------------------------------

%files Memory
%defattr(-,root,root,-)

%doc library/Zend/Memory/*.md
%doc library/Zend/Memory/composer.json

%{_datadir}/php/Zend/Memory
%exclude %{_datadir}/php/Zend/Memory/*.md
%exclude %{_datadir}/php/Zend/Memory/composer.json

# ------------------------------------------------------------------------------

%files Mime
%defattr(-,root,root,-)

%doc library/Zend/Mime/*.md
%doc library/Zend/Mime/composer.json

%{_datadir}/php/Zend/Mime
%exclude %{_datadir}/php/Zend/Mime/*.md
%exclude %{_datadir}/php/Zend/Mime/composer.json

# ------------------------------------------------------------------------------

%files ModuleManager
%defattr(-,root,root,-)

%doc library/Zend/ModuleManager/*.md
%doc library/Zend/ModuleManager/composer.json

%{_datadir}/php/Zend/ModuleManager
%exclude %{_datadir}/php/Zend/ModuleManager/*.md
%exclude %{_datadir}/php/Zend/ModuleManager/composer.json

# ------------------------------------------------------------------------------

%files Mvc
%defattr(-,root,root,-)

%doc library/Zend/Mvc/*.md
%doc library/Zend/Mvc/composer.json

%{_datadir}/php/Zend/Mvc
%exclude %{_datadir}/php/Zend/Mvc/*.md
%exclude %{_datadir}/php/Zend/Mvc/composer.json

# ------------------------------------------------------------------------------

%files Navigation
%defattr(-,root,root,-)

%doc library/Zend/Navigation/*.md
%doc library/Zend/Navigation/composer.json

%{_datadir}/php/Zend/Navigation
%exclude %{_datadir}/php/Zend/Navigation/*.md
%exclude %{_datadir}/php/Zend/Navigation/composer.json

# ------------------------------------------------------------------------------

%files Paginator
%defattr(-,root,root,-)

%doc library/Zend/Paginator/*.md
%doc library/Zend/Paginator/composer.json

%{_datadir}/php/Zend/Paginator
%exclude %{_datadir}/php/Zend/Paginator/*.md
%exclude %{_datadir}/php/Zend/Paginator/composer.json

# ------------------------------------------------------------------------------

%files Permissions-Acl
%defattr(-,root,root,-)

%doc library/Zend/Permissions/Acl/*.md
%doc library/Zend/Permissions/Acl/composer.json

%dir %{_datadir}/php/Zend/Permissions
     %{_datadir}/php/Zend/Permissions/Acl
%exclude %{_datadir}/php/Zend/Permissions/Acl/*.md
%exclude %{_datadir}/php/Zend/Permissions/Acl/composer.json

# ------------------------------------------------------------------------------

%files Permissions-Rbac
%defattr(-,root,root,-)

%doc library/Zend/Permissions/Rbac/*.md
%doc library/Zend/Permissions/Rbac/composer.json

%dir %{_datadir}/php/Zend/Permissions
     %{_datadir}/php/Zend/Permissions/Rbac
%exclude %{_datadir}/php/Zend/Permissions/Rbac/*.md
%exclude %{_datadir}/php/Zend/Permissions/Rbac/composer.json

# ------------------------------------------------------------------------------

%files ProgressBar
%defattr(-,root,root,-)

%doc library/Zend/ProgressBar/*.md
%doc library/Zend/ProgressBar/composer.json

%{_datadir}/php/Zend/ProgressBar
%exclude %{_datadir}/php/Zend/ProgressBar/*.md
%exclude %{_datadir}/php/Zend/ProgressBar/composer.json

# ------------------------------------------------------------------------------

%files Serializer
%defattr(-,root,root,-)

%doc library/Zend/Serializer/*.md
%doc library/Zend/Serializer/composer.json

%{_datadir}/php/Zend/Serializer
%exclude %{_datadir}/php/Zend/Serializer/*.md
%exclude %{_datadir}/php/Zend/Serializer/composer.json

# ------------------------------------------------------------------------------

%files Server
%defattr(-,root,root,-)

%doc library/Zend/Server/*.md
%doc library/Zend/Server/composer.json

%{_datadir}/php/Zend/Server
%exclude %{_datadir}/php/Zend/Server/*.md
%exclude %{_datadir}/php/Zend/Server/composer.json

# ------------------------------------------------------------------------------

%files ServiceManager
%defattr(-,root,root,-)

%doc library/Zend/ServiceManager/*.md
%doc library/Zend/ServiceManager/composer.json

%{_datadir}/php/Zend/ServiceManager
%exclude %{_datadir}/php/Zend/ServiceManager/*.md
%exclude %{_datadir}/php/Zend/ServiceManager/composer.json

# ------------------------------------------------------------------------------

%files Session
%defattr(-,root,root,-)

%doc library/Zend/Session/*.md
%doc library/Zend/Session/composer.json

%{_datadir}/php/Zend/Session
%exclude %{_datadir}/php/Zend/Session/*.md
%exclude %{_datadir}/php/Zend/Session/composer.json

# ------------------------------------------------------------------------------

%files Soap
%defattr(-,root,root,-)

%doc library/Zend/Soap/*.md
%doc library/Zend/Soap/composer.json

%{_datadir}/php/Zend/Soap
%exclude %{_datadir}/php/Zend/Soap/*.md
%exclude %{_datadir}/php/Zend/Soap/composer.json

# ------------------------------------------------------------------------------

%files Stdlib
%defattr(-,root,root,-)

%doc library/Zend/Stdlib/*.md
%doc library/Zend/Stdlib/composer.json

%{_datadir}/php/Zend/Stdlib
%exclude %{_datadir}/php/Zend/Stdlib/*.md
%exclude %{_datadir}/php/Zend/Stdlib/composer.json

# ------------------------------------------------------------------------------

%files Tag
%defattr(-,root,root,-)

%doc library/Zend/Tag/*.md
%doc library/Zend/Tag/composer.json

%{_datadir}/php/Zend/Tag
%exclude %{_datadir}/php/Zend/Tag/*.md
%exclude %{_datadir}/php/Zend/Tag/composer.json

# ------------------------------------------------------------------------------

%files Test
%defattr(-,root,root,-)

%doc library/Zend/Test/*.md
%doc library/Zend/Test/composer.json

%{_datadir}/php/Zend/Test
%exclude %{_datadir}/php/Zend/Test/*.md
%exclude %{_datadir}/php/Zend/Test/composer.json

# ------------------------------------------------------------------------------

%files Text
%defattr(-,root,root,-)

%doc library/Zend/Text/*.md
%doc library/Zend/Text/composer.json

%{_datadir}/php/Zend/Text
%exclude %{_datadir}/php/Zend/Text/*.md
%exclude %{_datadir}/php/Zend/Text/composer.json

# ------------------------------------------------------------------------------

%files Uri
%defattr(-,root,root,-)

%doc library/Zend/Uri/*.md
%doc library/Zend/Uri/composer.json

%{_datadir}/php/Zend/Uri
%exclude %{_datadir}/php/Zend/Uri/*.md
%exclude %{_datadir}/php/Zend/Uri/composer.json

# ------------------------------------------------------------------------------

%files Validator
%defattr(-,root,root,-)

%doc library/Zend/Validator/*.md
%doc library/Zend/Validator/composer.json

%{_datadir}/php/Zend/Validator
%exclude %{_datadir}/php/Zend/Validator/*.md
%exclude %{_datadir}/php/Zend/Validator/composer.json

# ------------------------------------------------------------------------------

%files Version
%defattr(-,root,root,-)

%doc library/Zend/Version/*.md
%doc library/Zend/Version/composer.json

%{_datadir}/php/Zend/Version
%exclude %{_datadir}/php/Zend/Version/*.md
%exclude %{_datadir}/php/Zend/Version/composer.json

# ------------------------------------------------------------------------------

%files View
%defattr(-,root,root,-)

%doc library/Zend/View/*.md
%doc library/Zend/View/composer.json

%{_datadir}/php/Zend/View
%exclude %{_datadir}/php/Zend/View/*.md
%exclude %{_datadir}/php/Zend/View/composer.json

# ------------------------------------------------------------------------------

%files XmlRpc
%defattr(-,root,root,-)

%doc library/Zend/XmlRpc/*.md
%doc library/Zend/XmlRpc/composer.json

%{_datadir}/php/Zend/XmlRpc
%exclude %{_datadir}/php/Zend/XmlRpc/*.md
%exclude %{_datadir}/php/Zend/XmlRpc/composer.json

# ##############################################################################

%changelog
* Sun Jun 12 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.4.10-1
- Update to 2.4.10 (RHBZ #1343995 / RHBZ #1343990)
- Switch to GitHub source (and separate ZendXml pkg)
- Move autoloader into spec

* Wed Nov 25 2015 Remi Collet <remi@fedoraproject.org> - 2.4.9-1
- Update to 2.4.9

* Wed Sep 16 2015 Remi Collet <remi@fedoraproject.org> - 2.4.8-1
- Update to 2.4.8

* Wed Aug 12 2015 Remi Collet <remi@fedoraproject.org> - 2.4.7-1
- Update to 2.4.7
- add autoloader in php-ZendFramework2-Loader

* Thu May 21 2015 Remi Collet <remi@fedoraproject.org> - 2.3.9-1
- Update to 2.3.9

* Fri May  8 2015 Remi Collet <remi@fedoraproject.org> - 2.3.8-1
- Update to 2.3.8

* Fri Mar 13 2015 Remi Collet <remi@fedoraproject.org> - 2.3.7-1
- Update to 2.3.7

* Thu Mar 12 2015 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- Update to 2.3.6

* Tue Feb 24 2015 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- Update to 2.3.5
- add patch for icu 54, FTBFS detected by Koschei

* Fri Jan 16 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4
- drop GLPI patch, fixed upstream

* Fri Oct 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.3.3-2
- Drop php-gmp dependency from Math component (BZ #1152440)
- Fix tests' autoloader

* Wed Sep 17 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Wed Aug 13 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2
- tests from github
- run test suite during build

* Sun Jul 20 2014 Remi Collet <remi@fedoraproject.org> - 2.3.1-3
- composer dependencies
- add missing license

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> 2.3.1-1
- backport 2.3.1 for remi repo

* Tue May 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.3.1-1
- Updated to 2.3.1

* Mon May 19 2014 Remi Collet <remi@fedoraproject.org> 2.2.7-1
- backport 2.2.7 for remi repo (security update for ZF2014-03)

* Sun May 18 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.7-1
- Updated to 2.2.7 (security update for ZF2014-03)

* Tue Apr  1 2014 Remi Collet <remi@fedoraproject.org> 2.2.6-1
- Updated to 2.2.6 for CVE-2014-2681 CVE-2014-2682
  CVE-2014-2683 CVE-2014-2684 CVE-2014-2685
- new package ZendXml
- fix for unversioned doc directory

* Mon Nov 11 2013 Remi Collet <remi@fedoraproject.org> 2.2.5-1
- backport 2.2.5 for remi repo

* Sun Nov 10 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.5-1
- Updated to 2.2.5
- Fixed Serializer sub-pkg broken dependency (php-pecl(msgpack) on ppc64)

* Wed Oct 02 2013 Remi Collet <remi@fedoraproject.org> 2.2.4-2
- Add patch needed for GLPI #1014478 (ZF-11974)

* Sun Sep 29 2013 Remi Collet <remi@fedoraproject.org> 2.2.4-1
- backport 2.2.4 for remi repo

* Thu Sep 12 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.4-1
- Updated to 2.2.4
- Versioned conflict
- Macros in comment fix

* Mon Jul 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.1-2
- Added php-ZendFramework conflict

* Mon Jul 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.1-1
- Initial package
