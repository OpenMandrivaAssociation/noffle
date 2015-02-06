%define name		noffle
%define version 1.1.5
%define release 8
%define spooldir	%{_var}/spool/%{name}
%define cfgfilename	%{_sysconfdir}/%{name}.conf

Summary: 	Usenet newsserver for small sites
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Group:		System/Servers
License:	GPL
URL:		http://noffle.sf.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source:		http://dl.sf.net/noffle/%{name}-%{version}.tar.bz2
Source1:	noffle.xinetd.bz2
BuildRequires:	gdbm-devel
Requires:	MailTransportAgent common-licenses
Requires(post,preun):	rpm-helper

%description
NOFFLE is a news server optimized for low speed dialup connection to the
Internet and few users. It allows reading news offline with many news reader
programs, even if they do not support offline reading by themselves.

%prep
%setup -q

%build
#CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="-s"
#export CFLAGS LDFLAGS
#./configure --prefix=/usr --enable-debug=no
#make
%serverbuild
%configure --with-spooldir=%{spooldir} --with-configfile=%{cfgfilename} \
	--enable-debug=no 
%make

%install
# noffle doesn't have a make install :(
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man{1,5},%{_sysconfdir}{,/{cron.daily,xinetd.d}}}
mkdir -p %{buildroot}%{spooldir}/{data,lock,requested,outgoing,overview}
mkdir -p %{buildroot}%{_sysconfdir}
cp src/noffle				%{buildroot}%{_bindir}/
ln -s noffle %{buildroot}%{_bindir}/inews
cp docs/noffle.1			%{buildroot}%{_mandir}/man1/
cp docs/noffle.conf.5			%{buildroot}%{_mandir}/man5/
cp noffle.conf.example			%{buildroot}%{cfgfilename}
cp packages/redhat/noffle-expire	%{buildroot}%{_sysconfdir}/cron.daily/
bzip2 -cd %{SOURCE1}		      > %{buildroot}%{_sysconfdir}/xinetd.d/noffle

#install -o 0 -g 0 -d $RPM_BUILD_ROOT/usr/bin
#install -s -m 4755 -o news -g news src/noffle $RPM_BUILD_ROOT/usr/bin
#install -o 0 -g 0 -d $RPM_BUILD_ROOT/usr/man/man1
#install -m 0644 -o 0 -g 0 docs/noffle.1 $RPM_BUILD_ROOT/usr/man/man1/noffle.1
#install -o 0 -g 0 -d $RPM_BUILD_ROOT/usr/man/man5
#install -m 0644 -o 0 -g 0 docs/noffle.conf.5 $RPM_BUILD_ROOT/usr/man/man5/noffle.conf.5
#install -m 2755 -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle
#install -o 0 -g 0 -d $RPM_BUILD_ROOT/etc
#install -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle/data
#install -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle/lock
#install -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle/requested
#install -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle/outgoing
#install -o news -g news -d $RPM_BUILD_ROOT/var/spool/noffle/overview
#install -m 0600 -o news -g news noffle.conf.example $RPM_BUILD_ROOT/etc/noffle.conf
#install -o 0 -g 0 -d $RPM_BUILD_ROOT/etc/cron.daily
#install -m 0755 -o news -g news packages/redhat/noffle-expire $RPM_BUILD_ROOT/etc/cron.daily/noffle-expire

%post
%_post_service %{name}
echo
echo " Don't forget to edit %{cfgfilename} !!! "
echo

%preun
%_preun_service %{name}

%clean
[ "$RPM_BUILD_ROOT" != "" ] && rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README INSTALL ChangeLog docs/FAQ docs/NOTES docs/INTERNALS
%doc docs/noffle.lsm noffle.conf.example
%attr(0644,root,root)	%config(noreplace) %{_sysconfdir}/xinetd.d/noffle
%{_bindir}/inews
%defattr(-,news,news)
%attr(4755,news,news)	%{_bindir}/noffle
%attr(0644,root,root)	%doc %{_mandir}/man*/noffle*
%attr(0600,news,news)	%config(noreplace) %{cfgfilename}
%attr(0755,news,news)	%config(noreplace) %{_sysconfdir}/cron.daily/noffle-expire
%attr(2755,news,news)	%dir %{spooldir}
%attr(0755,news,news)	%dir %{spooldir}/data
%attr(0755,news,news)	%dir %{spooldir}/lock
%attr(0755,news,news)	%dir %{spooldir}/requested
%attr(0755,news,news)	%dir %{spooldir}/outgoing
%attr(0755,news,news)	%dir %{spooldir}/overview



%changelog
* Tue May 03 2011 Michael Scherer <misc@mandriva.org> 1.1.5-7mdv2011.0
+ Revision: 664789
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.1.5-5mdv2010.0
+ Revision: 430180
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.1.5-4mdv2009.0
+ Revision: 254055
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Wed Dec 19 2007 Thierry Vignaud <tv@mandriva.org> 1.1.5-2mdv2008.1
+ Revision: 133085
- fix gdbm-devel BR
- fix prereq on rpm-helper
- kill re-definition of %%buildroot on Pixel's request
- use %%mkrel
- import noffle


* Fri May 13 2005 Nicolas Lécureuil <neoclust@mandriva.org> 1.1.5-2mdk
- Rebuild

* Fri Jan 14 2005 Per Ã˜yvind Karlsen <peroyvind@linux-mandrake.com> 1.1.5-1mdk
- 1.1.5

* Tue Feb 24 2004 Lenny Cartier <lenny@mandrakesoft.com> 1.1.2-2mdk
- rebuild

* Sat Dec 28 2002 Alexander Skwar <ASkwar@DigitalProjects.com> 1.1.2-1mdk
- 1.1.2

* Wed Jan 09 2002 Alexander Skwar <ASkwar@Linux-Mandrake.com> 1.1.1-1mdk
- First Mandrake version

* Wed Oct 31 2001 Jim Hague <jim.hague@acm.org>
- Up version to 1.1-1, and remove inews from %%files as it is created by %%post.
  Remove relocation prefix - it wasn't working properly. Also
  RPM 4 seems to automatically compress man pages, so put man pages in
  %%files as /usr/man/* so we pick up whatever is there, compressed or not.

* Thu Oct 26 2000 Jim Hague <jim.hague@am.org>
- Added inews link.

* Sun Jun 18 2000 Jim Hague <jim.hague@am.org>
- Version 1.0pre6-3 RPM
- Changed /etc/noffle.conf mode to 0600 in case server password is required
- Added noffle line to /etc/hosts.deny
- Make inetd.conf handling match linuxconf - don't keep old files and only
  add entries if nntp line is not already present, even if commented out,
  and only remove conf lines on an uninstall

* Fri Jun 16 2000 Jim Hague <jim.hague@am.org>
- Version 1.0pre6-2 RPM
- Added /etc/cron.daily/noffle-expire

* Thu Jun 15 2000 Jim Hague <jim.hague@am.org>
- Version 1.0pre6-1 RPM
- Modified SPEC from 1.0pre5

* Wed May 17 2000 Soenke J. Peters <peters+rpm@simprovement.com>
- Version 1.0pre5-1 RPM
- built SPEC from scratch

* Mon Aug 23 1999 Mario Moder <moderm@gmx.net>
- Version 1.0pre2-1 Binary only RPM, no SPEC available

