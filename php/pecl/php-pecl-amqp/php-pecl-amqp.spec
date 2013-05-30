%{!?__pecl:   %{expand: %%global __pecl   %{_bindir}/pecl}}
%global pecl_name   amqp

Summary:       Communicate with any AMQP compliant server
Name:          php-pecl-amqp
Version:       1.2.0
Release:       1%{?dist}.1
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/amqp
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel > 5.2.0
BuildRequires: php-pear
BuildRequires: librabbitmq-devel

Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
Requires(post):   %{__pecl}
Requires(postun): %{__pecl}

Provides:         php-%{pecl_name} = %{version}
Provides:         php-%{pecl_name}%{?_isa} = %{version}
Provides:         php-pecl(%{pecl_name}) = %{version}
Provides:         php-pecl(%{pecl_name})%{?_isa} = %{version}

# Other third party repo stuff
Obsoletes:     php53-pecl-%{pecl_name}
Obsoletes:     php53u-pecl-%{pecl_name}
%if "%{php_version}" > "5.4"
Obsoletes:     php54-pecl-%{pecl_name}
%endif
%if "%{php_version}" > "5.5"
Obsoletes:     php55-pecl-%{pecl_name}
%endif


# filter private shared
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
This extension can communicate with any AMQP spec 0-9-1 compatible server,
such as RabbitMQ, OpenAMQP and Qpid, giving you the ability to create and
delete exchanges and queues, as well as publish to any exchange and consume
from any queue.


%prep
%setup -q -c

cd %{pecl_name}-%{version}

# Upstream often forget to change this
extver=$(sed -n '/#define PHP_AMQP_VERSION/{s/.* "//;s/".*$//;p}' php_amqp.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
cd ..

cat > %{pecl_name}.ini << 'EOF'
; Enable %{pecl_name} extension module
extension = %{pecl_name}.so

; http://www.php.net/manual/en/amqp.configuration.php

; Whether calls to AMQPQueue::get() and AMQPQueue::consume()
; should require that the client explicitly acknowledge messages. 
; Setting this value to 1 will pass in the AMQP_AUTOACK flag to
: the above method calls if the flags field is omitted. 
;amqp.auto_ack = 0

; The host to which to connect.
;amqp.host = localhost

; The login to use while connecting to the broker.
;amqp.login = guest

; The password to use while connecting to the broker.
;amqp.password = guest

; The port on which to connect.
;amqp.port = 5672

; The number of messages to prefect from the server during a 
; call to AMQPQueue::get() or AMQPQueue::consume() during which
; the AMQP_AUTOACK flag is not set.
;amqp.prefetch_count = 3

; The virtual host on the broker to which to connect.
;amqp.vhost = /
EOF

cp -pr %{pecl_name}-%{version} %{pecl_name}-zts


%build
cd %{pecl_name}-%{version}
phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{pecl_name}-zts
zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}
make -C %{pecl_name}-zts \
     install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{php_ztsinidir}/%{pecl_name}.ini

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
# No test provided, just minimal load test
%{__php} --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    -m | grep %{pecl_name}

%{__ztsphp} --no-php-ini \
    --define extension_dir=%{pecl_name}-zts/modules \
    --define extension=%{pecl_name}.so \
    -m | grep %{pecl_name}


%clean
rm -rf %{buildroot}


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/{CREDITS,LICENSE}
%config(noreplace) %{php_inidir}/%{pecl_name}.ini
%config(noreplace) %{php_ztsinidir}/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{php_ztsextdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- Update to 1.0.10

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 1.0.9-3
- rebuild for new librabbitmq

* Tue Nov 13 2012 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9

* Mon Nov 12 2012 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8
- build ZTS extension
- also provides php-amqp

* Wed Sep 12 2012 Remi Collet <remi@fedoraproject.org> - 1.0.7-1
- update to 1.0.7
- cleanups

* Mon Aug 27 2012 Remi Collet <remi@fedoraproject.org> - 1.0.5-1
- update to 1.0.5
- LICENSE now provided in upstream tarball

* Wed Aug 01 2012 Remi Collet <remi@fedoraproject.org> - 1.0.4-1
- update to 1.0.4

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat May 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- update to 1.0.3
- add extension version check (and fix)

* Mon Mar 19 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- clean EL-5 stuff as requires php 5.2.0, https://bugs.php.net/61351

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- rebuild for PHP 5.4

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM release without ZTS extension
- open request for LICENSE file https://bugs.php.net/61337

