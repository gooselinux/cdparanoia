Summary: A Compact Disc Digital Audio (CDDA) extraction tool (or ripper).
Name: cdparanoia
Version: 10.2
Release: 5.1%{?dist}
# the app is GPLv2, everything else is LGPLv2
License: GPLv2 and LGPLv2
Group: Applications/Multimedia
URL: http://www.xiph.org/paranoia/index.html
Source: http://downloads.xiph.org/releases/%{name}/%{name}-III-%{version}.src.tgz
# Patch from upstream to fix cdda_interface.h C++ incompatibility ("private")
# https://trac.xiph.org/changeset/15338
# https://bugzilla.redhat.com/show_bug.cgi?id=463009
Patch0: cdparanoia-10.2-#463009.patch
# #466659
Patch1: cdparanoia-10.2-endian.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: cdparanoia-libs = %{version}-%{release}
Obsoletes: cdparanoia-III

%description 
Cdparanoia (Paranoia III) reads digital audio directly from a CD, then
writes the data to a file or pipe in WAV, AIFC or raw 16 bit linear
PCM format.  Cdparanoia doesn't contain any extra features (like the ones
included in the cdda2wav sampling utility).  Instead, cdparanoia's strength
lies in its ability to handle a variety of hardware, including inexpensive
drives prone to misalignment, frame jitter and loss of streaming during
atomic reads.  Cdparanoia is also good at reading and repairing data from
damaged CDs.

%package devel
Summary: Development tools for libcdda_paranoia (Paranoia III).
Group: Development/Libraries
Requires: cdparanoia-libs = %{version}-%{release}
License: LGPLv2

%description devel
The cdparanoia-devel package contains the static libraries and header
files needed for developing applications to read CD Digital Audio disks.

%package libs
Summary: Libraries for libcdda_paranoia (Paranoia III).
Group: Development/Libraries
License: LGPLv2

%description libs
The cdparanoia-libs package contains the dynamic libraries needed for
applications which read CD Digital Audio disks.

%prep
%setup -q -n %{name}-III-%{version}
%patch0 -p3 -b .#463009
%patch1 -p1 -b .endian

%build
rm -rf $RPM_BUILD_ROOT
export OPT="${CFLAGS:-%optflags} -O0 -Wno-pointer-sign -Wno-unused -Werror-implicit-function-declaration"
%configure --includedir=%{_includedir}/cdda
make OPT="$OPT"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_includedir}/cdda
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 0755 cdparanoia $RPM_BUILD_ROOT%{_bindir}
install -m 0644 cdparanoia.1 $RPM_BUILD_ROOT%{_mandir}/man1/ 
install -m 0644 utils.h paranoia/cdda_paranoia.h interface/cdda_interface.h \
	$RPM_BUILD_ROOT%{_includedir}/cdda
install -m 0755 paranoia/libcdda_paranoia.so.0.10.? \
	interface/libcdda_interface.so.0.10.? \
	$RPM_BUILD_ROOT%{_libdir}
install -m 0755 paranoia/libcdda_paranoia.a interface/libcdda_interface.a \
	$RPM_BUILD_ROOT%{_libdir}

/sbin/ldconfig -n $RPM_BUILD_ROOT/%{_libdir}

pushd $RPM_BUILD_ROOT%{_libdir}
ln -s libcdda_paranoia.so.0.10.? libcdda_paranoia.so
ln -s libcdda_interface.so.0.10.? libcdda_interface.so
popd

%post -n cdparanoia-libs
/sbin/ldconfig

%postun -n cdparanoia-libs
if [ "$1" -ge "1" ]; then
  /sbin/ldconfig
fi

%clean
[ "$RPM_BUILD_ROOT" != "/" -a -d "$RPM_BUILD_ROOT" ] && rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root)
%{_libdir}/*.so*

%files devel
%defattr(-,root,root)
%{_includedir}/cdda
%{_libdir}/*.a

%changelog
* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 10.2-5.1
- Rebuilt for RHEL 6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com>
- Merge review cleanups (not finished, #225638)

* Tue Feb 10 2009 Adam Jackson <ajax@redhat.com> 10.2-3
- cdparanoia-10.2-endian.patch: Backport a crash fix for host/drive
  endianness mismatch. (#466659)

* Tue Sep 30 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 10.2-2
- fix cdda_interface.h C++ incompatibility (patch from upstream) (#463009)

* Thu Sep 11 2008 Adam Jackson <ajax@redhat.com> 10.2-1
- cdparanoia 10.2

* Wed Aug 13 2008 Adam Jackson <ajax@redhat.com> 10.1-1
- Update to 10.1, just changes the license back.

* Tue Jul 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 10.0-3
- fix license tag
- fix headers, setspeed patch to apply with fuzz=0

* Thu Jun 19 2008 Adam Jackson <ajax@redhat.com> 10.0-2
- cdparanoia 10.

* Thu Mar 20 2008 Adam Jackson <ajax@redhat.com> alpha9.8-30
- Add -Werror-implicit-function-declarations.
- cdparanoia-III-alpha9.8-headers.patch: Fix the resulting errors.

* Tue Mar 04 2008 Adam Jackson <ajax@redhat.com> alpha9.8-29
- cdparanoia-III-alpha9.8.scsi-setspeed.patch: Allow setting the speed of
  SCSI CD drives. (#431178)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - alpha9.8-28.2
- Autorebuild for GCC 4.3

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-27.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-27.1
- bump again for double-long bug on ppc(64)

* Wed Feb 08 2006 Monty Montgomery <cmontgom@redhat.com> - alpha9.8-27
- rebuilt 

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - alpha9.8-26.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- make sure shared libs are linked against respective other libs

* Wed Mar 16 2005 Peter Jones <pjones@redhat.com> alpha9.8-25
- gcc4 rebuild and CFLAGS change

* Wed Feb 9 2005 Peter Jones <pjones@redhat.com> alpha9.8-24.2
- Rebuild for new toolchain

* Wed Oct 6 2004 Peter Jones <pjones@redhat.com> alpha9.8-24
- workaround for sgio read size issues in newer kernels.

* Fri Oct 1 2004 Peter Jones <pjones@redhat.com> alpha9.8-23
- "This time, with a meaningful changelog" release.  Just like -22.
- new SG_IO code in rawhide.  This means ripping will no longer use the 
  "cooked ioctl" mode that it has since we moved to 2.6, instead utilizing
  the real scsi-based command set to talk to most drives.  This should
  result in better error correction handling, and usage of much more
  commonly used kernel features.
- environment variable "CDDA_TRANSPORT" added.  If you set this to "cooked",
  cdparanoia will try to use the "cooked ioctl" mode instead of SCSI/SG_IO
  based modes first, and then fall back to SG_IO.
- It'd be good if this got some testing.  A prior version of the SG_IO code
  was known to fail on some USB drives.  This version should mitigate that
  quite a bit, but I lack the hardware to test it for sure.
  
* Wed Jul 7 2004 Peter Jones <pjones@redhat.com> alpha9.8-21sgio1
- a new set of sgio patches

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 17 2004 Peter Jones <pjones@redhat.com> alpha9.8-20
- take ownership of %{_includedir}/cdda

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 20 2003 Peter Jones <pjones@redhat.com> alpha9.8-17
- typo fix (g_fd -> fd)
- add errno output

* Tue May 06 2003 Peter Jones <pjones@redhat.com> alpha9.8-16
- fix warnings on switches
- use O_EXCL

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlinks to shared libs

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Dec 25 2002 Tim Powers <timp@redhat.com> alpha9.8-13
- fix %%install references in the changelog so that it will rebuild properly

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> alpha9.8-12
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr  3 2002 Peter Jones <pjones@redhat.com> alpha9.8-8
- don't strip, let rpm do that

* Mon Feb 25 2002 Tim Powers <timp@redhat.com> alpha9.8-7
- fix broken Obsoletes of cdparanoia-devel

* Thu Dec  6 2001 Peter Jones <pjones@redhat.com> alpha9.8-6
- move includes to %{_includedir}/cdda/
- add utils.h to %%install
- clean up %%install some.

* Sun Nov  4 2001 Peter Jones <pjones@redhat.com> alpha9.8-5
- make a -libs package which contains the .so files
- make the cdparanoia dependancy towards that, not -devel

* Thu Aug  2 2001 Peter Jones <pjones@redhat.com>
- bump the release not to conflict with on in the RH build tree :/
- reverse devel dependency

* Wed Aug  1 2001 Peter Jones <pjones@redhat.com>
- fix %post and %postun to only run ldconfig for devel packages

* Wed Jul 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- devel now depends on package

* Wed Mar 28 2001 Peter Jones <pjones@redhat.com>
- 9.8 release.

* Tue Feb 27 2001 Karsten Hopp <karsten@redhat.de>
- fix spelling error in description

* Thu Dec  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- rebuild for new tree

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use %%{_tmppath}

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Wed Jun 06 2000 Preston Brown <pbrown@redhat.com>
- revert name change
- use new rpm macro paths

* Wed Apr 19 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Switched spec file from the one used in Red Hat Linux 6.2, which
  also changes the name
- gzip man page

* Thu Dec 23 1999 Peter Jones <pjones@redhat.com>
- update package to provide cdparanoia-alpha9.7-2.*.rpm and 
  cdparanoia-devel-alpha9.7-2.*.rpm.  Also, URLs point at xiph.org
  like they should.

* Wed Dec 22 1999 Peter Jones <pjones@redhat.com>
- updated package for alpha9.7, based on input from:
  Monty <xiphmont@xiph.org> 
  David Philippi <david@torangan.saar.de>

* Mon Apr 12 1999 Michael Maher <mike@redhat.com>
- updated pacakge

* Tue Oct 06 1998 Michael Maher <mike@redhat.com>
- updated package

* Mon Jun 29 1998 Michael Maher <mike@redhat.com>
- built package
