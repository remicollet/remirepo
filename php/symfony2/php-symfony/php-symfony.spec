%global github_owner            symfony
%global github_name             symfony
%global github_version          2.3.7
%global github_commit           2829b471871c2564228fe9f0832a0f928a8ffaa1

%global php_min_ver             5.3.3
# "doctrine/common": "~2.2" (composer.json)
%global doctrine_common_min_ver 2.2
%global doctrine_common_max_ver 3.0
# "doctrine/dbal": "~2.2" (composer.json)
%global doctrine_dbal_min_ver   2.2
%global doctrine_dbal_max_ver   3.0
# "doctrine/orm": "~2.2,>=2.2.3" (composer.json)
%global doctrine_orm_min_ver    2.2.3
%global doctrine_orm_max_ver    3.0
# "ircmaxell/password-compat": "1.0.*" (composer.json)
%global password_compat_min_ver 1.0.0
%global password_compat_max_ver 1.1.0
# "monolog/monolog": "~1.3" (composer.json)
%global monolog_min_ver         1.3
%global monolog_max_ver         2.0
# "psr/log": "~1.0" (composer.json)
%global psrlog_min_ver          1.0
%global psrlog_max_ver          2.0
# "swiftmailer/swiftmailer": ">=4.2.0,<5.1-dev" (src/Symfony/Bridge/Swiftmailer/composer.json)
%global swift_min_ver           4.2.0
%global swift_max_ver           5.1.0
# "symfony/icu": "~1.0" (composer.json)
%global symfony_icu_min_ver     1.0
%global symfony_icu_max_ver     2.0
# "twig/twig": "~1.11" (composer.json)
%global twig_min_ver            1.11
%global twig_max_ver            2.0

%global symfony_dir             %{_datadir}/php/Symfony
%global pear_channel            pear.symfony.com

Name:          php-symfony
Version:       %{github_version}
Release:       3%{dist}
Summary:       PHP framework for web projects

Group:         Development/Libraries
License:       MIT
URL:           http://symfony.com
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-Monolog   >= %{monolog_min_ver}
BuildRequires: php-Monolog   <  %{monolog_max_ver}
BuildRequires: php-PsrLog    >= %{psrlog_min_ver}
BuildRequires: php-PsrLog    <  %{psrlog_max_ver}
BuildRequires: %{name}-icu   >= %{symfony_icu_min_ver}
BuildRequires: %{name}-icu   <  %{symfony_icu_max_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineCommon) >= %{doctrine_common_min_ver}
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineCommon) <  %{doctrine_common_max_ver}
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineDBAL)   >= %{doctrine_dbal_min_ver}
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineDBAL)   <  %{doctrine_dbal_max_ver}
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineORM)    >= %{doctrine_orm_min_ver}
BuildRequires: php-pear(pear.doctrine-project.org/DoctrineORM)    <  %{doctrine_orm_max_ver}
BuildRequires: php-pear(pear.twig-project.org/Twig)               >= %{twig_min_ver}
BuildRequires: php-pear(pear.twig-project.org/Twig)               <  %{twig_max_ver}
%if 0%{?rhel}
BuildRequires: php-password-compat >= %{password_compat_min_ver}
BuildRequires: php-password-compat <  %{password_compat_max_ver}
%endif
## TODO: "doctrine/data-fixtures": "1.0.*"
## TODO: "propel/propel1": "1.6.*"
## TODO: "ocramius/proxy-manager": ">=0.3.1,<0.4-dev"
# For tests: phpcompatinfo
BuildRequires: php-ctype
BuildRequires: php-date
BuildRequires: php-dom
BuildRequires: php-fileinfo
BuildRequires: php-filter
BuildRequires: php-hash
BuildRequires: php-iconv
BuildRequires: php-intl
BuildRequires: php-json
BuildRequires: php-libxml
BuildRequires: php-mbstring
BuildRequires: php-openssl
BuildRequires: php-pcntl
BuildRequires: php-pcre
BuildRequires: php-pdo
BuildRequires: php-posix
# php-cli instead of php-readline for EL-5
BuildRequires: php-cli
BuildRequires: php-reflection
BuildRequires: php-session
BuildRequires: php-simplexml
BuildRequires: php-sockets
BuildRequires: php-spl
BuildRequires: php-sqlite3
BuildRequires: php-tokenizer
BuildRequires: php-xml

# Bridges
Requires:      %{name}-doctrinebridge      = %{version}-%{release}
Requires:      %{name}-monologbridge       = %{version}-%{release}
#Requires:      %%{name}-propel1bridge       = %%{version}-%%{release}
#Requires:      %%{name}-proxymanagerbridge  = %%{version}-%%{release}
Requires:      %{name}-swiftmailerbridge   = %{version}-%{release}
Requires:      %{name}-twigbridge          = %{version}-%{release}
# Bundles
Requires:      %{name}-frameworkbundle     = %{version}-%{release}
Requires:      %{name}-securitybundle      = %{version}-%{release}
Requires:      %{name}-twigbundle          = %{version}-%{release}
Requires:      %{name}-webprofilerbundle   = %{version}-%{release}
# Components
Requires:      %{name}-browserkit          = %{version}-%{release}
Requires:      %{name}-classloader         = %{version}-%{release}
Requires:      %{name}-config              = %{version}-%{release}
Requires:      %{name}-console             = %{version}-%{release}
Requires:      %{name}-cssselector         = %{version}-%{release}
Requires:      %{name}-debug               = %{version}-%{release}
Requires:      %{name}-dependencyinjection = %{version}-%{release}
Requires:      %{name}-domcrawler          = %{version}-%{release}
Requires:      %{name}-eventdispatcher     = %{version}-%{release}
Requires:      %{name}-filesystem          = %{version}-%{release}
Requires:      %{name}-finder              = %{version}-%{release}
Requires:      %{name}-form                = %{version}-%{release}
Requires:      %{name}-httpfoundation      = %{version}-%{release}
Requires:      %{name}-httpkernel          = %{version}-%{release}
Requires:      %{name}-intl                = %{version}-%{release}
Requires:      %{name}-locale              = %{version}-%{release}
Requires:      %{name}-optionsresolver     = %{version}-%{release}
Requires:      %{name}-process             = %{version}-%{release}
Requires:      %{name}-propertyaccess      = %{version}-%{release}
Requires:      %{name}-routing             = %{version}-%{release}
Requires:      %{name}-security            = %{version}-%{release}
Requires:      %{name}-serializer          = %{version}-%{release}
Requires:      %{name}-stopwatch           = %{version}-%{release}
Requires:      %{name}-templating          = %{version}-%{release}
Requires:      %{name}-translation         = %{version}-%{release}
Requires:      %{name}-validator           = %{version}-%{release}
Requires:      %{name}-yaml                = %{version}-%{release}

%description
%{summary}

# ##############################################################################

%package   common

Summary:   Symfony common files
Group:     Development/Libraries

Requires:  php(language) >= %{php_min_ver}

Obsoletes: php-channel-symfony2

%description common
%{summary}

# ------------------------------------------------------------------------------

%package  doctrinebridge

Summary:  Symfony Doctrine Bridge
Group:    Development/Libraries

Requires: php-pear(pear.doctrine-project.org/DoctrineCommon) >= %{doctrine_common_min_ver}
Requires: php-pear(pear.doctrine-project.org/DoctrineCommon) <  %{doctrine_common_max_ver}
# Optional
Requires: %{name}-form      = %{version}-%{release}
Requires: %{name}-validator = %{version}-%{release}
Requires: php-pear(pear.doctrine-project.org/DoctrineDBAL)   >= %{doctrine_dbal_min_ver}
Requires: php-pear(pear.doctrine-project.org/DoctrineDBAL)   <  %{doctrine_dbal_max_ver}
Requires: php-pear(pear.doctrine-project.org/DoctrineORM)    >= %{doctrine_orm_min_ver}
Requires: php-pear(pear.doctrine-project.org/DoctrineORM)    <  %{doctrine_orm_max_ver}
# phpcompatinfo
Requires: php-date
Requires: php-json
Requires: php-mbstring
Requires: php-pcre
Requires: php-pdo
Requires: php-reflection
Requires: php-session
Requires: php-spl

# PEAR
Provides: php-pear(%{pear_channel}/DoctrineBridge) = %{version}

%description doctrinebridge
Provides integration for Doctrine (http://www.doctrine-project.org/) with
various Symfony components.

Configuration reference:
http://symfony.com/doc/current/reference/configuration/doctrine.html

# ------------------------------------------------------------------------------

%package  monologbridge

Summary:  Symfony Monolog Bridge
Group:    Development/Libraries

Requires: %{name}-httpkernel =  %{version}-%{release}
Requires: php-Monolog        >= %{monolog_min_ver}
Requires: php-Monolog        <  %{monolog_max_ver}
# phpcompatinfo
Requires: php-pcre

# PEAR
Provides: php-pear(%{pear_channel}/MonologBridge) = %{version}

%description monologbridge
Provides integration for Monolog (https://github.com/Seldaek/monolog) with
various Symfony components.

Configuration reference:
http://symfony.com/doc/current/reference/configuration/monolog.html

# ------------------------------------------------------------------------------

#%%package  propel1bridge

#Summary:  Symfony Propel 1 Bridge
#Group:    Development/Libraries

#Requires: %%{name}-httpfoundation = %%{version}-%%{release}
#Requires: %%{name}-httpkernel     = %%{version}-%%{release}
#Requires: %%{name}-form           = %%{version}-%%{release}
## propel/propel1 1.6.*

#%%description propel1bridge
#Provides integration for Propel 1 (http://propelorm.org/) with various
#Symfony components.

# ------------------------------------------------------------------------------

#%%package  proxymanagerbridge
#Group:    Development/Libraries

#Summary:  Symfony ProxyManager Bridge

#Requires: %%{name}-dependencyinjection = %%{version}-%%{release}
## ocramius/proxy-manager >=0.3.1,<0.4-dev
## phpcompatinfo
#Requires: php-reflection
#Requires: php-spl

#%%description proxymanagerbridge
#Provides integration for ProxyManager (https://github.com/Ocramius/ProxyManager)
#with various Symfony components.

# ------------------------------------------------------------------------------

%package  swiftmailerbridge

Summary:  Symfony Swiftmailer Bridge
Group:    Development/Libraries

Requires: php-pear(pear.swiftmailer.org/Swift) >= %{swift_min_ver}
Requires: php-pear(pear.swiftmailer.org/Swift) <  %{swift_max_ver}
# Optional
Requires: %{name}-httpkernel = %{version}-%{release}

%description swiftmailerbridge
Provides integration for Swift Mailer (http://swiftmailer.org/) with various
Symfony components.

Configuration reference:
http://symfony.com/doc/current/reference/configuration/swiftmailer.html

# ------------------------------------------------------------------------------

%package  twigbridge

Summary:  Symfony Twig Bridge
Group:    Development/Libraries

Requires: php-pear(pear.twig-project.org/Twig) >= %{twig_min_ver}
Requires: php-pear(pear.twig-project.org/Twig) <  %{twig_max_ver}
# Optional
Requires: %{name}-form        = %{version}-%{release}
Requires: %{name}-httpkernel  = %{version}-%{release}
Requires: %{name}-routing     = %{version}-%{release}
Requires: %{name}-security    = %{version}-%{release}
Requires: %{name}-templating  = %{version}-%{release}
Requires: %{name}-translation = %{version}-%{release}
Requires: %{name}-yaml        = %{version}-%{release}
# phpcompatinfo
Requires: php-pcre
Requires: php-spl

# PEAR
Provides: php-pear(%{pear_channel}/TwigBridge) = %{version}

%description twigbridge
Provides integration for Twig (http://twig.sensiolabs.org/) with various
Symfony components.

# ------------------------------------------------------------------------------

%package  frameworkbundle

Summary:  Symfony Framework Bundle
Group:    Development/Libraries

Requires: %{name}-config              = %{version}-%{release}
Requires: %{name}-dependencyinjection = %{version}-%{release}
Requires: %{name}-eventdispatcher     = %{version}-%{release}
Requires: %{name}-filesystem          = %{version}-%{release}
Requires: %{name}-httpkernel          = %{version}-%{release}
Requires: %{name}-routing             = %{version}-%{release}
Requires: %{name}-stopwatch           = %{version}-%{release}
Requires: %{name}-templating          = %{version}-%{release}
Requires: %{name}-translation         = %{version}-%{release}
Requires: php-pear(pear.doctrine-project.org/DoctrineCommon) >= %{doctrine_common_min_ver}
Requires: php-pear(pear.doctrine-project.org/DoctrineCommon) <  %{doctrine_common_max_ver}
# Optional
Requires: %{name}-console             = %{version}-%{release}
Requires: %{name}-finder              = %{version}-%{release}
Requires: %{name}-form                = %{version}-%{release}
Requires: %{name}-validator           = %{version}-%{release}
# phpcompatinfo
Requires: php-date
Requires: php-fileinfo
Requires: php-filter
Requires: php-json
Requires: php-pcre
Requires: php-reflection
Requires: php-session
Requires: php-spl
Requires: php-tokenizer

%description frameworkbundle
The FrameworkBundle contains most of the "base" framework functionality and can
be configured under the framework key in your application configuration. This
includes settings related to sessions, translation, forms, validation, routing
and more.

Configuration reference:
http://symfony.com/doc/current/reference/configuration/framework.html

# ------------------------------------------------------------------------------

%package  securitybundle

Summary:  Symfony Security Bundle
Group:    Development/Libraries

Requires: %{name}-httpkernel = %{version}-%{release}
Requires: %{name}-security   = %{version}-%{release}
# phpcompatinfo
Requires: php-pcre
Requires: php-spl

%description securitybundle
%{summary}

# ------------------------------------------------------------------------------

%package  twigbundle

Summary:  Symfony Twig Bundle
Group:    Development/Libraries

Requires: %{name}-httpkernel = %{version}-%{release}
Requires: %{name}-twigbridge = %{version}-%{release}
# phpcompatinfo
Requires: php-ctype
Requires: php-reflection
Requires: php-spl

%description twigbundle
%{summary}

Configuration reference:
http://symfony.com/doc/current/reference/configuration/twig.html

# ------------------------------------------------------------------------------

%package  webprofilerbundle

Summary:  Symfony WebProfiler Bundle
Group:    Development/Libraries

Requires: %{name}-httpkernel = %{version}-%{release}
Requires: %{name}-routing    = %{version}-%{release}
Requires: %{name}-twigbridge = %{version}-%{release}
# phpcompatinfo
Requires: php-pcre
Requires: php-spl

%description webprofilerbundle
%{summary}

Configuration reference:
http://symfony.com/doc/current/reference/configuration/web_profiler.html

# ------------------------------------------------------------------------------

%package   browserkit

Summary:   Symfony BrowserKit Component
Group:     Development/Libraries

Requires:  %{name}-domcrawler = %{version}-%{release}
# Optional
Requires:  %{name}-process    = %{version}-%{release}
# phpcompatinfo
Requires:  php-date
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/BrowserKit) = %{version}
# Rename
Obsoletes: %{name}2-BrowserKit < %{version}
Provides:  %{name}2-BrowserKit = %{version}

%description browserkit
BrowserKit simulates the behavior of a web browser.

The component only provide an abstract client and does not provide any
"default" backend for the HTTP layer.

# ------------------------------------------------------------------------------

%package   classloader

Summary:   Symfony ClassLoader Component
URL:       http://symfony.com/doc/current/components/class_loader/index.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-spl
Requires:  php-tokenizer

# PEAR
Provides:  php-pear(%{pear_channel}/ClassLoader) = %{version}
# Rename
Obsoletes: %{name}2-ClassLoader < %{version}
Provides:  %{name}2-ClassLoader = %{version}

%description classloader
The ClassLoader Component loads your project classes automatically if they
follow some standard PHP conventions.

Whenever you use an undefined class, PHP uses the autoloading mechanism
to delegate the loading of a file defining the class. Symfony provides
a "universal" autoloader, which is able to load classes from files that
implement one of the following conventions:
* The technical interoperability standards [1] for PHP 5.3 namespaces
  and class names
* The PEAR naming convention [2] for classes

If your classes and the third-party libraries you use for your project follow
these standards, the Symfony autoloader is the only autoloader you will ever
need.

Optional: APC, XCache

[1] http://symfony.com/PSR0
[2] http://pear.php.net/manual/en/standards.php

# ------------------------------------------------------------------------------

%package   config

Summary:   Symfony Config Component
URL:       http://symfony.com/doc/current/components/config/index.html
Group:     Development/Libraries

Requires:  %{name}-filesystem = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-dom
Requires:  php-json
Requires:  php-libxml
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Config) = %{version}
# Rename
Obsoletes: %{name}2-Config < %{version}
Provides:  %{name}2-Config = %{version}

%description config
The Config Component provides several classes to help you find, load, combine,
autofill and validate configuration values of any kind, whatever their source
may be (Yaml, XML, INI files, or for instance a database).

# ------------------------------------------------------------------------------

%package   console

Summary:   Symfony Console Component
URL:       http://symfony.com/doc/current/components/console/index.html
Group:     Development/Libraries

# Optional
Requires:  %{name}-eventdispatcher = %{version}-%{release}
# phpcompatinfo
Requires:  php-date
Requires:  php-dom
Requires:  php-json
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-posix
Requires:  php-readline
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Console) = %{version}
# Rename
Obsoletes: %{name}2-Console < %{version}
Provides:  %{name}2-Console = %{version}

%description console
The Console component eases the creation of beautiful and testable command line
interfaces.

The Console component allows you to create command-line commands. Your console
commands can be used for any recurring task, such as cronjobs, imports, or
other batch jobs.

# ------------------------------------------------------------------------------

%package   cssselector

Summary:   Symfony CssSelector Component
URL:       http://symfony.com/doc/current/components/css_selector.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-mbstring
Requires:  php-pcre

# PEAR
Provides:  php-pear(%{pear_channel}/CssSelector) = %{version}
# Rename
Obsoletes: %{name}2-CssSelector < %{version}
Provides:  %{name}2-CssSelector = %{version}

%description cssselector
The CssSelector Component converts CSS selectors to XPath expressions.

# ------------------------------------------------------------------------------

## TODO: xdebug optional?  NOTE: HttpKernel requires this component

%package  debug

Summary:  Symfony Debug Component
URL:      http://symfony.com/doc/current/components/debug.html
Group:    Development/Libraries

# Optional
Requires: %{name}-classloader    = %{version}-%{release}
Requires: %{name}-httpfoundation = %{version}-%{release}
Requires: %{name}-httpkernel     = %{version}-%{release}
# phpcompatinfo
#Requires: php-pecl(xdebug)
Requires: php-spl

# PEAR
Provides: php-pear(%{pear_channel}/Debug) = %{version}
# Rename
Obsoletes: %{name}2-Debug < %{version}
Provides:  %{name}2-Debug = %{version}

%description debug
The Debug Component provides tools to ease debugging PHP code.

# ------------------------------------------------------------------------------

%package   dependencyinjection

Summary:   Symfony DependencyInjection Component
URL:       http://symfony.com/doc/current/components/dependency_injection/index.html
Group:     Development/Libraries

# Optional
Requires:  %{name}-config = %{version}-%{release}
#Requires:  %%{name}-proxymanagerbridge = %%{version}-%%{release}
Requires:  %{name}-yaml   = %{version}-%{release}
# phpcompatinfo
Requires:  php-dom
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-simplexml
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/DependencyInjection) = %{version}
# Rename
Obsoletes: %{name}2-DependencyInjection < %{version}
Provides:  %{name}2-DependencyInjection = %{version}

%description dependencyinjection
The Dependency Injection component allows you to standardize and centralize
the way objects are constructed in your application.

# ------------------------------------------------------------------------------

%package   domcrawler

Summary:   Symfony DomCrawler Component
URL:       http://symfony.com/doc/current/components/dom_crawler.html
Group:     Development/Libraries

# Optional
Requires:  %{name}-cssselector = %{version}-%{release}
# phpcompatinfo
Requires:  php-dom
Requires:  php-libxml
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/DomCrawler) = %{version}
# Rename
Obsoletes: %{name}2-DomCrawler < %{version}
Provides:  %{name}2-DomCrawler = %{version}

%description domcrawler
The DomCrawler Component eases DOM navigation for HTML and XML documents.

# ------------------------------------------------------------------------------

%package   eventdispatcher

Summary:   Symfony EventDispatcher Component
URL:       http://symfony.com/doc/current/components/event_dispatcher/index.html
Group:     Development/Libraries

# Optional
Requires:  %{name}-dependencyinjection = %{version}-%{release}
Requires:  %{name}-httpkernel          = %{version}-%{release}
# phpcompatinfo
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/EventDispatcher) = %{version}
# Rename
Obsoletes: %{name}2-EventDispatcher < %{version}
Provides:  %{name}2-EventDispatcher = %{version}

%description eventdispatcher
The Symfony Event Dispatcher component implements the Observer [1] pattern in
a simple and effective way to make all these things possible and to make your
projects truly extensible.

[1] http://en.wikipedia.org/wiki/Observer_pattern

# ------------------------------------------------------------------------------

%package   filesystem

Summary:   Symfony Filesystem Component
URL:       http://symfony.com/doc/current/components/filesystem.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Filesystem) = %{version}
# Rename
Obsoletes: %{name}2-Filesystem < %{version}
Provides:  %{name}2-Filesystem = %{version}

%description filesystem
The Filesystem component provides basic utilities for the filesystem.

# ------------------------------------------------------------------------------

%package   finder

Summary:   Symfony Finder Component
URL:       http://symfony.com/doc/current/components/finder.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-date
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Finder) = %{version}
# Rename
Obsoletes: %{name}2-Finder < %{version}
Provides:  %{name}2-Finder = %{version}

%description finder
The Finder Component finds files and directories via an intuitive fluent
interface.

# ------------------------------------------------------------------------------

%package   form

Summary:   Symfony Form Component
Group:     Development/Libraries

Requires:  %{name}-eventdispatcher = %{version}-%{release}
Requires:  %{name}-intl            = %{version}-%{release}
Requires:  %{name}-optionsresolver = %{version}-%{release}
Requires:  %{name}-propertyaccess  = %{version}-%{release}
# Optional
Requires:  %{name}-httpfoundation  = %{version}-%{release}
Requires:  %{name}-validator       = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-date
Requires:  php-intl
Requires:  php-json
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-session
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Form) = %{version}
# Rename
Obsoletes: %{name}2-Form < %{version}
Provides:  %{name}2-Form = %{version}

%description form
Form provides tools for defining forms, rendering and mapping request data
to related models. Furthermore it provides integration with the Validation
component.

# ------------------------------------------------------------------------------

%package   httpfoundation

Summary:   Symfony HttpFoundation Component
URL:       http://symfony.com/doc/current/components/http_foundation/index.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-date
Requires:  php-fileinfo
Requires:  php-filter
Requires:  php-json
Requires:  php-pcre
Requires:  php-pdo
Requires:  php-session
Requires:  php-sockets
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/HttpFoundation) = %{version}
# Rename
Obsoletes: %{name}2-HttpFoundation < %{version}
Provides:  %{name}2-HttpFoundation = %{version}

%description httpfoundation
The HttpFoundation Component defines an object-oriented layer for the HTTP
specification.

In PHP, the request is represented by some global variables ($_GET, $_POST,
$_FILES, $_COOKIE, $_SESSION, ...) and the response is generated by some
functions (echo, header, setcookie, ...).

The Symfony HttpFoundation component replaces these default PHP global
variables and functions by an Object-Oriented layer.

Optional: memcache, memcached, mongo

# ------------------------------------------------------------------------------

%package   httpkernel

Summary:   Symfony HttpKernel Component
URL:       http://symfony.com/doc/current/components/http_kernel/index.html
Group:     Development/Libraries

Requires:  %{name}-debug               =  %{version}-%{release}
Requires:  %{name}-eventdispatcher     =  %{version}-%{release}
Requires:  %{name}-httpfoundation      =  %{version}-%{release}
Requires:  php-PsrLog                  >= %{psrlog_min_ver}
Requires:  php-PsrLog                  <  %{psrlog_max_ver}
# Optional
Requires:  %{name}-browserkit          =  %{version}-%{release}
Requires:  %{name}-classloader         =  %{version}-%{release}
Requires:  %{name}-config              =  %{version}-%{release}
Requires:  %{name}-console             =  %{version}-%{release}
Requires:  %{name}-dependencyinjection =  %{version}-%{release}
Requires:  %{name}-finder              =  %{version}-%{release}
# phpcompatinfo
Requires:  php-date
Requires:  php-hash
Requires:  php-json
Requires:  php-pcre
Requires:  php-pdo
Requires:  php-reflection
Requires:  php-spl
Requires:  php-sqlite3
Requires:  php-tokenizer

# PEAR
Provides:  php-pear(%{pear_channel}/HttpKernel) = %{version}
# Rename
Obsoletes: %{name}2-HttpKernel < %{version}
Provides:  %{name}2-HttpKernel = %{version}

%description httpkernel
The HttpKernel Component provides a structured process for converting a Request
into a Response by making use of the event dispatcher. It's flexible enough to
create a full-stack framework (Symfony), a micro-framework (Silex) or an
advanced CMS system (Drupal).

Configuration reference:
http://symfony.com/doc/current/reference/configuration/kernel.html

Optional: memcache, memcached, redis, Zend OPcache

# ------------------------------------------------------------------------------

%package   intl

Summary:   Symfony Intl Component
URL:       http://symfony.com/doc/current/components/intl.html
Group:     Development/Libraries

Requires:  %{name}-common =  %{version}-%{release}
Requires:  %{name}-icu    >= %{symfony_icu_min_ver}
Requires:  %{name}-icu    <  %{symfony_icu_max_ver}
# phpcompatinfo
Requires:  php-date
Requires:  php-intl
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-simplexml
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Intl) = %{version}
# Rename
Obsoletes: %{name}2-Intl < %{version}
Provides:  %{name}2-Intl = %{version}

%description intl
A PHP replacement layer for the C intl extension [1] that also provides access
to the localization data of the ICU library [2].

[1] http://www.php.net/manual/en/book.intl.php
[2] http://site.icu-project.org/

# ------------------------------------------------------------------------------

%package   locale

Summary:   Symfony Locale Component
Group:     Development/Libraries

Requires:  %{name}-intl   = %{version}-%{release}
# phpcompatinfo
Requires:  php-intl

# PEAR
Provides:  php-pear(%{pear_channel}/Locale) = %{version}
# Rename
Obsoletes: %{name}2-Locale < %{version}
Provides:  %{name}2-Locale = %{version}

%description locale
Locale provides fallback code to handle cases when the intl extension is
missing.

The Locale component is deprecated since version 2.3 and will be removed in
Symfony 3.0. You should use the more capable Intl component instead.

# ------------------------------------------------------------------------------

%package   optionsresolver

Summary:   Symfony OptionsResolver Component
URL:       http://symfony.com/doc/current/components/options_resolver.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-reflection
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/OptionsResolver) = %{version}
# Rename
Obsoletes: %{name}2-OptionsResolver < %{version}
Provides:  %{name}2-OptionsResolver = %{version}

%description optionsresolver
The OptionsResolver Component helps you configure objects with option arrays.
It supports default values, option constraints and lazy options.

# ------------------------------------------------------------------------------

%package   process

Summary:   Symfony Process Component
URL:       http://symfony.com/doc/current/components/process.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-pcntl
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Process) = %{version}
# Rename
Obsoletes: %{name}2-Process < %{version}
Provides:  %{name}2-Process = %{version}

%description process
The Process Component executes commands in sub-processes.

# ------------------------------------------------------------------------------

%package   propertyaccess

Summary:   Symfony PropertyAccess Component
URL:       http://symfony.com/doc/current/components/property_access/introduction.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/PropertyAccess) = %{version}
# Rename
Obsoletes: %{name}2-PropertyAccess < %{version}
Provides:  %{name}2-PropertyAccess = %{version}

%description propertyaccess
The PropertyAccess component provides function to read and write from/to an
object or array using a simple string notation.

# ------------------------------------------------------------------------------

%package   routing

Summary:   Symfony Routing Component
URL:       http://symfony.com/doc/current/components/routing/index.html
Group:     Development/Libraries

# Optional
Requires:  %{name}-config = %{version}-%{release}
Requires:  %{name}-yaml   = %{version}-%{release}
Requires:  php-pear(pear.doctrine-project.org/DoctrineCommon) >= %{doctrine_common_min_ver}
Requires:  php-pear(pear.doctrine-project.org/DoctrineCommon) <  %{doctrine_common_max_ver}
# phpcompatinfo
Requires:  php-dom
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-spl
Requires:  php-tokenizer

# PEAR
Provides:  php-pear(%{pear_channel}/Routing) = %{version}
# Rename
Obsoletes: %{name}2-Routing < %{version}
Provides:  %{name}2-Routing = %{version}

%description routing
The Routing Component maps an HTTP request to a set of configuration variables.

# ------------------------------------------------------------------------------

%package   security

Summary:   Symfony Security Component
URL:       http://symfony.com/doc/current/components/security/index.html
Group:     Development/Libraries

Requires:  %{name}-eventdispatcher =  %{version}-%{release}
Requires:  %{name}-httpfoundation  =  %{version}-%{release}
Requires:  %{name}-httpkernel      =  %{version}-%{release}
%if 0%{?rhel}
Requires:   php-password-compat    >= %{password_compat_min_ver}
Requires:   php-password-compat    <  %{password_compat_max_ver}
%endif
# Optional
Requires:  %{name}-classloader     =  %{version}-%{release}
Requires:  %{name}-finder          =  %{version}-%{release}
Requires:  %{name}-form            =  %{version}-%{release}
Requires:  %{name}-routing         =  %{version}-%{release}
Requires:  %{name}-validator       =  %{version}-%{release}
Requires:  php-pear(pear.doctrine-project.org/DoctrineDBAL) >= %{doctrine_dbal_min_ver}
Requires:  php-pear(pear.doctrine-project.org/DoctrineDBAL) <  %{doctrine_dbal_max_ver}
# phpcompatinfo
Requires:  php-date
Requires:  php-hash
Requires:  php-json
Requires:  php-openssl
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Security) = %{version}
# Rename
Obsoletes: %{name}2-Security < %{version}
Provides:  %{name}2-Security = %{version}

%description security
The Security Component provides a complete security system for your web
application. It ships with facilities for authenticating using HTTP basic
or digest authentication, interactive form login or X.509 certificate login,
but also allows you to implement your own authentication strategies.
Furthermore, the component provides ways to authorize authenticated users
based on their roles, and it contains an advanced ACL system.

# ------------------------------------------------------------------------------

%package   serializer

Summary:   Symfony Serializer Component
URL:       http://symfony.com/doc/current/components/serializer.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-dom
Requires:  php-json
Requires:  php-libxml
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-simplexml
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Serializer) = %{version}
# Rename
Obsoletes: %{name}2-Serializer < %{version}
Provides:  %{name}2-Serializer = %{version}

%description serializer
The Serializer Component is meant to be used to turn objects into a specific
format (XML, JSON, Yaml, ...) and the other way around.

# ------------------------------------------------------------------------------

%package  stopwatch

Summary:  Symfony Stopwatch Component
URL:      http://symfony.com/doc/current/components/stopwatch.html
Group:    Development/Libraries

Requires: %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires: php-spl

# PEAR
Provides: php-pear(%{pear_channel}/Stopwatch) = %{version}
# Rename
Obsoletes: %{name}2-Stopwatch < %{version}
Provides:  %{name}2-Stopwatch = %{version}

%description stopwatch
Stopwatch component provides a way to profile code.

# ------------------------------------------------------------------------------

%package   templating

Summary:   Symfony Templating Component
URL:       http://symfony.com/doc/current/components/templating.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-iconv
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Templating) = %{version}
# Rename
Obsoletes: %{name}2-Templating < %{version}
Provides:  %{name}2-Templating = %{version}

%description templating
Templating provides all the tools needed to build any kind of template system.

It provides an infrastructure to load template files and optionally monitor
them for changes. It also provides a concrete template engine implementation
using PHP with additional tools for escaping and separating templates into
blocks and layouts.

# ------------------------------------------------------------------------------

%package   translation

Summary:   Symfony Translation Component
Group:     Development/Libraries

# Optional
Requires:  %{name}-config = %{version}-%{release}
Requires:  %{name}-yaml   = %{version}-%{release}
# phpcompatinfo
Requires:  php-dom
Requires:  php-iconv
Requires:  php-intl
Requires:  php-libxml
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-simplexml
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Translation) = %{version}
# Rename
Obsoletes: %{name}2-Translation < %{version}
Provides:  %{name}2-Translation = %{version}

%description translation
Translation provides tools for loading translation files and generating
translated strings from these including support for pluralization.

# ------------------------------------------------------------------------------

%package   validator

Summary:   Symfony Validator Component
Group:     Development/Libraries

Requires:  %{name}-translation    = %{version}-%{release}
# Optional
Requires:  %{name}-config         = %{version}-%{release}
Requires:  %{name}-httpfoundation = %{version}-%{release}
Requires:  %{name}-intl           = %{version}-%{release}
Requires:  %{name}-yaml           = %{version}-%{release}
Requires:  php-pear(pear.doctrine-project.org/DoctrineCommon)
# phpcompatinfo
Requires:  php-ctype
Requires:  php-date
Requires:  php-filter
Requires:  php-intl
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-simplexml
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Validator) = %{version}
# Rename
Obsoletes: %{name}2-Validator < %{version}
Provides:  %{name}2-Validator = %{version}

%description validator
This component is based on the JSR-303 Bean Validation specification and
enables specifying validation rules for classes using XML, YAML, PHP or
annotations, which can then be checked against instances of these classes.

Optional: APC

# ------------------------------------------------------------------------------

%package   yaml

Summary:   Symfony Yaml Component
URL:       http://symfony.com/doc/current/components/yaml/index.html
Group:     Development/Libraries

Requires:  %{name}-common = %{version}-%{release}
# phpcompatinfo
Requires:  php-ctype
Requires:  php-date
Requires:  php-iconv
Requires:  php-json
Requires:  php-mbstring
Requires:  php-pcre
Requires:  php-spl

# PEAR
Provides:  php-pear(%{pear_channel}/Yaml) = %{version}
# Rename
Obsoletes: %{name}2-Yaml < %{version}
Provides:  %{name}2-Yaml = %{version}

%description yaml
The YAML Component loads and dumps YAML files.

# ##############################################################################


%prep
%setup -q -n %{github_name}-%{github_commit}

# Remove unnecessary files
find src -name '.git*' -delete
rm -rf src/Symfony/Bridge/{Propel1,ProxyManager}


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}%{symfony_dir}
cp -rp src/Symfony/* %{buildroot}%{symfony_dir}/

# Symlink main package docs to common sub-package docs
mkdir -p %{buildroot}%{_docdir}
%if 0%{?fedora} >= 20
ln -s %{name}-common %{buildroot}%{_docdir}/%{name}
%else
ln -s %{name}-common-%{version} %{buildroot}%{_docdir}/%{name}-%{version}
%endif


%check
# Create tests' autoloader
mkdir vendor
( cat <<'AUTOLOADER'
<?php

require_once __DIR__.'/../src/Symfony/Component/ClassLoader/UniversalClassLoader.php';

use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$loader->registerNamespace('Symfony', __DIR__.'/../src');
$loader->useIncludePath(true);
$loader->register();

if (version_compare(PHP_VERSION, '5.4.0', '<')) {
    require __DIR__.'/../src/Symfony/Component/HttpFoundation/Resources/stubs/SessionHandlerInterface.php';
}

if (file_exists('%{_datadir}/php/password_compat/password.php')) {
    require '%{_datadir}/php/password_compat/password.php';
}

return $loader;
AUTOLOADER
) > vendor/autoload.php

# Create PHPUnit config w/ colors turned off
cat phpunit.xml.dist \
    | sed 's/colors="true"/colors="false"/' \
    > phpunit.xml

# Skip tests that rely on external resources
sed -i \
    's/function testNonSeekableStream/function SKIP_testNonSeekableStream/' \
    src/Symfony/Component/Finder/Tests/FinderTest.php

# Temporarily skip tests that are known to fail
%if 0%{?rhel}
sed -i \
    's/function testForm/function SKIP_testForm/' \
    src/Symfony/Component/DomCrawler/Tests/CrawlerTest.php
sed -i \
    -e 's/function testConstructorHandlesFormAttribute/function SKIP_testConstructorHandlesFormAttribute/' \
    -e 's/function testConstructorHandlesFormValues/function SKIP_testConstructorHandlesFormValues/' \
    src/Symfony/Component/DomCrawler/Tests/FormTest.php
rm -f src/Symfony/Component/HttpFoundation/Tests/Session/Storage/Handler/NativeFileSessionHandlerTest.php
%endif

# Run tests
for PKG in src/Symfony/*/*; do
    echo -e "\n>>>>>>>>>>>>>>>>>>>>>>> ${PKG}\n"
    %{_bindir}/phpunit \
        --include-path ./src \
        --exclude-group tty,benchmark \
        -d date.timezone="UTC" \
        $PKG
done


%files
%defattr(-,root,root,-)
%if 0%{?fedora} >= 20
%doc %{_docdir}/%{name}
%else
%doc %{_docdir}/%{name}-%{version}
%endif


# ##############################################################################

%files common
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json

%dir %{symfony_dir}
%dir %{symfony_dir}/Bridge
%dir %{symfony_dir}/Bundle
%dir %{symfony_dir}/Component

# ------------------------------------------------------------------------------

%files doctrinebridge
%defattr(-,root,root,-)
%doc src/Symfony/Bridge/Doctrine/LICENSE
%doc src/Symfony/Bridge/Doctrine/*.md
%doc src/Symfony/Bridge/Doctrine/composer.json

%{symfony_dir}/Bridge/Doctrine
%exclude %{symfony_dir}/Bridge/Doctrine/LICENSE
%exclude %{symfony_dir}/Bridge/Doctrine/*.md
%exclude %{symfony_dir}/Bridge/Doctrine/composer.json
%exclude %{symfony_dir}/Bridge/Doctrine/phpunit.*
%exclude %{symfony_dir}/Bridge/Doctrine/Tests

# ------------------------------------------------------------------------------

%files monologbridge
%defattr(-,root,root,-)
%doc src/Symfony/Bridge/Monolog/LICENSE
%doc src/Symfony/Bridge/Monolog/*.md
%doc src/Symfony/Bridge/Monolog/composer.json

%{symfony_dir}/Bridge/Monolog
%exclude %{symfony_dir}/Bridge/Monolog/LICENSE
%exclude %{symfony_dir}/Bridge/Monolog/*.md
%exclude %{symfony_dir}/Bridge/Monolog/composer.json
%exclude %{symfony_dir}/Bridge/Monolog/phpunit.*
%exclude %{symfony_dir}/Bridge/Monolog/Tests

# ------------------------------------------------------------------------------

#%%files propel1bridge
#%defattr(-,root,root,-)
#%%doc src/Symfony/Bridge/Propel1/LICENSE
#%%doc src/Symfony/Bridge/Propel1/*.md
#%%doc src/Symfony/Bridge/Propel1/composer.json

# %%{symfony_dir}/Bridge/Propel1
#%%exclude %%{symfony_dir}/Bridge/Propel1/LICENSE
#%%exclude %%{symfony_dir}/Bridge/Propel1/*.md
#%%exclude %%{symfony_dir}/Bridge/Propel1/composer.json
#%%exclude %%{symfony_dir}/Bridge/Propel1/phpunit.*
#%%exclude %%{symfony_dir}/Bridge/Propel1/Tests

# ------------------------------------------------------------------------------

#%%files proxymanagerbridge

#%%doc src/Symfony/Bridge/ProxyManager/LICENSE
#%%doc src/Symfony/Bridge/ProxyManager/*.md
#%%doc src/Symfony/Bridge/ProxyManager/composer.json

# %%{symfony_dir}/Bridge/ProxyManager
#%%exclude %%{symfony_dir}/Bridge/ProxyManager/LICENSE
#%%exclude %%{symfony_dir}/Bridge/ProxyManager/*.md
#%%exclude %%{symfony_dir}/Bridge/ProxyManager/composer.json
#%%exclude %%{symfony_dir}/Bridge/ProxyManager/phpunit.*
#%%exclude %%{symfony_dir}/Bridge/ProxyManager/Tests

# ------------------------------------------------------------------------------

%files swiftmailerbridge
%defattr(-,root,root,-)
%doc src/Symfony/Bridge/Swiftmailer/LICENSE
%doc src/Symfony/Bridge/Swiftmailer/*.md
%doc src/Symfony/Bridge/Swiftmailer/composer.json

%{symfony_dir}/Bridge/Swiftmailer
%exclude %{symfony_dir}/Bridge/Swiftmailer/LICENSE
%exclude %{symfony_dir}/Bridge/Swiftmailer/*.md
%exclude %{symfony_dir}/Bridge/Swiftmailer/composer.json
#%%exclude %%{symfony_dir}/Bridge/Swiftmailer/phpunit.*
#%%exclude %%{symfony_dir}/Bridge/Swiftmailer/Tests

# ------------------------------------------------------------------------------

%files twigbridge
%defattr(-,root,root,-)
%doc src/Symfony/Bridge/Twig/LICENSE
%doc src/Symfony/Bridge/Twig/*.md
%doc src/Symfony/Bridge/Twig/composer.json

%{symfony_dir}/Bridge/Twig
%exclude %{symfony_dir}/Bridge/Twig/LICENSE
%exclude %{symfony_dir}/Bridge/Twig/*.md
%exclude %{symfony_dir}/Bridge/Twig/composer.json
%exclude %{symfony_dir}/Bridge/Twig/phpunit.*
%exclude %{symfony_dir}/Bridge/Twig/Tests

# ------------------------------------------------------------------------------

%files frameworkbundle
%defattr(-,root,root,-)
%doc src/Symfony/Bundle/FrameworkBundle/*.md
%doc src/Symfony/Bundle/FrameworkBundle/composer.json
%doc src/Symfony/Bundle/FrameworkBundle/Resources/meta/LICENSE

%{symfony_dir}/Bundle/FrameworkBundle
%exclude %{symfony_dir}/Bundle/FrameworkBundle/*.md
%exclude %{symfony_dir}/Bundle/FrameworkBundle/composer.json
%exclude %{symfony_dir}/Bundle/FrameworkBundle/phpunit.*
%exclude %{symfony_dir}/Bundle/FrameworkBundle/Tests
%exclude %{symfony_dir}/Bundle/FrameworkBundle/Resources/meta/LICENSE

# ------------------------------------------------------------------------------

%files securitybundle
%defattr(-,root,root,-)
%doc src/Symfony/Bundle/SecurityBundle/*.md
%doc src/Symfony/Bundle/SecurityBundle/composer.json
%doc src/Symfony/Bundle/SecurityBundle/Resources/meta/LICENSE

%{symfony_dir}/Bundle/SecurityBundle
%exclude %{symfony_dir}/Bundle/SecurityBundle/*.md
%exclude %{symfony_dir}/Bundle/SecurityBundle/composer.json
%exclude %{symfony_dir}/Bundle/SecurityBundle/phpunit.*
%exclude %{symfony_dir}/Bundle/SecurityBundle/Tests
%exclude %{symfony_dir}/Bundle/SecurityBundle/Resources/meta/LICENSE

# ------------------------------------------------------------------------------

%files twigbundle
%defattr(-,root,root,-)
%doc src/Symfony/Bundle/TwigBundle/*.md
%doc src/Symfony/Bundle/TwigBundle/composer.json
%doc src/Symfony/Bundle/TwigBundle/Resources/meta/LICENSE

%{symfony_dir}/Bundle/TwigBundle
%exclude %{symfony_dir}/Bundle/TwigBundle/*.md
%exclude %{symfony_dir}/Bundle/TwigBundle/composer.json
%exclude %{symfony_dir}/Bundle/TwigBundle/phpunit.*
%exclude %{symfony_dir}/Bundle/TwigBundle/Tests
%exclude %{symfony_dir}/Bundle/TwigBundle/Resources/meta/LICENSE

# ------------------------------------------------------------------------------

%files webprofilerbundle
%defattr(-,root,root,-)
%doc src/Symfony/Bundle/WebProfilerBundle/*.md
%doc src/Symfony/Bundle/WebProfilerBundle/composer.json
%doc src/Symfony/Bundle/WebProfilerBundle/Resources/ICONS_LICENSE.txt
%doc src/Symfony/Bundle/WebProfilerBundle/Resources/meta/LICENSE

%{symfony_dir}/Bundle/WebProfilerBundle
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/*.md
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/composer.json
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/phpunit.*
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/Tests
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/Resources/ICONS_LICENSE.txt
%exclude %{symfony_dir}/Bundle/WebProfilerBundle/Resources/meta/LICENSE

# ------------------------------------------------------------------------------

%files browserkit
%defattr(-,root,root,-)
%doc src/Symfony/Component/BrowserKit/LICENSE
%doc src/Symfony/Component/BrowserKit/*.md
%doc src/Symfony/Component/BrowserKit/composer.json

%{symfony_dir}/Component/BrowserKit
%exclude %{symfony_dir}/Component/BrowserKit/LICENSE
%exclude %{symfony_dir}/Component/BrowserKit/*.md
%exclude %{symfony_dir}/Component/BrowserKit/composer.json
%exclude %{symfony_dir}/Component/BrowserKit/phpunit.*
%exclude %{symfony_dir}/Component/BrowserKit/Tests

# ------------------------------------------------------------------------------

%files classloader
%defattr(-,root,root,-)
%doc src/Symfony/Component/ClassLoader/LICENSE
%doc src/Symfony/Component/ClassLoader/*.md
%doc src/Symfony/Component/ClassLoader/composer.json

%{symfony_dir}/Component/ClassLoader
%exclude %{symfony_dir}/Component/ClassLoader/LICENSE
%exclude %{symfony_dir}/Component/ClassLoader/*.md
%exclude %{symfony_dir}/Component/ClassLoader/composer.json
%exclude %{symfony_dir}/Component/ClassLoader/phpunit.*
%exclude %{symfony_dir}/Component/ClassLoader/Tests

# ------------------------------------------------------------------------------

%files config
%defattr(-,root,root,-)
%doc src/Symfony/Component/Config/LICENSE
%doc src/Symfony/Component/Config/*.md
%doc src/Symfony/Component/Config/composer.json

%{symfony_dir}/Component/Config
%exclude %{symfony_dir}/Component/Config/LICENSE
%exclude %{symfony_dir}/Component/Config/*.md
%exclude %{symfony_dir}/Component/Config/composer.json
%exclude %{symfony_dir}/Component/Config/phpunit.*
%exclude %{symfony_dir}/Component/Config/Tests

# ------------------------------------------------------------------------------

%files console
%defattr(-,root,root,-)
%doc src/Symfony/Component/Console/LICENSE
%doc src/Symfony/Component/Console/*.md
%doc src/Symfony/Component/Console/composer.json

%{symfony_dir}/Component/Console
%exclude %{symfony_dir}/Component/Console/LICENSE
%exclude %{symfony_dir}/Component/Console/*.md
%exclude %{symfony_dir}/Component/Console/composer.json
%exclude %{symfony_dir}/Component/Console/phpunit.*
%exclude %{symfony_dir}/Component/Console/Tests

# ------------------------------------------------------------------------------

%files cssselector
%defattr(-,root,root,-)
%doc src/Symfony/Component/CssSelector/LICENSE
%doc src/Symfony/Component/CssSelector/*.md
%doc src/Symfony/Component/CssSelector/composer.json

%{symfony_dir}/Component/CssSelector
%exclude %{symfony_dir}/Component/CssSelector/LICENSE
%exclude %{symfony_dir}/Component/CssSelector/*.md
%exclude %{symfony_dir}/Component/CssSelector/composer.json
%exclude %{symfony_dir}/Component/CssSelector/phpunit.*
%exclude %{symfony_dir}/Component/CssSelector/Tests

# ------------------------------------------------------------------------------

%files debug
%defattr(-,root,root,-)
%doc src/Symfony/Component/Debug/LICENSE
%doc src/Symfony/Component/Debug/*.md
%doc src/Symfony/Component/Debug/composer.json

%{symfony_dir}/Component/Debug
%exclude %{symfony_dir}/Component/Debug/LICENSE
%exclude %{symfony_dir}/Component/Debug/*.md
%exclude %{symfony_dir}/Component/Debug/composer.json
%exclude %{symfony_dir}/Component/Debug/phpunit.*
%exclude %{symfony_dir}/Component/Debug/Tests

# ------------------------------------------------------------------------------

%files dependencyinjection
%defattr(-,root,root,-)
%doc src/Symfony/Component/DependencyInjection/LICENSE
%doc src/Symfony/Component/DependencyInjection/*.md
%doc src/Symfony/Component/DependencyInjection/composer.json

%{symfony_dir}/Component/DependencyInjection
%exclude %{symfony_dir}/Component/DependencyInjection/LICENSE
%exclude %{symfony_dir}/Component/DependencyInjection/*.md
%exclude %{symfony_dir}/Component/DependencyInjection/composer.json
%exclude %{symfony_dir}/Component/DependencyInjection/phpunit.*
%exclude %{symfony_dir}/Component/DependencyInjection/Tests

# ------------------------------------------------------------------------------

%files domcrawler
%defattr(-,root,root,-)
%doc src/Symfony/Component/DomCrawler/LICENSE
%doc src/Symfony/Component/DomCrawler/*.md
%doc src/Symfony/Component/DomCrawler/composer.json

%{symfony_dir}/Component/DomCrawler
%exclude %{symfony_dir}/Component/DomCrawler/LICENSE
%exclude %{symfony_dir}/Component/DomCrawler/*.md
%exclude %{symfony_dir}/Component/DomCrawler/composer.json
%exclude %{symfony_dir}/Component/DomCrawler/phpunit.*
%exclude %{symfony_dir}/Component/DomCrawler/Tests

# ------------------------------------------------------------------------------

%files eventdispatcher
%defattr(-,root,root,-)
%doc src/Symfony/Component/EventDispatcher/LICENSE
%doc src/Symfony/Component/EventDispatcher/*.md
%doc src/Symfony/Component/EventDispatcher/composer.json

%{symfony_dir}/Component/EventDispatcher
%exclude %{symfony_dir}/Component/EventDispatcher/LICENSE
%exclude %{symfony_dir}/Component/EventDispatcher/*.md
%exclude %{symfony_dir}/Component/EventDispatcher/composer.json
%exclude %{symfony_dir}/Component/EventDispatcher/phpunit.*
%exclude %{symfony_dir}/Component/EventDispatcher/Tests

# ------------------------------------------------------------------------------

%files filesystem
%defattr(-,root,root,-)
%doc src/Symfony/Component/Filesystem/LICENSE
%doc src/Symfony/Component/Filesystem/*.md
%doc src/Symfony/Component/Filesystem/composer.json

%{symfony_dir}/Component/Filesystem
%exclude %{symfony_dir}/Component/Filesystem/LICENSE
%exclude %{symfony_dir}/Component/Filesystem/*.md
%exclude %{symfony_dir}/Component/Filesystem/composer.json
%exclude %{symfony_dir}/Component/Filesystem/phpunit.*
%exclude %{symfony_dir}/Component/Filesystem/Tests

# ------------------------------------------------------------------------------

%files finder
%defattr(-,root,root,-)
%doc src/Symfony/Component/Finder/LICENSE
%doc src/Symfony/Component/Finder/*.md
%doc src/Symfony/Component/Finder/composer.json

%{symfony_dir}/Component/Finder
%exclude %{symfony_dir}/Component/Finder/LICENSE
%exclude %{symfony_dir}/Component/Finder/*.md
%exclude %{symfony_dir}/Component/Finder/composer.json
%exclude %{symfony_dir}/Component/Finder/phpunit.*
%exclude %{symfony_dir}/Component/Finder/Tests

# ------------------------------------------------------------------------------

%files form
%defattr(-,root,root,-)
%doc src/Symfony/Component/Form/LICENSE
%doc src/Symfony/Component/Form/*.md
%doc src/Symfony/Component/Form/composer.json

%{symfony_dir}/Component/Form
%exclude %{symfony_dir}/Component/Form/LICENSE
%exclude %{symfony_dir}/Component/Form/*.md
%exclude %{symfony_dir}/Component/Form/composer.json
%exclude %{symfony_dir}/Component/Form/phpunit.*
%exclude %{symfony_dir}/Component/Form/Tests

# ------------------------------------------------------------------------------

%files httpfoundation
%defattr(-,root,root,-)
%doc src/Symfony/Component/HttpFoundation/LICENSE
%doc src/Symfony/Component/HttpFoundation/*.md
%doc src/Symfony/Component/HttpFoundation/composer.json

%{symfony_dir}/Component/HttpFoundation
%exclude %{symfony_dir}/Component/HttpFoundation/LICENSE
%exclude %{symfony_dir}/Component/HttpFoundation/*.md
%exclude %{symfony_dir}/Component/HttpFoundation/composer.json
%exclude %{symfony_dir}/Component/HttpFoundation/phpunit.*
%exclude %{symfony_dir}/Component/HttpFoundation/Tests

# ------------------------------------------------------------------------------

%files httpkernel
%defattr(-,root,root,-)
%doc src/Symfony/Component/HttpKernel/LICENSE
%doc src/Symfony/Component/HttpKernel/*.md
%doc src/Symfony/Component/HttpKernel/composer.json

%{symfony_dir}/Component/HttpKernel
%exclude %{symfony_dir}/Component/HttpKernel/LICENSE
%exclude %{symfony_dir}/Component/HttpKernel/*.md
%exclude %{symfony_dir}/Component/HttpKernel/composer.json
%exclude %{symfony_dir}/Component/HttpKernel/phpunit.*
%exclude %{symfony_dir}/Component/HttpKernel/Tests

# ------------------------------------------------------------------------------

%files intl
%defattr(-,root,root,-)
%doc src/Symfony/Component/Intl/LICENSE
%doc src/Symfony/Component/Intl/*.md
%doc src/Symfony/Component/Intl/composer.json

%{symfony_dir}/Component/Intl
%exclude %{symfony_dir}/Component/Intl/LICENSE
%exclude %{symfony_dir}/Component/Intl/*.md
%exclude %{symfony_dir}/Component/Intl/composer.json
%exclude %{symfony_dir}/Component/Intl/phpunit.*
%exclude %{symfony_dir}/Component/Intl/Tests

# ------------------------------------------------------------------------------

%files locale
%defattr(-,root,root,-)
%doc src/Symfony/Component/Locale/LICENSE
%doc src/Symfony/Component/Locale/*.md
%doc src/Symfony/Component/Locale/composer.json

%{symfony_dir}/Component/Locale
%exclude %{symfony_dir}/Component/Locale/LICENSE
%exclude %{symfony_dir}/Component/Locale/*.md
%exclude %{symfony_dir}/Component/Locale/composer.json
%exclude %{symfony_dir}/Component/Locale/phpunit.*
%exclude %{symfony_dir}/Component/Locale/Tests

# ------------------------------------------------------------------------------

%files optionsresolver
%defattr(-,root,root,-)
%doc src/Symfony/Component/OptionsResolver/LICENSE
%doc src/Symfony/Component/OptionsResolver/*.md
%doc src/Symfony/Component/OptionsResolver/composer.json

%{symfony_dir}/Component/OptionsResolver
%exclude %{symfony_dir}/Component/OptionsResolver/LICENSE
%exclude %{symfony_dir}/Component/OptionsResolver/*.md
%exclude %{symfony_dir}/Component/OptionsResolver/composer.json
%exclude %{symfony_dir}/Component/OptionsResolver/phpunit.*
%exclude %{symfony_dir}/Component/OptionsResolver/Tests

# ------------------------------------------------------------------------------

%files process
%defattr(-,root,root,-)
%doc src/Symfony/Component/Process/LICENSE
%doc src/Symfony/Component/Process/*.md
%doc src/Symfony/Component/Process/composer.json

%{symfony_dir}/Component/Process
%exclude %{symfony_dir}/Component/Process/LICENSE
%exclude %{symfony_dir}/Component/Process/*.md
%exclude %{symfony_dir}/Component/Process/composer.json
%exclude %{symfony_dir}/Component/Process/phpunit.*
%exclude %{symfony_dir}/Component/Process/Tests

# ------------------------------------------------------------------------------

%files propertyaccess
%defattr(-,root,root,-)
%doc src/Symfony/Component/PropertyAccess/LICENSE
%doc src/Symfony/Component/PropertyAccess/*.md
%doc src/Symfony/Component/PropertyAccess/composer.json

%{symfony_dir}/Component/PropertyAccess
%exclude %{symfony_dir}/Component/PropertyAccess/LICENSE
%exclude %{symfony_dir}/Component/PropertyAccess/*.md
%exclude %{symfony_dir}/Component/PropertyAccess/composer.json
#%%exclude %%{symfony_dir}/Component/PropertyAccess/phpunit.*
#%%exclude %%{symfony_dir}/Component/PropertyAccess/Tests

# ------------------------------------------------------------------------------

%files routing
%defattr(-,root,root,-)
%doc src/Symfony/Component/Routing/LICENSE
%doc src/Symfony/Component/Routing/*.md
%doc src/Symfony/Component/Routing/composer.json

%{symfony_dir}/Component/Routing
%exclude %{symfony_dir}/Component/Routing/LICENSE
%exclude %{symfony_dir}/Component/Routing/*.md
%exclude %{symfony_dir}/Component/Routing/composer.json
%exclude %{symfony_dir}/Component/Routing/phpunit.*
%exclude %{symfony_dir}/Component/Routing/Tests

# ------------------------------------------------------------------------------

%files security
%defattr(-,root,root,-)
%doc src/Symfony/Component/Security/LICENSE
%doc src/Symfony/Component/Security/*.md
%doc src/Symfony/Component/Security/composer.json

%{symfony_dir}/Component/Security
%exclude %{symfony_dir}/Component/Security/LICENSE
%exclude %{symfony_dir}/Component/Security/*.md
%exclude %{symfony_dir}/Component/Security/composer.json
%exclude %{symfony_dir}/Component/Security/phpunit.*
%exclude %{symfony_dir}/Component/Security/Tests

# ------------------------------------------------------------------------------

%files serializer
%defattr(-,root,root,-)
%doc src/Symfony/Component/Serializer/LICENSE
%doc src/Symfony/Component/Serializer/*.md
%doc src/Symfony/Component/Serializer/composer.json

%{symfony_dir}/Component/Serializer
%exclude %{symfony_dir}/Component/Serializer/LICENSE
%exclude %{symfony_dir}/Component/Serializer/*.md
%exclude %{symfony_dir}/Component/Serializer/composer.json
%exclude %{symfony_dir}/Component/Serializer/phpunit.*
%exclude %{symfony_dir}/Component/Serializer/Tests

# ------------------------------------------------------------------------------

%files stopwatch
%defattr(-,root,root,-)
%doc src/Symfony/Component/Stopwatch/LICENSE
%doc src/Symfony/Component/Stopwatch/*.md
%doc src/Symfony/Component/Stopwatch/composer.json

%{symfony_dir}/Component/Stopwatch
%exclude %{symfony_dir}/Component/Stopwatch/LICENSE
%exclude %{symfony_dir}/Component/Stopwatch/*.md
%exclude %{symfony_dir}/Component/Stopwatch/composer.json
#%%exclude %%{symfony_dir}/Component/Stopwatch/phpunit.*
#%%exclude %%{symfony_dir}/Component/Stopwatch/Tests

# ------------------------------------------------------------------------------

%files templating
%defattr(-,root,root,-)
%doc src/Symfony/Component/Templating/LICENSE
%doc src/Symfony/Component/Templating/*.md
%doc src/Symfony/Component/Templating/composer.json

%{symfony_dir}/Component/Templating
%exclude %{symfony_dir}/Component/Templating/LICENSE
%exclude %{symfony_dir}/Component/Templating/*.md
%exclude %{symfony_dir}/Component/Templating/composer.json
%exclude %{symfony_dir}/Component/Templating/phpunit.*
%exclude %{symfony_dir}/Component/Templating/Tests

# ------------------------------------------------------------------------------

%files translation
%defattr(-,root,root,-)
%doc src/Symfony/Component/Translation/LICENSE
%doc src/Symfony/Component/Translation/*.md
%doc src/Symfony/Component/Translation/composer.json

%{symfony_dir}/Component/Translation
%exclude %{symfony_dir}/Component/Translation/LICENSE
%exclude %{symfony_dir}/Component/Translation/*.md
%exclude %{symfony_dir}/Component/Translation/composer.json
%exclude %{symfony_dir}/Component/Translation/phpunit.*
%exclude %{symfony_dir}/Component/Translation/Tests

# ------------------------------------------------------------------------------

%files validator
%defattr(-,root,root,-)
%doc src/Symfony/Component/Validator/LICENSE
%doc src/Symfony/Component/Validator/*.md
%doc src/Symfony/Component/Validator/composer.json

%{symfony_dir}/Component/Validator
%exclude %{symfony_dir}/Component/Validator/LICENSE
%exclude %{symfony_dir}/Component/Validator/*.md
%exclude %{symfony_dir}/Component/Validator/composer.json
%exclude %{symfony_dir}/Component/Validator/phpunit.*
%exclude %{symfony_dir}/Component/Validator/Tests

# ------------------------------------------------------------------------------

%files yaml
%defattr(-,root,root,-)
%doc src/Symfony/Component/Yaml/LICENSE
%doc src/Symfony/Component/Yaml/*.md
%doc src/Symfony/Component/Yaml/composer.json

%{symfony_dir}/Component/Yaml
%exclude %{symfony_dir}/Component/Yaml/LICENSE
%exclude %{symfony_dir}/Component/Yaml/*.md
%exclude %{symfony_dir}/Component/Yaml/composer.json
%exclude %{symfony_dir}/Component/Yaml/phpunit.*
%exclude %{symfony_dir}/Component/Yaml/Tests

# ##############################################################################

%changelog
* Wed Nov 27 2013 Remi Collet <remi@fedoraproject.org> 2.3.7-3
- sync with rawhide, build for remi repo

* Tue Nov 26 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.7-3
- Fixed several summaries and descriptions ("Symfony2" => "Symfony")

* Sat Nov 23 2013 Remi Collet <remi@fedoraproject.org> 2.3.7-2
- backport stuff for remi repo

* Fri Nov 22 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.7-2
- Renamed from "php-symfony2" to "php-symfony"
- Updated main pkg summary
- Removed dependency on common sub-pkg for sub-pkgs that require other sub-pkgs
- Common sub-pkg obsoletes php-channel-symfony2
- Fixed swiftmailerbridge sub-pkg dependency
- Updated %%check to use PHPUnit's "--include-path" option

* Sun Nov 17 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.7-1
- Updated to 2.3.7
- Separated icu pkg
- Added php-password-compat requires for el6 (PHP < 5.5.0)
- common sub-pkg now owns %%{symfony_dir}/{Bridge,Bundle,Component}
- Fixed classloader URL

* Wed Nov 06 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.6-2
- Updated tests' autoloader
- Individual pkg tests instead of one
- Skip specific tests
- Exclude tty and benchmark test groups
- Fix main package doc symlink

* Mon Oct 21 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.6-1
- Updated to 2.3.6
- Renamed sub-packages to lowercase

* Sat Jul 13 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.1-1
- Initial package
