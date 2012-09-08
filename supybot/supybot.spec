%global origname Supybot
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           supybot
Version:        0.83.4.1
Release:        9%{?dist}
Summary:        Cross-platform IRC bot written in Python

Group:          Applications/Internet
# The entire source code is BSD except for
# Supybot-0.83.4/plugins/Math/local/convertcore.py which is GPLv2
License:        BSD and GPLv2
URL:            http://supybot.com
Source0:        http://downloads.sourceforge.net/supybot/%{origname}-%{version}.tar.bz2
# Fix a conflict between python-json and the built in json module
# in Python 2.6.  Already submitted and commited upstream.
Patch0:         %{name}-%{version}-json.patch
#fix karma plugin to actually work should go upstream
Patch1:         Supybot-0.83.4.1-karma-plugin.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch:      noarch
BuildRequires:  python-setuptools-devel
Requires:       python-twisted-core
Requires:       python-twisted-names
Requires:       python-dateutil
Requires:       python-feedparser
Requires:       python-dictclient
Requires:       python-simplejson
Provides:       Supybot = %{version}-%{release}
Conflicts:	supybot-gribble

%description
Supybot is a robust, user-friendly, and programmer-friendly Python IRC bot.
It aims to be an adequate replacement for most existing IRC bots.  It
includes a very flexible and powerful ACL system for controlling access
to commands, as well as more than 50 builtin plugins providing around
400 actual commands.

%prep
%setup -q -n %{origname}-%{version}
%patch0 -p1
%patch1 -p1


%build
CFLAGS="%{optflags}" %{__python} -c 'import setuptools; execfile("setup.py")' build


%install
%{__rm} -rf %{buildroot}
%{__python} -c 'import setuptools; execfile("setup.py")' install \
    --skip-build --root %{buildroot}

%{__install} -d -m 755 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-adduser.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-botchk.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-plugin-create.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-plugin-doc.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-test.1 %{buildroot}%{_mandir}/man1/
%{__install} -m 644 docs/man/supybot-wizard.1 %{buildroot}%{_mandir}/man1/

# These are provided in python-feedparser, python-dateutil,
# python-dictclient, and python-simplejson
%{__rm} -rf %{buildroot}%{python_sitelib}/supybot/plugins/RSS/local
%{__rm} -rf %{buildroot}%{python_sitelib}/supybot/plugins/Time/local
%{__rm} -rf %{buildroot}%{python_sitelib}/supybot/plugins/Dict/local
%{__rm} -rf %{buildroot}%{python_sitelib}/supybot/plugins/Google/local


%clean
%{__rm} -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc ACKS ChangeLog LICENSE README RELNOTES
%doc docs/{ADVANCED_PLUGIN_CONFIG,ADVANCED_PLUGIN_TESTING,CAPABILITIES}
%doc docs/{CONFIGURATION,FAQ,GETTING_STARTED,PLUGIN_TUTORIAL,STYLE}
%doc docs/{USING_UTILS,USING_WRAP}
%{python_sitelib}/*egg-info
%{python_sitelib}/supybot
%{_bindir}/supybot
%{_bindir}/supybot-adduser
%{_bindir}/supybot-botchk
%{_bindir}/supybot-plugin-create
%{_bindir}/supybot-plugin-doc
%{_bindir}/supybot-plugin-package
%{_bindir}/supybot-test
%{_bindir}/supybot-wizard
%{_mandir}/man1/supybot.1*
%{_mandir}/man1/supybot-adduser.1*
%{_mandir}/man1/supybot-botchk.1*
%{_mandir}/man1/supybot-plugin-create.1*
%{_mandir}/man1/supybot-plugin-doc.1*
%{_mandir}/man1/supybot-test.1*
%{_mandir}/man1/supybot-wizard.1*


%changelog
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 18 2011 Dave Riches <dcr226@fedoraproject.org> - 0.83.4.1-7
- added conflict with supybot-gribble

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.83.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 03 2010 Dennis Gilmore <dennis@ausil.us> - 0.83.4.1-4
- actually apply the patch

* Thu Jun 03 2010 Dennis Gilmore <dennis@ausil.us> - 0.83.4.1-3
- add a patch to make the karma plugin work

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 03 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.83.4.1-1
- Upstream released new version.

* Mon May 18 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.83.4-1
- Upstream released new version.

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-11
- Change define to global.
- Remove old >= 8 conditional.
- Remove unnecessary BuildRequires on python-devel.

* Sat Apr 11 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-10
- Backporting Python 2.6 fixes from Supybot git.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.83.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.83.3-8
- Rebuild for Python 2.6

* Thu Jun 05 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-7
- Uncomment python-dictclient requirement.

* Wed May 24 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-6
- Add Requires for plugin dependencies.
- Add Provides Supybot.

* Wed May 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-5
- Apply Douglas Warner's patch to fix line lengths/add origname macro.

* Wed May 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-4
- Rename from Supybot to supybot.
- Fix incorrect paths to rm.

* Sun Apr 06 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-3
- Remove included Python modules.
- Mention different license for plugins/Math/convertcore.py.

* Fri Mar 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-2
- Use macros instead of calling commands directly.

* Fri Mar 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.3-1
- Update for 0.83.3 release.

* Fri Mar 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.2-3
- Generate egg-info for Fedora <= 8, add to files section.

* Fri Mar 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.2-2
- Use consistent macro style.
- Update source URLs to match guidelines more precisely.

* Fri Mar 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 0.83.2-1
- Initial RPM Package.

