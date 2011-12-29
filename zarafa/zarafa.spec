%global beta_or_rc      0
%global actual_release  1
%global svnrevision     30515
%global with_clucene    1
%global with_ldap       1
%global with_xmlto      1
%global no_multiupload  1
%global php_apiver      %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")

# Private libraries are not be exposed globally by RPM
%if 0%{?rhel}%{?fedora} > 4
%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}/.*\.so$
%filter_setup
}
%endif

Summary:            Open Source Edition of the Zarafa Collaboration Platform
Name:               zarafa
Version:            7.0.3
%if %{beta_or_rc}
Release:            0.%{actual_release}.svn%{svnrevision}%{?dist}
%else
Release:            %{actual_release}%{?dist}
%endif
# Red Hat Legal has been advised by email from Zarafa that no license is
# required in order to use the letter string "zarafa" (combined with other
# words) in the package naming, to refer to the software as "Zarafa" to
# indicate its intended purpose, and to modify packages with bug fixes and
# enhancements.
License:            AGPLv3 with exceptions
Group:              Applications/Productivity
URL:                http://www.zarafa.com/
%if %{beta_or_rc}
Source0:            http://download.zarafa.com/community/beta/7.0/%{version}-%{svnrevision}/sourcecode/zcp-%{version}.tar.gz
%else
Source0:            http://download.zarafa.com/community/final/7.0/%{version}-%{svnrevision}/sourcecode/zcp-%{version}.tar.gz
%endif
Source1:            %{name}.ini
Source2:            %{name}.logrotate
Source3:            %{name}-webaccess.conf

Patch0:             zarafa-6.40.5-rpath.patch

BuildRequires:      bison
BuildRequires:      gcc-c++
BuildRequires:      byacc
BuildRequires:      flex
BuildRequires:      gettext
BuildRequires:      libical-devel >= 0.42
BuildRequires:      libvmime-devel >= 0.9.0
BuildRequires:      libxml2-devel
BuildRequires:      mysql-devel >= 4.1
BuildRequires:      ncurses-devel
BuildRequires:      pam-devel
BuildRequires:      php-devel >= 4.3
BuildRequires:      %{_includedir}/uuid/uuid.h
BuildRequires:      %{_includedir}/curl/curl.h
BuildRequires:      libicu-devel >= 3.4
%if 0%{?rhel}%{?fedora} > 5
BuildRequires:      boost-devel >= 1.35.0
%else
BuildRequires:      boost141-devel
%endif
BuildRequires:      swig
%if 0
BuildRequires:      %{_bindir}/xsubpp
%endif
%if 0%{?rhel}%{?fedora} > 4
BuildRequires:      python-devel >= 2.4
%endif

%if %{with_clucene}
%if 0%{?fedora} > 15
BuildRequires:      clucene09-core-devel >= 0.9.21b-1
%else
BuildRequires:      clucene-core-devel >= 0.9.21b-1
%endif
%endif

%if %{with_ldap}
BuildRequires:      openldap-devel
%endif

%if %{with_xmlto}
BuildRequires:      xmlto
%endif

# The main package pulls in all of classical zarafa core packages
Requires:           zarafa-dagent%{?_isa} = %{version}-%{release}
Requires:           zarafa-gateway%{?_isa} = %{version}-%{release}
Requires:           zarafa-ical%{?_isa} = %{version}-%{release}
Requires:           zarafa-monitor%{?_isa} = %{version}-%{release}
Requires:           zarafa-server%{?_isa} = %{version}-%{release}
Requires:           zarafa-spooler%{?_isa} = %{version}-%{release}
Requires:           zarafa-utils%{?_isa} = %{version}-%{release}

BuildRoot:          %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The Zarafa Collaboration Platform is a Microsoft Exchange replacement. The
Open Source Collaboration provides an integration with your existing Linux
mail server, native mobile phone support by ActiveSync compatibility and a
webaccess with 'Look & Feel' similar to Outlook using Ajax. Including an
IMAP and a POP3 gateway as well as an iCal/CalDAV gateway, the Zarafa Open
Source Collaboration can combine the usability with the stability and the
flexibility of a Linux server.

The proven Zarafa groupware solution is using MAPI objects, provides a MAPI
client library as well as programming interfaces for C++, PHP and Perl. The
other Zarafa related packages need to be installed to gain all the features
and benefits of the Zarafa Collaboration Platform (ZCP).

%package archiver
Summary:            Archive messages to a secondary Zarafa server
Group:              Applications/Archiving
Requires:           zarafa-common = %{version}-%{release}

%description archiver
The zarafa-archiver package includes the Zarafa Archiver to decrease the
size of a production Zarafa server by copying or moving the messages to
a secondary Zarafa server. Clients will still be able to open the message
from the secondary Zarafa server directly.

%package client
Summary:            The Zarafa Client library
Group:              System Environment/Libraries
Requires:           zarafa-common = %{version}-%{release}

%description client
The zarafa-client package provides the Zarafa Client library, which gets
used by the Open Source MAPI (Messaging Application Programming Interface)
implementation of Zarafa as provider between MAPI and Zarafa.

%package common
Summary:            Common Zarafa files and directories
Group:              Applications/Productivity
Requires(pre):      shadow-utils
%if 0%{?rhel}%{?fedora} > 5
BuildArch:          noarch
%endif

%description common
The zarafa-common package provides the filesystem structure and includes
common files required by most other Zarafa packages. It also provides the
creation of the zarafa user for the different Zarafa services.

%package dagent
Summary:            Mail Delivery Agent for Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires:           php-mapi%{?_isa} = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description dagent
The zarafa-dagent package includes the Zarafa Delivery Agent to deliver
e-mail messages from Internet Mail format to Zarafa. The Zarafa Delivery
Agent can be used trigger the local mailer (MDA) or even act as the LMTP
server.

%package devel
Summary:            Development files for several Zarafa libraries
Group:              Development/Libraries
Requires:           libmapi%{?_isa} = %{version}-%{release}, pkgconfig
Provides:           %{name}-static = %{version}-%{release}
Provides:           %{name}-static%{?_isa} = %{version}-%{release}

%description devel
The zarafa-devel package includes header files and libraries necessary for
developing own programs which use functions and interfaces from the Zarafa
Collaboration Platform. The Zarafa Open Source Collaboration is using MAPI
objects, provides a MAPI client library and a C++ programming interface.

%package gateway
Summary:            POP3/IMAP Gateway for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description gateway
The zarafa-gateway package includes the Zarafa POP3/IMAP Gateway service
to enable regular non-MAPI e-mail clients to connect through POP3 or IMAP
to the Zarafa server to access their e-mails. Using IMAP, it is possible
as well to view the contents of shared folders and subfolders. The Zarafa
POP3/IMAP Gateway service can be configured to listen for POP3, POP3S,
IMAP and/or IMAPS.

%package ical
Summary:            iCal/CalDAV gateway for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service
Provides:           zarafa-caldav = %{version}-%{release}
Provides:           zarafa-caldav%{?_isa} = %{version}-%{release}
Obsoletes:          zarafa-caldav < 6.40.5-1

%description ical
The zarafa-ical package includes the Zarafa iCal/CalDAV gateway service
to enable users to access their calendar using iCalendar (RFC 2445/5545)
or CalDAV (RFC 4791) compliant clients. The iCal/CalDAV gateway service
can be configured to listen for HTTP and HTTPS requests.

%if %{with_clucene}
%package indexer
Summary:            Indexer search engine for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}, file
Requires:           catdoc, libxslt, w3m, unzip, %{_bindir}/pdftotext
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description indexer
The zarafa-indexer package includes the Zarafa Indexing service for fast
and full-text searching. Using CLucene search engine, this service makes
an index per user of messages and attachments for the Zarafa server. At
search queries, the server will use this index to quickly find messages,
items and even in contents of attached documents.
%endif

%package monitor
Summary:            Quota Monitor for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description monitor
The zarafa-monitor package includes the Zarafa Monitoring service which
is responsible for checking the users store (mailbox) size, and sending
them (and administrators) a warning e-mail when limits are exceeded.

%package server
Summary:            Server component for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description server
The zarafa-server package includes the main Zarafa Server and Storage
process. It contacts a database server and provides services to Zarafa
clients. The user base can be either retrieved from an external source
or can be setup with a separate list of users.

%package spooler
Summary:            Mail Spooler for the Zarafa Collaboration Platform
Group:              System Environment/Daemons
Requires:           zarafa-common = %{version}-%{release}
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/service, /sbin/chkconfig
Requires(postun):   /sbin/service

%description spooler
The zarafa-spooler package includes the Zarafa Spooler service which is
responsible for converting the Zarafa e-mails from outboxes to Internet
Mail and send it using the configured SMTP server to the recipients.

%package utils
Summary:            Zarafa Utilities for administration and management
Group:              Applications/System
Requires:           zarafa-common = %{version}-%{release}

%description utils
The zarafa-utils package includes various administration and management
utilities for the Zarafa Open Source Collaboration environment including
reporting, user and password management.

%package webaccess
Summary:            Zarafa Webaccess featuring a 'Look & Feel' similar to Outlook
Group:              Applications/Productivity
Requires:           httpd, php-mapi = %{version}-%{release}
# Bug: php53 from RHEL 5 does not provide php (#717158)
%if 0%{?rhel} == 5
Requires:           mod_php >= 4.3
%else
Requires:           php >= 4.3
%endif
%if 0%{?rhel}%{?fedora} > 5
BuildArch:          noarch
%endif

%description webaccess
Zarafa Webaccess features the familiar Outlook 'Look & Feel' interface
and you can keep using the features in Outlook that have always allowed
you to work efficiently. View your e-mail, calendar and contacts via a
web browser. And opening your colleagues calendar or sending a meeting
request is only a piece of cake. The Zarafa Webaccess is using the ajax
technology to give a more interactive feeling to the users.

%package -n libmapi
Summary:            MAPI implementation and library by Zarafa
Group:              System Environment/Libraries
Requires:           zarafa-client%{?_isa} = %{version}-%{release}
Requires(post):     /sbin/ldconfig
Requires(postun):   /sbin/ldconfig
Obsoletes:          perl-MAPI < 6.40.5-1, perl-libmapi < 6.40.0-1

%description -n libmapi
The libmapi package provides the Open Source MAPI (Messaging Application
Programming Interface) implementation by Zarafa. The MAPI is a messaging
architecture and a Component Object Model based API for Microsoft Windows
which allows control over the messaging system on the client computer,
creation and management of messages, management of the client mailbox,
service providers, etc. This MAPI implementation by Zarafa is also known
as MAPI4Linux.

%if 0
%package -n perl-MAPI
Summary:            The Perl MAPI extension by Zarafa
Group:              Development/Libraries
Requires:           perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Provides:           perl-libmapi = %{version}-%{release}
Obsoletes:          perl-libmapi < 6.40.0-1

%description -n perl-MAPI
The perl-MAPI package contains the Perl MAPI extension to provide access
to Microsoft MAPI functions while using Perl.
%endif

%package -n php-mapi
Summary:            The PHP MAPI extension by Zarafa
Group:              Development/Languages
# Bug: Without mod_ssl, reloading httpd causes core dump
Requires:           mod_ssl
%if 0%{?rhel}%{?fedora} > 4
%if 0%{?php_zend_api:1}
Requires:           php(zend-abi) = %{php_zend_api}, php(api) = %{php_core_api}
%else
Requires:           php-api = %{php_apiver}
%endif
%else
Requires:           php >= 4.3
%endif

%description -n php-mapi
The php-mapi package contains the PHP MAPI extension to provide access to
Microsoft MAPI functions while using PHP. Although not all MAPI functions
and interfaces are supported so far, most functions have a PHP counterpart
in this extension. Using this PHP MAPI extension, developers can create
e.g. webbased e-mail and calendaring systems and interfaces with existing
PHP projects, using the MAPI functions like a normal MAPI program.

%if 0%{?rhel}%{?fedora} > 4
%package -n python-MAPI
Summary:            The Python MAPI extension by Zarafa
Group:              Development/Languages

%description -n python-MAPI
The python-MAPI package contains the Python MAPI extension to provide the
access to Microsoft MAPI functions while using Python. Using this Python
MAPI extension, developers can create Python programs which use MAPI calls
to interact with Zarafa.
%endif

%prep
%setup -q
%patch0 -p1 -b .rpath
touch -c -r aclocal.m4.rpath aclocal.m4

%build
%if 0%{?rhel}%{?fedora} < 6
export CPPFLAGS="$CPPFLAGS -I%{_includedir}/boost141"
export LDFLAGS="$LDFLAGS -L%{_libdir}/boost141"
%endif

%if 0%{?fedora} > 15
export LDFLAGS="$LDFLAGS -L%{_libdir}/clucene09"
%endif

%configure \
    --with-userscript-prefix=%{_sysconfdir}/%{name}/userscripts \
    --with-quotatemplate-prefix=%{_sysconfdir}/%{name}/quotamail \
    --with-indexerscripts-prefix=%{_datadir}/%{name}/indexerscripts \
%if %{with_clucene}
%if 0%{?fedora} > 15
    --with-clucene-lib-prefix=%{_libdir}/clucene09 \
    --with-clucene-include-prefix=%{_includedir}/clucene09 \
%else
    --with-clucene-lib-prefix=%{_libdir} \
    --with-clucene-include-prefix=%{_includedir} \
%endif
%else
    --with-clucene-lib-prefix= \
%endif
    --enable-release \
    --enable-swig \
    --disable-perl \
%if 0%{?rhel}%{?fedora} > 4
    --enable-python \
%else
    --disable-python \
%endif
    --disable-static \
    --disable-testtools
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make \
%if 0%{?rhel}%{?fedora} < 6
    docdir=%{_datadir}/doc/%{name}/ \
    datarootdir=%{_datadir} \
%endif
    DESTDIR=$RPM_BUILD_ROOT \
    INSTALL='install -p' \
    install \
    install-ajax-webaccess

# Nuke all overlefts from licensed, managed or other proprietary items
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{license,licensed.cfg,report-ca}
rm -f $RPM_BUILD_ROOT%{_mandir}/man?/{zarafa-{backup,restore,report,msr,ldapms.cfg,licensed{,.cfg}},za-aclsync}.*

# Move all the initscripts to their appropriate place and
# ensure that all services are off by default at boot time
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/init.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/
for service in dagent gateway ical indexer monitor server spooler; do
    if [ -f installer/linux/%{name}-$service.init.rhel ]; then
        sed -e 's@345@-@' installer/linux/%{name}-$service.init.rhel > \
            $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}-$service
        chmod 755 $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}-$service
        touch -c -r installer/linux/%{name}-$service.init.rhel $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}-$service
    fi
done

# Move the configuration files to their correct place and handle
# /usr/lib vs. /usr/lib64 for all architectures correct and set
# run_as_user, run_as_group and local_admin_users values correct
for config in $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/example-config/*.cfg; do
    config=$(basename $config)
    if [ -f $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/example-config/$config ]; then
        sed -e 's@\(run_as_\(user\|group\)[[:space:]]*=\).*@\1 %{name}@' -e 's@/usr/lib/zarafa@%{_libdir}/%{name}@' \
            -e 's@\(local_admin_users[[:space:]]*=[[:space:]]*root.*\)@\1 %{name}@' \
                $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/example-config/$config > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
        chmod 640 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
        touch -c -r $RPM_BUILD_ROOT%{_datadir}/doc/%{name}/example-config/$config $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$config
    fi
done

# Move the logrotate configuration file to its correct place
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/%{name}

# Move the userscripts to their correct place and symlink them
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/userscripts/
for userscript in companies_common.sh groups_common.sh users_common.sh \
            createcompany creategroup createuser deletecompany deletegroup deleteuser; do
    mv -f $RPM_BUILD_ROOT{%{_sysconfdir},%{_datadir}}/%{name}/userscripts/$userscript
    ln -sf ../../..%{_datadir}/%{name}/userscripts/$userscript $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/userscripts/$userscript
done

# Create the data directory and install some files into
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -p -m 644 installer/linux/db-{calc-storesize,convert-attachments-to-files} $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -p -m 644 installer/linux/{ssl-certificates.sh,audit-parse.pl,zarafa7-upgrade} $RPM_BUILD_ROOT%{_datadir}/%{name}/
%if %{with_ldap}
install -p -m 644 installer/linux/{db-upgrade-objectsid-to-objectguid,ldap-switch-sendas}.pl $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -p -m 644 installer/ldap/%{name}.schema $RPM_BUILD_ROOT%{_datadir}/%{name}/
%else
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/ldap.{active-directory,openldap,propmap}.cfg
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/%{name}-ldap.cfg.5*
%endif

# Install the script to optimize IMAP headers for new gateway
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-gateway/
install -p -m 644 tools/python-scripts/optimize-imap.py $RPM_BUILD_ROOT%{_datadir}/%{name}-gateway/

# Create the default log and lib directory for packaging
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/{log,lib}/%{name}/

# Remove all libtool .la files to avoid packaging of them
rm -f $RPM_BUILD_ROOT{%{_libdir}/{,php/modules,php4,%{name}},%{perl_vendorarch}/auto/MAPI,%{python_sitearch}}/*.la

# Remove files that are anyway in %doc or %{_datadir}/%{name}/
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/%{name}{,-gateway}/

# Move Indexer/CLucene related files to its correct places
%if %{with_clucene}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/indexerscripts/
mv -f $RPM_BUILD_ROOT{%{_datadir},%{_sysconfdir}}/%{name}/indexerscripts/attachments_parser.db
for helper in attachments_parser xmltotext.xslt zmktemp; do
    ln -s ../../..%{_datadir}/%{name}/indexerscripts/$helper $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/indexerscripts/$helper
done
%else
rm -f $RPM_BUILD_ROOT{%{_sysconfdir}/{rc.d/init.d,sysconfig},%{_mandir}/man?}/%{name}-indexer*
rm -rf $RPM_BUILD_ROOT{%{_sysconfdir}/%{name}/indexer.cfg,%{_datadir}/%{name}/indexerscripts/}
%endif

# Move the webaccess configuration file to its correct place
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/webaccess{-ajax,}
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/config.php
ln -sf ../../..%{_sysconfdir}/%{name}/webaccess/config.php $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/config.php

# Install the apache configuration file for webaccess
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}-webaccess.conf

# Move the webaccess plugins directory to its correct place
rm -rf $RPM_BUILD_ROOT{%{_datadir},%{_localstatedir}/lib}/%{name}-webaccess/plugins
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/plugins/

# Remove unwanted language connectors and webaccess files
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/client/widgets/fckeditor/editor/dialog/fck_spellerpages/spellerpages/server-scripts/spellchecker.{cfm,pl}
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/{.htaccess,%{name}-webaccess.conf}

# Remove flash-based multi-attachment upload (missing source)
%if %{no_multiupload}
sed '122,129d' $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/webaccess/config.php > \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/webaccess/config.php.new
touch -c -r $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/webaccess/config.php{,.new}
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/webaccess/config.php{.new,}
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}-webaccess/client/widgets/swfupload/
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre common
getent group %{name} > /dev/null || %{_sbindir}/groupadd -r %{name}
getent passwd %{name} > /dev/null || %{_sbindir}/useradd -r -g %{name} -d %{_localstatedir}/lib/%{name} -s /sbin/nologin -c "Zarafa Service Account" %{name}
exit 0

%post archiver
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/archiver.* > /dev/null 2>&1 || :

%post dagent
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-dagent
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/dagent.* > /dev/null 2>&1 || :

%post gateway
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-gateway
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/gateway.* > /dev/null 2>&1 || :

%post ical
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-ical
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/ical.* > /dev/null 2>&1 || :

%if %{with_clucene}
%post indexer
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-indexer
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/indexer.* > /dev/null 2>&1 || :
%endif

%post monitor
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-monitor
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/monitor.* > /dev/null 2>&1 || :

%post server
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-server
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/server.* > /dev/null 2>&1 || :
chown %{name}:%{name} %{_localstatedir}/log/%{name}/audit.* > /dev/null 2>&1 || :

%post spooler
[ $1 -eq 1 ] && /sbin/chkconfig --add %{name}-spooler
# Ensure correct log file ownership after upgrade from official packages
chown %{name}:%{name} %{_localstatedir}/log/%{name}/spooler.* > /dev/null 2>&1 || :

%post -n libmapi -p /sbin/ldconfig

%preun dagent
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-dagent stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-dagent
fi

%preun gateway
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-gateway stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-gateway
fi

%preun ical
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-ical stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-ical
fi

%if %{with_clucene}
%preun indexer
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-indexer stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-indexer
fi
%endif

%preun monitor
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-monitor stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-monitor
fi

%preun server
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-server stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-server
fi

%preun spooler
if [ $1 -eq 0 ]; then
    /sbin/service %{name}-spooler stop > /dev/null 2>&1 || :
    /sbin/chkconfig --del %{name}-spooler
fi

%postun dagent
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-dagent condrestart > /dev/null 2>&1 || :
fi

%postun gateway
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-gateway condrestart > /dev/null 2>&1 || :
fi

%postun ical
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-ical condrestart > /dev/null 2>&1 || :
fi

%if %{with_clucene}
%postun indexer
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-indexer condrestart > /dev/null 2>&1 || :
fi
%endif

%postun monitor
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-monitor condrestart > /dev/null 2>&1 || :
fi

%postun server
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-server condrestart > /dev/null 2>&1 || :
fi

%postun spooler
if [ $1 -ne 0 ]; then
    /sbin/service %{name}-spooler condrestart > /dev/null 2>&1 || :
fi

%postun -n libmapi -p /sbin/ldconfig

%files
%defattr(-,root,root,-)

%files archiver
%defattr(-,root,root,-)
%{_bindir}/%{name}-archiver
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/archiver.cfg
%{_mandir}/man1/%{name}-archiver.1*
%{_mandir}/man5/%{name}-archiver.cfg.5*

%files client -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/libzarafaclient.so

%files common
%defattr(-,root,root,-)
%doc installer/licenseagreement/AGPL-3
%dir %{_sysconfdir}/%{name}/
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_mandir}/man1/%{name}.1*
%dir %{_datadir}/%{name}/
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}/
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/log/%{name}/

%files dagent
%defattr(-,root,root,-)
%doc installer/linux/createuser.dotforward
%{_bindir}/%{name}-autorespond
%{_bindir}/%{name}-dagent
%{_bindir}/%{name}-mr-accept
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/dagent.cfg
%config(noreplace) %{_sysconfdir}/%{name}/autorespond
%{_sysconfdir}/rc.d/init.d/%{name}-dagent
%{_mandir}/man1/%{name}-dagent.1*
%{_mandir}/man5/%{name}-dagent.cfg.5*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libarchiver.so
%{_libdir}/libicalmapi.so
%{_libdir}/libinetmapi.so
%{_libdir}/libmapi.so
%{_libdir}/libcommon_mapi.a
%{_libdir}/libcommon_ssl.a
%{_libdir}/libcommon_util.a
%{_libdir}/libfreebusy.a
%{_libdir}/libzarafasync.a
%{_includedir}/icalmapi/
%{_includedir}/inetmapi/
%{_includedir}/mapi4linux/
%{_includedir}/libfreebusy/
%{_includedir}/libzarafasync/
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/%{name}.pc

%files gateway
%defattr(-,root,root,-)
%{_bindir}/%{name}-gateway
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/gateway.cfg
%{_sysconfdir}/rc.d/init.d/%{name}-gateway
%{_datadir}/%{name}-gateway/
%{_mandir}/man1/%{name}-gateway.1*
%{_mandir}/man5/%{name}-gateway.cfg.5*

%files ical
%defattr(-,root,root,-)
%{_bindir}/%{name}-ical
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/ical.cfg
%{_sysconfdir}/rc.d/init.d/%{name}-ical
%{_mandir}/man1/%{name}-ical.1*
%{_mandir}/man5/%{name}-ical.cfg.5*

%if %{with_clucene}
%files indexer
%defattr(-,root,root,-)
%{_bindir}/%{name}-indexer
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/indexer.cfg
%{_sysconfdir}/rc.d/init.d/%{name}-indexer
%dir %{_sysconfdir}/%{name}/indexerscripts/
%config(noreplace) %{_sysconfdir}/%{name}/indexerscripts/attachments_parser.db
%{_sysconfdir}/%{name}/indexerscripts/attachments_parser
%{_sysconfdir}/%{name}/indexerscripts/xmltotext.xslt
%{_sysconfdir}/%{name}/indexerscripts/zmktemp
%dir %{_datadir}/%{name}/indexerscripts/
%{_datadir}/%{name}/indexerscripts/attachments_parser
%{_datadir}/%{name}/indexerscripts/xmltotext.xslt
%{_datadir}/%{name}/indexerscripts/zmktemp
%{_mandir}/man1/%{name}-indexer.1*
%{_mandir}/man5/%{name}-indexer.cfg.5*
%endif

%files monitor
%defattr(-,root,root,-)
%{_bindir}/%{name}-monitor
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/monitor.cfg
%dir %{_sysconfdir}/%{name}/quotamail/
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/companyhard.mail
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/companysoft.mail
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/companywarning.mail
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/userhard.mail
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/usersoft.mail
%config(noreplace) %{_sysconfdir}/%{name}/quotamail/userwarning.mail
%{_sysconfdir}/rc.d/init.d/%{name}-monitor
%{_mandir}/man1/%{name}-monitor.1*
%{_mandir}/man5/%{name}-monitor.cfg.5*

%files server
%defattr(-,root,root,-)
%{_bindir}/%{name}-server
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/server.cfg
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/unix.cfg
%{_sysconfdir}/rc.d/init.d/%{name}-server
%dir %{_sysconfdir}/%{name}/userscripts/
%{_sysconfdir}/%{name}/userscripts/createuser
%{_sysconfdir}/%{name}/userscripts/creategroup
%{_sysconfdir}/%{name}/userscripts/createcompany
%{_sysconfdir}/%{name}/userscripts/deleteuser
%{_sysconfdir}/%{name}/userscripts/deletegroup
%{_sysconfdir}/%{name}/userscripts/deletecompany
%{_sysconfdir}/%{name}/userscripts/*common.sh
%dir %{_sysconfdir}/%{name}/userscripts/createuser.d/
%dir %{_sysconfdir}/%{name}/userscripts/creategroup.d/
%dir %{_sysconfdir}/%{name}/userscripts/createcompany.d/
%dir %{_sysconfdir}/%{name}/userscripts/deleteuser.d/
%dir %{_sysconfdir}/%{name}/userscripts/deletegroup.d/
%dir %{_sysconfdir}/%{name}/userscripts/deletecompany.d/
%config(noreplace) %{_sysconfdir}/%{name}/userscripts/createcompany.d/00createpublic
%config(noreplace) %{_sysconfdir}/%{name}/userscripts/createuser.d/00createstore
%{_datadir}/%{name}/userscripts/
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/dbplugin.so
%{_libdir}/%{name}/unixplugin.so
%{_mandir}/man1/%{name}-server.1*
%{_mandir}/man5/%{name}-server.cfg.5*
%{_mandir}/man5/%{name}-unix.cfg.5*
%if %{with_ldap}
%{_datadir}/%{name}/%{name}.schema
%{_datadir}/%{name}/db-upgrade-objectsid-to-objectguid.pl
%{_datadir}/%{name}/ldap-switch-sendas.pl
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/ldap.active-directory.cfg
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/ldap.openldap.cfg
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/ldap.propmap.cfg
%{_libdir}/%{name}/ldapplugin.so
%{_mandir}/man5/%{name}-ldap.cfg.5*
%endif

%files spooler
%defattr(-,root,root,-)
%{_bindir}/%{name}-spooler
%config(noreplace) %attr(0640,%{name},%{name}) %{_sysconfdir}/%{name}/spooler.cfg
%{_sysconfdir}/rc.d/init.d/%{name}-spooler
%{_mandir}/man1/%{name}-spooler.1*
%{_mandir}/man5/%{name}-spooler.cfg.5*

%files utils
%defattr(-,root,root,-)
%{_bindir}/%{name}-admin
%{_bindir}/%{name}-fsck
%{_bindir}/%{name}-passwd
%{_bindir}/%{name}-stats
%{_datadir}/%{name}/audit-parse.pl
%{_datadir}/%{name}/db-calc-storesize
%{_datadir}/%{name}/db-convert-attachments-to-files
%{_datadir}/%{name}/ssl-certificates.sh
%{_datadir}/%{name}/zarafa7-upgrade
%{_mandir}/man1/%{name}-admin.1*
%{_mandir}/man1/%{name}-fsck.1*
%{_mandir}/man1/%{name}-passwd.1*
%{_mandir}/man1/%{name}-stats.1*

%files webaccess
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}-webaccess.conf
%dir %{_sysconfdir}/%{name}/
%dir %{_sysconfdir}/%{name}/webaccess/
%config(noreplace) %{_sysconfdir}/%{name}/webaccess/config.php
%{_datadir}/%{name}-webaccess/
%dir %{_localstatedir}/lib/%{name}-webaccess/
%attr(-,apache,apache) %dir %{_localstatedir}/lib/%{name}-webaccess/tmp/

%files -n libmapi
%defattr(-,root,root,-)
%{_libdir}/libarchiver.so.*
%{_libdir}/libicalmapi.so.*
%{_libdir}/libinetmapi.so.*
%{_libdir}/libmapi.so.*

%if 0
%files -n perl-MAPI
%defattr(-,root,root,-)
%{perl_vendorarch}/MAPI.pm
%{perl_vendorarch}/auto/MAPI/
%endif

%files -n php-mapi
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%{_datadir}/php/mapi/
%if 0%{?rhel}%{?fedora} > 4
%{_libdir}/php/modules/mapi.so
%else
%{_libdir}/php4/mapi.so
%endif

%if 0%{?rhel}%{?fedora} > 4
%files -n python-MAPI
%defattr(-,root,root,-)
%{python_sitearch}/*
%endif

%changelog
* Sun Nov 20 2011 Robert Scheck <robert@fedoraproject.org> 7.0.3-1
- Upgrade to 7.0.3

* Sat Oct 01 2011 Robert Scheck <robert@fedoraproject.org> 7.0.2-1
- Upgrade to 7.0.2 (#717968)

* Sun Aug 14 2011 Robert Scheck <robert@fedoraproject.org> 7.0.1-1
- Upgrade to 7.0.1 (#725250, #725909, #727346)

* Mon Jun 27 2011 Robert Scheck <robert@fedoraproject.org> 7.0.0-1
- Upgrade to 7.0.0

* Tue Jun 14 2011 Robert Scheck <robert@fedoraproject.org> 6.40.9-1
- Upgrade to 6.40.9

* Sat May 28 2011 Robert Scheck <robert@fedoraproject.org> 6.40.8-1
- Upgrade to 6.40.8

* Wed Apr 06 2011 Robert Scheck <robert@fedoraproject.org> 6.40.7-1
- Upgrade to 6.40.7

* Thu Mar 24 2011 Robert Scheck <robert@fedoraproject.org> 6.40.6-2
- Rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Mon Mar 21 2011 Robert Scheck <robert@fedoraproject.org> 6.40.6-1
- Upgrade to 6.40.6

* Sun Feb 27 2011 Robert Scheck <robert@fedoraproject.org> 6.40.5-1
- Upgrade to 6.40.5

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.40.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Robert Scheck <robert@fedoraproject.org> 6.40.4-1
- Upgrade to 6.40.4

* Fri Oct 29 2010 Robert Scheck <robert@fedoraproject.org> 6.40.3-1
- Upgrade to 6.40.3

* Tue Aug 31 2010 Robert Scheck <robert@fedoraproject.org> 6.40.2-1
- Upgrade to 6.40.2

* Mon Aug 09 2010 Robert Scheck <robert@fedoraproject.org> 6.40.1-1
- Upgrade to 6.40.1

* Tue Jun 15 2010 Robert Scheck <robert@fedoraproject.org> 6.40.0-3
- Rebuild for perl 5.12.1

* Fri Jun 11 2010 Robert Scheck <robert@fedoraproject.org> 6.40.0-2
- Added patch to ensure -pthread for -lclucene configure test

* Thu Jun 10 2010 Robert Scheck <robert@fedoraproject.org> 6.40.0-1
- Upgrade to 6.40.0 (#564135, #565252, #600993)

* Sat May 01 2010 Robert Scheck <robert@fedoraproject.org> 6.30.14-1
- Upgrade to 6.30.14

* Sun Apr 25 2010 Robert Scheck <robert@fedoraproject.org> 6.30.13-1
- Upgrade to 6.30.13
- Moved zarafa.schema file from %%doc to %%{_datadir}/%%{name}

* Sat Mar 20 2010 Robert Scheck <robert@fedoraproject.org> 6.30.12-1
- Upgrade to 6.30.12

* Fri Mar 19 2010 Robert Scheck <robert@fedoraproject.org> 6.30.11-1
- Upgrade to 6.30.11

* Tue Feb 23 2010 Robert Scheck <robert@fedoraproject.org> 6.30.10-2
- Backported a patch from trunk to avoid the crash of zarafa-server
  when creating new user with db or unix plugin (#564282, #567262)
- Backported another patch from trunk to avoid the crash of httpd
  caused by PHP mapi.so during the logon in the webaccess (#564129)

* Sat Feb 06 2010 Robert Scheck <robert@fedoraproject.org> 6.30.10-1
- Upgrade to 6.30.10 (#498194)
- Initial spec file for Fedora and Red Hat Enterprise Linux (thanks
  to Jeroen van Meeuwen, John van der Kamp and Steve Hardy)
