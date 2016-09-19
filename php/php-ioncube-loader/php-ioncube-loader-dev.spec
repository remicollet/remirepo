# remirepo spec file for php-ioncube-loader
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-ioncube-loader}
%global extname       ioncube_loader
%global debug_package %{nil}
%global __debug_install_post /bin/true
%global with_zts      0%{?__ztsphp:1}
%if "%{php_version}" < "5.6"
%global ininame       %{extname}.ini
%else
# [ionCube Loader] The Loader must appear as the first entry in the php.ini
%global ininame       01-%{extname}.ini
%endif

# Open issues
# http://forum.ioncube.com/viewtopic.php?t=4244 - No versio in Reflection
# http://forum.ioncube.com/viewtopic.php?p=10779 - ZTS module broken on EL-5
#

Name:          %{?scl_prefix}php-ioncube-loader
Summary:       Loader for ionCube Encoded Files with ionCube 24 support
Version:       6.0.3
Release:       1%{?dist}%{!?scl:%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}}
License:       Distribuable
Group:         Development/Languages

URL:           http://www.ioncube.com
Source0:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86_%{version}.tar.gz
Source1:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86-64_%{version}.tar.gz
Source2:       LICENSE.txt

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: %{?scl_prefix}php-devel

# ABI check
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

%if "%{?vendor}" == "Remi Collet" && 0%{!?scl:1}
# Other third party repo stuff
Obsoletes:      php53-ioncube-loader <= %{version}
Obsoletes:     php53u-ioncube-loader <= %{version}
Obsoletes:      php54-ioncube-loader <= %{version}
Obsoletes:     php54w-ioncube-loader <= %{version}
%if "%{php_version}" > "5.5"
Obsoletes:     php55u-ioncube-loader <= %{version}
Obsoletes:     php55w-ioncube-loader <= %{version}
%endif
%if "%{php_version}" > "5.6"
Obsoletes:     php56u-ioncube-loader <= %{version}
Obsoletes:     php56w-ioncube-loader <= %{version}
%endif
%if "%{php_version}" > "7.0"
Obsoletes:     php70u-ioncube-loader <= %{version}
Obsoletes:     php70w-ioncube-loader <= %{version}
%endif
%endif

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Loader for ionCube Encoded Files with ionCube 24 support.

Package built for PHP %(%{__php} -n -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%prep
%setup -q -T -c

%ifarch x86_64
tar xvf %{SOURCE1}
%else
tar xvf %{SOURCE0}
%endif

# Drop in the bit of configuration
# Sometime file is missing
# http://forum.ioncube.com/viewtopic.php?t=4245
[ -f ioncube/LICENSE.txt ] || cp %{SOURCE2} ioncube/
sed -e 's/\r//' -i ioncube/*.txt

cat << 'EOF' | tee %{extname}.nts
; Enable %{extname} extension module
zend_extension = %{extname}.so

; ionCube PHP Loader + Intrusion Protection from ioncube24.com configuration
;ic24.enable = 0
;ic24.sec.stop_on_error = 1
;ic24.sec.approve_included_files = ''
;ic24.sec.trusted_include_paths = ''
;ic24.sec.block_uploaded_files = 1
;ic24.api_access_key = ''
;ic24.api_check_ip = 1
;ic24.slt = '7'
;ic24.sec.enable=1
;ic24.sec.exclusion_key = ''
;ic24.cache_path = ''
;ic24.home_dir = ''
;ic24.sec.block_stdin = '1'
;ic24.update_domains_retry_interval = '30'
;ic24.dump_cache = 0
;ic24.phperr.enable = 'auto'
;ic24.phperr.ignore = 0
;ioncube.loader.encoded_paths = ''
;phpd = 1
;phpd.t = 1
EOF

cp %{extname}.nts %{extname}.zts

%if "%{php_version}" < "5.5"
sed -e 's:%{extname}.so:%{php_ztsextdir}/%{extname}.so:' \
    -i %{extname}.zts
sed -e 's:%{extname}.so:%{php_extdir}/%{extname}.so:' \
    -i %{extname}.nts
diff %{extname}.nts %{extname}.zts || : ok
%endif


%build
# tarball provides binaries


%install
rm -rf %{buildroot}
ver=$(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')

if [ ! -f ioncube/%{extname}_lin_${ver}.so ]; then
  : Module for PHP $ver not provided
  exit 1
fi

install -D -pm 755 ioncube/%{extname}_lin_${ver}.so    %{buildroot}%{php_extdir}/%{extname}.so
install -D -m 644  %{extname}.nts                      %{buildroot}%{php_inidir}/%{ininame}

%if %{with_zts}
install -D -pm 755 ioncube/%{extname}_lin_${ver}_ts.so %{buildroot}%{php_ztsextdir}/%{extname}.so
install -D -m 644  %{extname}.zts                      %{buildroot}%{php_ztsinidir}/%{ininame}
%endif


%check
# simple module load test
%{__php} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --version | grep 'ionCube.*%{version}'

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --version | grep 'ionCube.*%{version}'
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license ioncube/LICENSE.txt
#doc ioncube/USER-GUIDE.*

%config(noreplace) %{php_inidir}/%{ininame}
%{php_extdir}/%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ininame}
%{php_ztsextdir}/%{extname}.so
%endif


%changelog
* Mon Sep 19 2016 Remi Collet <remi@remirepo.net> - 6.0.3-1
- update to 6.0.3 (Sep 19, 2016)

* Thu Sep 15 2016 Remi Collet <remi@remirepo.net> - 6.0.1-1
- update to 6.0.1 (Sep 14, 2016)

* Wed Mar 23 2016 Remi Collet <remi@remirepo.net> - 5.1.2-1
- update to 5.1.2 (Mar 22, 2016)

* Sun Feb  7 2016 Remi Collet <remi@remirepo.net> - 5.1.1-1
- update to 5.1.1 (Feb 7, 2016)

* Sat Feb  6 2016 Remi Collet <remi@remirepo.net> - 5.1.0-1
- update to 5.1.0 (Feb 5, 2016)
- add new options in configuration file
- remove README.txt, add USER-GUIDE.pdf
- add missing LICENSE file from previous version

* Wed Jan 27 2016 Remi Collet <remi@remirepo.net> - 5.0.23-1
- update to 5.0.23 (Jan 26, 2016)
- re-add ZTS module on EL-5

* Thu Jan 21 2016 Remi Collet <remi@remirepo.net> - 5.0.22-1
- update to 5.0.22 (Jan 20, 2016)

* Wed Jan 20 2016 Remi Collet <remi@remirepo.net> - 5.0.21-1
- update to 5.0.21 (Jan 19, 2016)

* Sat Jan 16 2016 Remi Collet <remi@remirepo.net> - 5.0.20-1
- update to 5.0.20 (Jan 16, 2016)
- update configuration comments, remove sec.alert_action
  add slt, sec.block_stdin, update_domains_retry_interval
- drop broken ZTS module on EL-5
  http://forum.ioncube.com/viewtopic.php?p=10779

* Tue Oct 20 2015 Remi Collet <remi@remirepo.net> - 5.0.19-1
- update to 5.0.19 (Oct 19, 2015)

* Tue Sep 15 2015 Remi Collet <remi@remirepo.net> - 5.0.18-1
- update to 5.0.18 (Sep 14, 2015)

* Thu Sep 10 2015 Remi Collet <remi@remirepo.net> - 5.0.17-1
- update to 5.0.17 (Sep 9, 2015)

* Fri Aug 28 2015 Remi Collet <remi@remirepo.net> - 5.0.16-1
- update to 5.0.16 (Aug 27, 2015)

* Fri Aug 21 2015 Remi Collet <remi@remirepo.net> - 5.0.15-1
- update to 5.0.15 (Aug 19, 2015)

* Thu Jul 30 2015 Remi Collet <remi@remirepo.net> - 5.0.14-1
- update to 5.0.14 (Jul 29, 2015)

* Tue Jul 28 2015 Remi Collet <remi@remirepo.net> - 5.0.13-1
- update to 5.0.13 (Jul 28, 2015)

* Tue Jul 14 2015 Remi Collet <remi@remirepo.net> - 5.0.12-1
- update to 5.0.12 (Jul 13, 2015)

* Mon Jun 29 2015 Remi Collet <remi@remirepo.net> - 5.0.11-1
- update to 5.0.11 (Jun 28, 2015)

* Tue Jun 23 2015 Remi Collet <remi@remirepo.net> - 5.0.10-1
- update to 5.0.10 (Jun 22, 2015)

* Sat Jun 20 2015 Remi Collet <remi@remirepo.net> - 5.0.9-1
- update to 5.0.9 (Jun 19, 2015)

* Tue Jun 16 2015 Remi Collet <remi@remirepo.net> - 5.0.8-1
- update to 5.0.8 (Jun 16, 2015)
- update configuration with new options

* Sat May 23 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.7-1
- update to 5.0.7 (May 22, 2015)

* Tue May 19 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.6-1
- update to 5.0.6 (May 18, 2015)

* Sun May 17 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.5-1
- update to 5.0.5 (May 15, 2015)

* Mon May 11 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.4-1
- update to 5.0.4 (May 8, 2015)

* Mon May  4 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.3-1
- update to 5.0.3 (May 4, 2015)

* Tue Apr 28 2015 Remi Collet <RPMS@famillecollet.com> - 5.0.1-1
- update to 5.0.1 (Apr 27, 2015)

* Tue Mar  3 2015 Remi Collet <RPMS@famillecollet.com> - 4.7.5-2
- LICENSE.txt and README.txt are back
  http://forum.ioncube.com/viewtopic.php?t=4245
- php 5.5+ don't need full extension path

* Sat Feb 28 2015 Remi Collet <RPMS@famillecollet.com> - 4.7.5-1
- update to 4.7.5 (Feb 27, 2015)

* Thu Feb 12 2015 Remi Collet <RPMS@famillecollet.com> - 4.7.4-1
- update to 4.7.4 (Feb 10, 2015)

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> 4.7.3-1.1
- Fedora 21 SCL mass rebuild

* Wed Dec 17 2014 Remi Collet <RPMS@famillecollet.com> - 4.7.3-1
- update to 4.7.3 (Dec 15, 2014)

* Mon Nov 24 2014 Remi Collet <RPMS@famillecollet.com> - 4.7.2-1
- update to 4.7.2 (Nov 24, 2014)

* Fri Oct 31 2014 Remi Collet <RPMS@famillecollet.com> - 4.7.1-1
- update to 4.7.1 (Oct 31, 2014)

* Sat Oct 18 2014 Remi Collet <RPMS@famillecollet.com> - 4.7.0-1
- update to 4.6.2 (Oct 17, 2014) with PHP 5.6 support

* Thu Oct 16 2014 Remi Collet <RPMS@famillecollet.com> - 4.6.2-1
- update to 4.6.2 (Oct 14, 2014)

* Mon Sep  1 2014 Remi Collet <RPMS@famillecollet.com> - 4.6.1-2
- allow SCL build
- make ZTS optional

* Tue Apr 22 2014 Remi Collet <RPMS@famillecollet.com> - 4.6.1-1
- update to 4.6.1 (Apr 22, 2014)

* Sun Apr  6 2014 Remi Collet <RPMS@famillecollet.com> - 4.6.0-1
- update to 4.6.0 (Apr 4, 2014)

* Tue Feb 18 2014 Remi Collet <RPMS@famillecollet.com> - 4.5.3-1
- update to 4.5.3 (Feb 11, 2014)

* Sat Jan 18 2014 Remi Collet <RPMS@famillecollet.com> - 4.5.2-1
- update to 4.5.2

* Sat Jan 11 2014 Remi Collet <RPMS@famillecollet.com> - 4.5.1-1
- update to 4.5.1

* Sat Oct 19 2013 Remi Collet <RPMS@famillecollet.com> - 4.4.4-1
- update to 4.4.4 (php 5.4 only)

* Mon Sep 16 2013 Remi Collet <RPMS@famillecollet.com> - 4.4.3-1
- update to 4.4.3 (php 5.4 only)

* Mon Jun 24 2013 Remi Collet <RPMS@famillecollet.com> - 4.4.1-1
- update to 4.4.1

* Mon Sep  3 2012 Remi Collet <RPMS@famillecollet.com> - 4.2.2-1
- initial package

