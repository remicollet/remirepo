%global php_name ZendFramework
#define posttag .PL1

Summary:         Leading open-source PHP framework
Name:            php-ZendFramework
Version:         1.10.5
Release:         1%{?posttag}%{?dist}

License:         BSD
Group:           Development/Libraries
Source0:         http://framework.zend.com/releases/%{php_name}-%{version}%{?posttag}/%{php_name}-%{version}%{?posttag}.tar.gz
Source1:         README.fedora
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL:             http://framework.zend.com/

BuildArch:       noarch

Requires: php >= 5.2.4
Requires: php-bcmath
Requires: php-ctype
Requires: php-curl
Requires: php-dom
Requires: php-hash
Requires: php-iconv
Requires: php-json
Requires: php-pcre
Requires: php-posix
Requires: php-reflection
Requires: php-session
Requires: php-simplexml
Requires: php-spl
Requires: php-zlib
Requires: php-pdo
Requires: php-xml
# missing for Http_Client
# Requires: php-mime_magic

# Needed after the removal of the tests subpackage
Provides:  %{name}-tests = %{version}-%{release}
Obsoletes: %{name}-tests < 1.9.6-2

%description
Extending the art & spirit of PHP, Zend Framework is based on simplicity,
object-oriented best practices, corporate friendly licensing, and a rigorously
tested agile codebase. Zend Framework is focused on building more secure,
reliable, and modern Web 2.0 applications & web services, and consuming widely
available APIs from leading vendors like Google, Amazon, Yahoo!, Flickr, as
well as API providers and catalogers like StrikeIron and ProgrammableWeb.


%package demos
Summary:  Demos for the Zend Framework
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description demos
This package includes Zend Framework demos for the Feeds, Gdata, Mail, OpenId,
Pdf, Search-Lucene and Services subpackages.


%package extras
Summary:  Zend Framework Extras (ZendX)
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: %{name}-ZendX = %{version}-%{release}

%description extras
This package includes the ZendX libraries.


%package Auth-Adapter-Ldap
Summary:  Zend Framework LDAP Authentication Adapter
Group:    Development/Libraries
Requires: %{name}-Ldap = %{version}-%{release}

%description Auth-Adapter-Ldap
This package contains the authentication adapter needed to operate against LDAP
directories.


%package Cache-Backend-Apc
Summary:  Zend Framework APC cache backend
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-apc

%description Cache-Backend-Apc
This package contains the backend for Zend_Cache to store and retrieve data via
APC.


%package Cache-Backend-Memcached
Summary:  Zend Framework memcache cache backend
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-pecl-memcache

%description Cache-Backend-Memcached
This package contains the back end for Zend_Cache to store and retrieve data
via memcache.


%package Cache-Backend-Sqlite
Summary:  Zend Framework sqlite back end
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-sqlite

%description Cache-Backend-Sqlite
This package contains the back end for Zend_Cache to store and retrieve data
via sqlite databases.


%package Captcha
Summary:  Zend Framework CAPTCHA component
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-gd

%description Captcha
This package contains the Zend Framework CAPTCHA extension.


%package Dojo
Summary:  Zend Framework Dojo Toolkit integration component
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description Dojo
This package contains the Zend Framework Dojo Toolkit component as well as a
copy of Dojo itself.


%package Db-Adapter-Mysqli
Summary:  Zend Framework database adapter for mysqli
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-mysqli

%description Db-Adapter-Mysqli
This package contains the files for Zend Framework necessary to connect to a
MySQL server via mysqli connector.


# %package Db-Adapter-Db2
# Summary:  Zend Framework database adapter for DB2
# Group:    Development/Libraries
# Requires: %{name} = %{version}-%{release}
# Requires: php-ibm_db2 # Not available in Fedora's PHP

# %description Db-Adapter-Db2
# This package contains the files for Zend Framework necessary to connect to an
# IBM DB2 database.


%package Db-Adapter-Firebird
Summary:  Zend Framework database adapter for InterBase
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-interbase

%description Db-Adapter-Firebird
This package contains the files for Zend Framework necessary to connect to a
Firebird/InterBase database.


%package Db-Adapter-Oracle
Summary:  Zend Framework database adapter for Oracle
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-oci8

%description Db-Adapter-Oracle
This package contains the files for Zend Framework necessary to connect to an
Oracle database.


%package Feed
Summary:  Live syndication feeds helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-mbstring

%description Feed
This component provides a very simple way to work with live syndicated feeds.

* consumes RSS and Atom feeds
* provides utilities for discovering feed links
* imports feeds from multiple sources
* providers feed building and posting operations


%package Gdata
Summary:  Google Data APIs
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description Gdata
The Google Data APIs provide read/write access to such services hosted at
google.com as Spreadsheets, Calendar, Blogger, and CodeSearch.

* supports both authentication mechanisms of Google Data servers
* supports queries and posting changes against Google Data services
* supports service-specific element types in an object-oriented interface
* matches functionality and design of other Google Data API clients


%package Ldap
Summary:  Basic LDAP operations API
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-ldap

%description Ldap
Zend_Ldap is a class for performing LDAP operations including but not limited
to binding, searching and modifying entries in an LDAP directory.


%package Pdf
Summary:  PDF file handling helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-gd

%description Pdf
Portable Document Format (PDF) from Adobe is the de facto standard for
cross-platform rich documents. Now, PHP applications can create or read PDF
documents on the fly, without the need to call utilities from the shell, depend
on PHP extensions, or pay licensing fees. Zend_Pdf can even modify existing PDF
documents.

* supports Adobe PDF file format
* parses PDF structure and provides access to elements
* creates or modifies PDF documents
* utilizes memory efficiently


%package Search-Lucene
Summary:  Apache Lucene engine PHP port
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
# php-pecl-bitset is not available but this is an optional requirement
# Requires: php-bitset

%description Search-Lucene
The Apache Lucene engine is a powerful, feature-rich Java search engine that is
flexible about document storage and supports many complex query
types. Zend_Search_Lucene is a port of this engine written entirely in PHP 5.

* allows PHP-powered websites to leverage powerful search capabilities without
  the need for web services or Java
* provides binary compatibility with Apache Lucene
* matches Apache Lucene in performance


%package Services
Summary:  Web service APIs for a number of providers
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-mcrypt
Requires: php-soap

%description Services
This package contains web service client APIs for the following services:

- Akismet
- Amazon (including Ec2, S3)
- Audioscrobbler
- del.icio.us
- Flickr
- Nirvanix
- ReCaptcha
- Simpy
- SlideShare
- StrikeIron
- Technorati
- Twitter
- Yahoo!


%package Soap
Summary:  SOAP web services server part helper
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: php-soap

%description Soap
Zend_Soap_Server class is intended to simplify Web Services server part
development for PHP programmers.

It may be used in WSDL or non-WSDL mode, and using classes or functions to
define Web Service API.

When Zend_Soap_Server component works in the WSDL mode, it uses already
prepared WSDL document to define server object behavior and transport layer
options.

WSDL document may be auto-generated with functionality provided by
Zend_Soap_AutoDiscovery component or should be constructed manually using
Zend_Soap_Wsdl class or any other XML generating tool.

If the non-WSDL mode is used, then all protocol options have to be set using
options mechanism.


%prep
%setup -qn %{php_name}-%{version}%{?posttag}
cp %{SOURCE1} .


%build
%if 0%{?rhel} == 4
find . -type f  \
  -fprint executables -exec %{__chmod} -x '{}' \; >/dev/null
%else
find . -type f -perm /111 \
  -fprint executables -exec %{__chmod} -x '{}' \; >/dev/null
%endif

find . -type f -name \*.sh \
  -fprint valid_executables -exec %{__chmod} +x '{}' \; >/dev/null

%{__cat} executables valid_executables|sort|uniq -u > invalid_executables


%install
%{__rm} -rf $RPM_BUILD_ROOT

%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/php
%{__cp} -pr library/Zend $RPM_BUILD_ROOT%{_datadir}/php
%{__cp} -pr demos/Zend $RPM_BUILD_ROOT%{_datadir}/php/Zend/demos
%{__cp} -pr externals $RPM_BUILD_ROOT%{_datadir}/php/Zend

# ZendX
cd extras
%{__cp} -pr library/ZendX $RPM_BUILD_ROOT%{_datadir}/php
cd ..

%{__cp} -pr bin/zf.{php,sh} \
  $RPM_BUILD_ROOT%{_datadir}/php/Zend
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__ln_s} %{_datadir}/php/Zend/zf.sh \
  $RPM_BUILD_ROOT%{_bindir}/zf


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc LICENSE.txt INSTALL.txt README.txt README.fedora
%{_bindir}/zf
# we list all files explicitly to find out what's new in future releases more
# easily
%dir %{_datadir}/php/Zend
%{_datadir}/php/Zend/zf.php
%{_datadir}/php/Zend/zf.sh
%{_datadir}/php/Zend/Acl
%{_datadir}/php/Zend/Acl.php
%{_datadir}/php/Zend/Amf
%{_datadir}/php/Zend/Application
%{_datadir}/php/Zend/Application.php
%{_datadir}/php/Zend/Auth
%exclude %{_datadir}/php/Zend/Auth/Adapter/Ldap.php
%{_datadir}/php/Zend/Auth.php
%{_datadir}/php/Zend/Barcode
%{_datadir}/php/Zend/Barcode.php
%{_datadir}/php/Zend/Cache
%exclude %{_datadir}/php/Zend/Cache/Backend/Apc.php
%exclude %{_datadir}/php/Zend/Cache/Backend/Memcached.php
%exclude %{_datadir}/php/Zend/Cache/Backend/Sqlite.php
%{_datadir}/php/Zend/Cache.php
%{_datadir}/php/Zend/CodeGenerator
%{_datadir}/php/Zend/Config
%{_datadir}/php/Zend/Config.php
%{_datadir}/php/Zend/Console
%{_datadir}/php/Zend/Controller
%{_datadir}/php/Zend/Crypt
%{_datadir}/php/Zend/Crypt.php
%{_datadir}/php/Zend/Currency
%{_datadir}/php/Zend/Currency.php
%{_datadir}/php/Zend/Date
%{_datadir}/php/Zend/Date.php
%{_datadir}/php/Zend/Db
%exclude %{_datadir}/php/Zend/Db/Adapter/Db2.php
%exclude %{_datadir}/php/Zend/Db/Adapter/Db2
%exclude %{_datadir}/php/Zend/Db/Statement/Db2.php
%exclude %{_datadir}/php/Zend/Db/Statement/Db2
%exclude %{_datadir}/php/Zend/Db/Adapter/Mysqli.php
%exclude %{_datadir}/php/Zend/Db/Adapter/Mysqli
%exclude %{_datadir}/php/Zend/Db/Statement/Mysqli.php
%exclude %{_datadir}/php/Zend/Db/Statement/Mysqli
%exclude %{_datadir}/php/Zend/Db/Adapter/Oracle.php
%exclude %{_datadir}/php/Zend/Db/Adapter/Oracle
%exclude %{_datadir}/php/Zend/Db/Statement/Oracle.php
%exclude %{_datadir}/php/Zend/Db/Statement/Oracle
%{_datadir}/php/Zend/Db.php
%{_datadir}/php/Zend/Debug.php
%{_datadir}/php/Zend/Dom
%{_datadir}/php/Zend/Exception.php
%{_datadir}/php/Zend/File
%{_datadir}/php/Zend/Filter
%{_datadir}/php/Zend/Filter.php
%{_datadir}/php/Zend/Form
%{_datadir}/php/Zend/Form.php
%{_datadir}/php/Zend/Http
%{_datadir}/php/Zend/InfoCard
%{_datadir}/php/Zend/InfoCard.php
%{_datadir}/php/Zend/Json
%{_datadir}/php/Zend/Json.php
%{_datadir}/php/Zend/Layout
%{_datadir}/php/Zend/Layout.php
%{_datadir}/php/Zend/Loader
%{_datadir}/php/Zend/Loader.php
%{_datadir}/php/Zend/Locale
%{_datadir}/php/Zend/Locale.php
%{_datadir}/php/Zend/Log
%{_datadir}/php/Zend/Log.php
%{_datadir}/php/Zend/Mail
%{_datadir}/php/Zend/Mail.php
%{_datadir}/php/Zend/Markup
%{_datadir}/php/Zend/Markup.php
%{_datadir}/php/Zend/Measure
%{_datadir}/php/Zend/Memory
%{_datadir}/php/Zend/Memory.php
%{_datadir}/php/Zend/Mime
%{_datadir}/php/Zend/Mime.php
%{_datadir}/php/Zend/Navigation
%{_datadir}/php/Zend/Navigation.php
%{_datadir}/php/Zend/Oauth
%{_datadir}/php/Zend/Oauth.php
%{_datadir}/php/Zend/OpenId
%{_datadir}/php/Zend/OpenId.php
%{_datadir}/php/Zend/Queue.php
%{_datadir}/php/Zend/Queue
%{_datadir}/php/Zend/Paginator
%{_datadir}/php/Zend/Paginator.php
%{_datadir}/php/Zend/ProgressBar
%{_datadir}/php/Zend/ProgressBar.php
%{_datadir}/php/Zend/Reflection
%{_datadir}/php/Zend/Registry.php
%{_datadir}/php/Zend/Rest
%{_datadir}/php/Zend/Server
%{_datadir}/php/Zend/Service
%exclude %{_datadir}/php/Zend/Service/Akismet.php
%exclude %{_datadir}/php/Zend/Service/Amazon.php
%exclude %{_datadir}/php/Zend/Service/Amazon
%exclude %{_datadir}/php/Zend/Service/Audioscrobbler.php
%exclude %{_datadir}/php/Zend/Service/Delicious.php
%exclude %{_datadir}/php/Zend/Service/Delicious
%exclude %{_datadir}/php/Zend/Service/Flickr.php
%exclude %{_datadir}/php/Zend/Service/Flickr
%exclude %{_datadir}/php/Zend/Service/Nirvanix.php
%exclude %{_datadir}/php/Zend/Service/Nirvanix
%exclude %{_datadir}/php/Zend/Service/ReCaptcha.php
%exclude %{_datadir}/php/Zend/Service/ReCaptcha
%exclude %{_datadir}/php/Zend/Service/Simpy.php
%exclude %{_datadir}/php/Zend/Service/Simpy
%exclude %{_datadir}/php/Zend/Service/SlideShare.php
%exclude %{_datadir}/php/Zend/Service/SlideShare
%exclude %{_datadir}/php/Zend/Service/StrikeIron.php
%exclude %{_datadir}/php/Zend/Service/StrikeIron
%exclude %{_datadir}/php/Zend/Service/Technorati.php
%exclude %{_datadir}/php/Zend/Service/Technorati
%exclude %{_datadir}/php/Zend/Service/Yahoo.php
%exclude %{_datadir}/php/Zend/Service/Yahoo
%{_datadir}/php/Zend/Serializer
%{_datadir}/php/Zend/Serializer.php
%{_datadir}/php/Zend/Session
%{_datadir}/php/Zend/Session.php
%{_datadir}/php/Zend/Tag
%{_datadir}/php/Zend/Test
%{_datadir}/php/Zend/Text
%{_datadir}/php/Zend/TimeSync
%{_datadir}/php/Zend/TimeSync.php
%{_datadir}/php/Zend/Tool
%{_datadir}/php/Zend/Translate
%{_datadir}/php/Zend/Translate.php
%{_datadir}/php/Zend/Uri
%{_datadir}/php/Zend/Uri.php
%{_datadir}/php/Zend/Validate
%{_datadir}/php/Zend/Validate.php
%{_datadir}/php/Zend/Version.php
%{_datadir}/php/Zend/View
%{_datadir}/php/Zend/View.php
%{_datadir}/php/Zend/Wildfire
%{_datadir}/php/Zend/XmlRpc
%{_datadir}/php/Zend/externals
%exclude %{_datadir}/php/Zend/externals/dojo

%files demos
%defattr(-,root,root,-)
%{_datadir}/php/Zend/demos
%doc LICENSE.txt

%files extras
%defattr(-,root,root,-)
%{_datadir}/php/ZendX
%exclude %{_datadir}/php/ZendX/Db
%doc LICENSE.txt

%files Auth-Adapter-Ldap
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Auth/Adapter/Ldap.php
%doc LICENSE.txt

%files Cache-Backend-Apc
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Cache/Backend/Apc.php
%doc LICENSE.txt

%files Cache-Backend-Memcached
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Cache/Backend/Memcached.php
%doc LICENSE.txt

%files Cache-Backend-Sqlite
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Cache/Backend/Sqlite.php
%doc LICENSE.txt

%files Captcha
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Captcha
%doc LICENSE.txt

%files Db-Adapter-Mysqli
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Db/Adapter/Mysqli.php
%{_datadir}/php/Zend/Db/Adapter/Mysqli
%{_datadir}/php/Zend/Db/Statement/Mysqli.php
%{_datadir}/php/Zend/Db/Statement/Mysqli
%doc LICENSE.txt

# php-ibm_db2 not available for Fedora
# %files Db-Adapter-Db2
# %defattr(-,root,root,-)
# %{_datadir}/php/Zend/Db/Adapter/Db2.php
# %{_datadir}/php/Zend/Db/Adapter/Db2
# %{_datadir}/php/Zend/Db/Statement/Db2.php
# %{_datadir}/php/Zend/Db/Statement/Db2
# %doc LICENSE.txt

%files Db-Adapter-Firebird
%defattr(-,root,root,-)
%{_datadir}/php/ZendX/Db/Adapter/Firebird.php
%{_datadir}/php/ZendX/Db/Adapter/Firebird
%{_datadir}/php/ZendX/Db/Statement/Firebird.php
%{_datadir}/php/ZendX/Db/Statement/Firebird
%doc LICENSE.txt

%files Db-Adapter-Oracle
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Db/Adapter/Oracle.php
%{_datadir}/php/Zend/Db/Adapter/Oracle
%{_datadir}/php/Zend/Db/Statement/Oracle.php
%{_datadir}/php/Zend/Db/Statement/Oracle
%doc LICENSE.txt

%files Dojo
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Dojo.php
%{_datadir}/php/Zend/Dojo
%{_datadir}/php/Zend/externals/dojo
%doc LICENSE.txt

%files Feed
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Feed.php
%{_datadir}/php/Zend/Feed
%doc LICENSE.txt

%files Gdata
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Gdata.php
%{_datadir}/php/Zend/Gdata
%doc LICENSE.txt

%files Ldap
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Ldap.php
%{_datadir}/php/Zend/Ldap
%doc LICENSE.txt

%files Pdf
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Pdf.php
%{_datadir}/php/Zend/Pdf
%doc LICENSE.txt

%files Search-Lucene
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Search
%doc LICENSE.txt

%files Services
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Service/Akismet.php
%{_datadir}/php/Zend/Service/Amazon.php
%{_datadir}/php/Zend/Service/Amazon
%{_datadir}/php/Zend/Service/Audioscrobbler.php
%{_datadir}/php/Zend/Service/Delicious.php
%{_datadir}/php/Zend/Service/Delicious
%{_datadir}/php/Zend/Service/Flickr.php
%{_datadir}/php/Zend/Service/Flickr
%{_datadir}/php/Zend/Service/Nirvanix.php
%{_datadir}/php/Zend/Service/Nirvanix
%{_datadir}/php/Zend/Service/ReCaptcha.php
%{_datadir}/php/Zend/Service/ReCaptcha
%{_datadir}/php/Zend/Service/Simpy.php
%{_datadir}/php/Zend/Service/Simpy
%{_datadir}/php/Zend/Service/SlideShare.php
%{_datadir}/php/Zend/Service/SlideShare
%{_datadir}/php/Zend/Service/StrikeIron.php
%{_datadir}/php/Zend/Service/StrikeIron
%{_datadir}/php/Zend/Service/Technorati.php
%{_datadir}/php/Zend/Service/Technorati
%{_datadir}/php/Zend/Service/Yahoo.php
%{_datadir}/php/Zend/Service/Yahoo
%doc LICENSE.txt

%files Soap
%defattr(-,root,root,-)
%{_datadir}/php/Zend/Soap
%doc LICENSE.txt


%changelog
* Sun Jun 13 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.10.5-1
- rebuild for remi repository

* Sat Jun 12 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.5-1
- update to 1.10.5 which contains over 60 bugfixes

* Fri May 13 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.10.4-1
- rebuild for remi repository

* Thu May 13 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.4-1
- about 180 bugfixes since 1.10.2 (http://framework.zend.com/changelog/1.10.4)
- fixes ZF2010-07: Potential Security Issues in Bundled Dojo Library

* Thu Mar  5 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.10.2-1
- rebuild for remi repository

* Wed Mar 03 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10.2-1
- 1.10.2
- over 50 bugfixes since 1.10.1 (which in turn had over 50 bugfixes)

* Sat Feb 06 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.10-1
- rebuild for remi repository

* Sun Jan 31 2010 Felix Kaechele <heffer@fedoraproject.org> - 1.10-1
- 1.10
- new components: Barcode, Oauth, Markup, Serializer

* Sat Jan 16 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.9.7-1
- rebuild for remi repository

* Thu Jan 14 2010 Alexander Kahl <akahl@imttechnologies.com> - 1.9.7-1
- update to bugfix / security release 1.9.7 

* Fri Dec 18 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.9.6-2
- rebuild for remi repository

* Tue Dec 08 2009 Felix Kaechele <felix@fetzig.org> - 1.9.6-2
- insert correct provides/obsoletes for tests subpackage removal

* Mon Nov 30 2009 Felix Kaechele <heffer@fedoraproject.org> - 1.9.6-1
- update to 1.9.6

* Thu Nov 19 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.9.5-1
- rebuild for remi repository

* Sun Nov 15 2009 Felix Kaechele <felix@fetzig.org> - 1.9.5-1
- update to 1.9.5
- removed test subpackage as it can never comply to font packaging guidelines

* Sat Nov 14 2009 Remi Collet <Fedora@FamilleCollet.com> - 1.9.3-1.PL1
- rebuild for remi repository
- enable Oracle and Sqlite sub package

* Wed Sep 30 2009 Felix Kaechele <heffer@fedoraproject.org> - 1.9.3-1.PL1
- new upstream version
- new component: Queue
- fixed dangling symlinks
- enabled Db-Adapter-Firebird

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-3.PL1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 20 2009 Alexander Kahl <akahl@iconmobile.com> - 1.8.4-2.PL1
- removed Fileinfo dependency
- don't make zf.sh symlink absolute (breaks the script)

* Thu Jul 16 2009 Alexander Kahl <akahl@iconmobile.com> - 1.8.4-1.PL1
- update to 1.8.4 patch 1 (it's about time!)
- Requires php 5.1.4 -> 5.2.4
- list all files explicitly for easier future updates
- incubator no more (Zend_Tool stable now)
- Request now part of Controller
- new components: Application, CodeGenerator, Crypt, Navigation, Reflection,
  Tag
- Soap and Services require php-soap now

* Tue Mar 17 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.7-2
- bump to catch up with with f10

* Tue Mar 17 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.7-1
- update to 1.7.7
- PHPUnit dep now >= 3.3.0
- moved Ldap bindings to extra packages (php-ldap dep)
- excluded db adapters with unresolvable deps
- moved mysqli db adapter files to correct package
- support both old and new font deps using conditional

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 16 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.7.2-5
- Fix font [Build]Requires yet again to track moving target of naming
  convention.  Fixes broken deps.

* Mon Jan 12 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.7.2-4
- Fix Requires, BuildRequires: bitstream-vera-fonts-{sans,sans-mono,serif}
  fixes broken deps

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-3
- +BuildRequires: bitstream-vera-fonts
- -Requires: bitstream-vera-fonts

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-2
- Bug 477440: Use Vera fonts from Fedora's package

* Fri Jan  2 2009 Alexander Kahl <akahl@iconmobile.com> - 1.7.2-1
- update to 1.7.2
- ZendX documentation doesn't need regeneration anymore, removed deps

* Wed Nov 19 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-3
- fix to use internal docbook

* Wed Nov 19 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-2
- bump for rawhide (Zend_Tool activated)

* Tue Nov 18 2008 Alexander Kahl <akahl@iconmobile.com> - 1.7.0-1
- update to 1.7.0

* Wed Nov 12 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.2-2
- last tag failed, bump

* Wed Nov 12 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.2-1
- update to 1.6.2

* Tue Sep 16 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.1-1
- update to 1.6.1

* Sat Sep 13 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-1
- update to 1.6.0 stable (full version)
- create list of invalid executables in %%build for upstream
- new components Captcha, Dojo, Service-ReCaptcha, Wildfire, Zend_Tool
- BuildRequire symlinks to sanitize zf -> zf.sh symlink

* Sat Aug  2 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-0.2.rc1
- added license file to all packages to silence rpmline

* Tue Jul 29 2008 Alexander Kahl <akahl@iconmobile.com> - 1.6.0-0.1.rc1
- update to 1.6.0RC1
- added php-Fileinfo dependency

* Wed Jun 11 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.2-1
- update to 1.5.2
- new package split
- removed Cache-Backend-Sqlite, Db-Adapter-Db2, Db-Adapter-Firebird,
  Db-Adapter-Oracle
- removed optional php-bitset requirement from Search-Lucene, not available
- removed virtual requires and provides, not necessary anymore

* Mon Mar 17 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1
- updated for 1.5.0 stable

* Mon Mar 17 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1.rc3
- new upstream version rc3
- updated for 1.5.0 stable
- new subpackages Ldap and Service-Nirvanix

* Fri Mar  7 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-2.rc1
- added missing dependencies

* Thu Mar  6 2008 Alexander Kahl <akahl@iconmobile.com> - 1.5.0-1.rc1
- new release candidate version 1.5.0
- package all zend components in subpackages

* Wed Dec 12 2007 Alexander Kahl <akahl@iconmobile.com> - 1.0.3-1
- new stable version 1.0.3
- preserve timestamps upon copying
- split up documentation into subpackages
- description BE->AE

* Thu Oct 30 2007 Alexander Kahl <akahl@iconmobile.com> - 1.0.2-1
- initial release
