%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Notification

Name:           php-horde-Horde-Notification
Version:        1.0.1
Release:        1%{?dist}
Summary:        Horde Notification System

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch

BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) >= 1.0.0
Requires:       php-pear(pear.horde.org/Horde_Util) < 2.0.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)

Provides:       php-pear(pear.horde.org/Horde_Notification) = %{version}

%description
A library implementing a subject-observer pattern for raising and showing
messages of different types and to different listeners.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Horde/Notification/Event/Status.php
%{pear_phpdir}/Horde/Notification/Handler/Decorator/Alarm.php
%{pear_phpdir}/Horde/Notification/Handler/Decorator/Base.php
%{pear_phpdir}/Horde/Notification/Handler/Decorator/Log.php
%{pear_phpdir}/Horde/Notification/Listener/Audio.php
%{pear_phpdir}/Horde/Notification/Listener/Status.php
%{pear_phpdir}/Horde/Notification/Storage/Interface.php
%{pear_phpdir}/Horde/Notification/Storage/Object.php
%{pear_phpdir}/Horde/Notification/Storage/Session.php
%{pear_phpdir}/Horde/Notification/Event.php
%{pear_phpdir}/Horde/Notification/Exception.php
%{pear_phpdir}/Horde/Notification/Handler.php
%{pear_phpdir}/Horde/Notification/Listener.php
%{pear_phpdir}/Horde/Notification.php

%{pear_testdir}/Horde_Notification


%changelog
* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
