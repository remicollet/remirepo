%{!?__pecl:   %{expand: %%global __pecl   %{_bindir}/pecl}}
%global php_apiver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)
%global php_extver  %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP Extension => //p') | tail -1)
%global pecl_name   amqp


Summary:       Communicate with any AMQP compliant server
Name:          php-pecl-amqp
Version:       1.0.1
Release:       2%{?dist}
# https://bugs.php.net/61337 - missing LICENSE file
License:       PHP
Group:         Development/Languages
URL:           http://pecl.php.net/package/amqp
Source0:       http://pecl.php.net/get/%{pecl_name}-%{version}.tgz

# http://svn.php.net/viewvc?view=revision&revision=324074
Patch0:        %{pecl_name}-php54.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php-devel
BuildRequires: php-pear
BuildRequires: librabbitmq-devel

%if 0%{?php_zend_api:1}
# For Fedora and EL >= 6
Requires:         php(zend-abi) = %{php_zend_api}
Requires:         php(api) = %{php_core_api}
%else
# For EL = 5
Requires:         php-zend-abi = %{php_extver}
Requires:         php-api = %{php_apiver}
%endif
Requires(post):   %{__pecl}
Requires(postun): %{__pecl}
Provides:         php-pecl(%{pecl_name}) = %{version}-%{release}


# RPM 4.8
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
# RPM 4.9
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}%{_libdir}/.*\\.so$


%description
This extension can communicate with any AMQP spec 0-9-1 compatible server,
such as RabbitMQ, OpenAMQP and Qpid, giving you the ability to create and
delete exchanges and queues, as well as publish to any exchange and consume
from any queue.


%prep
%setup -q -c

%patch0 -p0 -b php54

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


%build
cd %{pecl_name}-%{version}
phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make -C %{pecl_name}-%{version} \
     install INSTALL_ROOT=%{buildroot}

# Drop in the bit of configuration
install -Dpm 644 %{pecl_name}.ini %{buildroot}%{_sysconfdir}/php.d/%{pecl_name}.ini

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml


%check
# No test provided, just minimal load test
php --no-php-ini \
    --define extension_dir=%{pecl_name}-%{version}/modules \
    --define extension=%{pecl_name}.so \
    -m | grep %{pecl_name}


%clean
rm -rf %{buildroot}


%if 0%{?pecl_install:1}
%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
%endif


%if 0%{?pecl_uninstall:1}
%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%files
%defattr(-,root,root,-)
%doc %{pecl_name}-%{version}/CREDITS
%config(noreplace) %{_sysconfdir}/php.d/%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml


%changelog
* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-2
- rebuild for PHP 5.4

* Sat Mar 10 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial RPM release without ZTS extension
- open request for LICENSE file https://bugs.php.net/61337

