%define separate_devel_static 1

Summary: A collection of utilities and DSOs to handle compiled objects
Name: elfutils
Version: 0.170
Release: 1
License: GPLv3+ and (GPLv2+ or LGPLv3+)
Group: Development/Tools
URL: https://sourceware.org/elfutils/
Source: %{name}-%{version}.tar.bz2
Requires: elfutils-libelf-%{_arch} = %{version}-%{release}
Requires: elfutils-libs-%{_arch} = %{version}-%{release}

BuildRequires: bison >= 1.875
BuildRequires: flex >= 2.5.4a
BuildRequires: bzip2
BuildRequires: gcc >= 3.4

BuildRequires: zlib-devel >= 1.2.2.3
BuildRequires: bzip2-devel
BuildRequires: xz-devel

%define _gnu %{nil}
%define _program_prefix eu-

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readelf (to see the raw ELF file structures), and elflint
(to check for well-formed ELF files).


%package libs
Summary: Libraries to handle compiled objects
Group:  System/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-libs-%{_arch} = %{version}-%{release}
Requires: elfutils-libelf-%{_arch} = %{version}-%{release}

%description libs
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling.  These libraries are used by the programs
in the elfutils package.  The elfutils-devel package enables building
other programs using these libraries.

%package devel
Summary: Development libraries to handle compiled objects
Group: Development/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-devel-%{_arch} = %{version}-%{release}
Requires: elfutils-libs-%{_arch} = %{version}-%{release}
Requires: elfutils-libelf-devel-%{_arch} = %{version}-%{release}
%if !0%{?separate_devel_static}
Requires: elfutils-devel-static-%{_arch} = %{version}-%{release}
%endif

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libebl provides some
higher-level ELF access functionality.  libdw provides access to
the DWARF debugging information.  libasm provides a programmable
assembler interface.

%package devel-static
Summary: Static archives to handle compiled objects
Group: Development/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-devel-static-%{_arch} = %{version}-%{release}
Requires: elfutils-devel-%{_arch} = %{version}-%{release}
Requires: elfutils-libelf-devel-static-%{_arch} = %{version}-%{release}

%description devel-static
The elfutils-devel-static package contains the static archives
with the code to handle compiled objects.

%package libelf
Summary: Library to read and write ELF files
Group: System/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-libelf-%{_arch} = %{version}-%{release}
Obsoletes: libelf <= 0.8.2-2

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary: Development support for libelf
Group: Development/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-libelf-devel-%{_arch} = %{version}-%{release}
Requires: elfutils-libelf-%{_arch} = %{version}-%{release}
%if !0%{?separate_devel_static}
Requires: elfutils-libelf-devel-static-%{_arch} = %{version}-%{release}
%endif
Obsoletes: libelf-devel <= 0.8.2-2

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package libelf-devel-static
Summary: Static archive of libelf
Group: Development/Libraries
License: GPLv2+ or LGPLv3+
Provides: elfutils-libelf-devel-static-%{_arch} = %{version}-%{release}
Requires: elfutils-libelf-devel-%{_arch} = %{version}-%{release}

%description libelf-devel-static
The elfutils-libelf-static package contains the static archive
for libelf.

%prep
%setup -q -n %{name}-%{version}/%{name}

find . -name \*.sh ! -perm -0100 -print | xargs chmod +x

%build
# Remove -Wall from default flags.  The makefiles enable enough warnings
# themselves, and they use -Werror.  Appending -Wall defeats the cases where
# the makefiles disable some specific warnings for specific code.
RPM_OPT_FLAGS=${RPM_OPT_FLAGS/-Wall/}
RPM_OPT_FLAGS=${RPM_OPT_FLAGS/-Wunused/}

%reconfigure CFLAGS="$RPM_OPT_FLAGS -fexceptions" --disable-werror --enable-maintainer-mode
make %{?_smp_mflags} 

%install
rm -rf ${RPM_BUILD_ROOT}
make -s install DESTDIR=${RPM_BUILD_ROOT}

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/elfutils/lib*.so*

# XXX Nuke unpackaged files
(cd ${RPM_BUILD_ROOT}
 rm -f .%{_bindir}/eu-ld
 rm -rf .%{_datadir}/locale
)

%check
#make -s check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING COPYING-GPLV2 COPYING-LGPLV3
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-nm
%{_bindir}/eu-objdump
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-stack
%{_bindir}/eu-strings
%{_bindir}/eu-strip
%{_bindir}/eu-unstrip
%{_bindir}/eu-make-debug-archive
%{_bindir}/eu-elfcompress

%files libs
%defattr(-,root,root)
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libasm-*.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw-*.so
%{_libdir}/libdw.so.*
%dir %{_libdir}/elfutils
%{_libdir}/elfutils/lib*.so

%files devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libebl.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/version.h
%{_libdir}/libebl.a
%{_libdir}/libasm.so
%{_libdir}/libdw.so
%{_libdir}/pkgconfig/libdw.pc

%files devel-static
%defattr(-,root,root)
%{_libdir}/libasm.a
%{_libdir}/libdw.a

%files libelf
%defattr(-,root,root)
%{_libdir}/libelf-*.so
%{_libdir}/libelf.so.*

%files libelf-devel
%defattr(-,root,root)
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_libdir}/libelf.so
%{_libdir}/pkgconfig/libelf.pc

%files libelf-devel-static
%defattr(-,root,root)
%{_libdir}/libelf.a
