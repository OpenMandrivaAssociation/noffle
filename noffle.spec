%define name		noffle
%define version 1.1.5
%define release %mkrel 7
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

