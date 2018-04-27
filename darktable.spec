%define	_cmake_skip_rpath -DCMAKE_SKIP_RPATH:BOOL=OFF

# Keep libraries private
%if %{_use_internal_dependency_generator}
%define	__noautoprov '(.*)\\.so(.*)'
%define	__noautoreq 'libdarktable\\.so(.*)'
%endif

Summary:	Utility to organize and develop raw images
Name:		darktable
Version:	2.4.3
Release:	1
License:	GPLv3+
Group:		Graphics
Url:		http://www.darktable.org
Source0:	https://github.com/darktable-org/darktable/releases/download/release-%{version}/%{name}-%{version}.tar.xz
Source100:	%{name}.rpmlintrc
Patch0:		darktable-2.2.0-rpath.patch
BuildRequires:	cmake >= 3.0
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
BuildRequires:	libxml2-utils
# For OpenCL support
BuildRequires:	llvm >= 3.9.0
BuildRequires:	clang >= 3.9.0
BuildRequires:	po4a
BuildRequires:	xml2po
BuildRequires:	xsltproc
BuildRequires:	cups-devel
BuildRequires:	gettext-devel
BuildRequires:	gomp-devel
BuildRequires:	jpeg-devel
BuildRequires:	pugixml-devel >= 1.2
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(colord)
BuildRequires:	pkgconfig(colord-gtk)
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(exiv2) >= 0.23
BuildRequires:	pkgconfig(flickcurl)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.32
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gnome-keyring-1) >= 3.12.0
BuildRequires:	pkgconfig(GraphicsMagick)
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.12
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(lcms2)
BuildRequires:	pkgconfig(lensfun)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libglade-2.0)
BuildRequires:	pkgconfig(libgphoto2) >= 2.5
BuildRequires:	pkgconfig(libopenjpeg1) >= 1.5.0
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(librsvg-2.0)
BuildRequires:	pkgconfig(libsecret-1) >= 0.18
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libwebp) >= 0.3.0
BuildRequires:	pkgconfig(lua)
BuildRequires:	pkgconfig(OpenEXR)
#BuildRequires:	pkgconfig(osmgpsmap-1.0) >= 1.1.0
BuildRequires:	pkgconfig(pangocairo)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	python-jsonschema
Requires:	gphoto2

%description
Darktable is an open source photography workflow application and RAW developer.
A virtual lighttable and darkroom for photographers. It manages your digital
negatives in a database, lets you view them through a zoomable lighttable
and enables you to develop raw images and enhance them.

%files -f %{name}.lang
%doc doc/README* doc/TRANSLATORS*
%{_bindir}/%{name}*
%{_libdir}/%{name}
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}*
%{_mandir}/man1/%{name}*
%{_mandir}/*/man1/%{name}*

#----------------------------------------------------------------------------

%prep
%setup -q
%patch0 -p1

# Fix clang headers detection
sed -i 's|${LLVM_INSTALL_PREFIX}/lib/clang|${LLVM_INSTALL_PREFIX}/%{_lib}/clang|g' CMakeLists.txt


%build
# Now darktable seems to support lua 5.3, remove this:
# -DDONT_USE_INTERNAL_LUA=OFF
%cmake \
	-DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD:BOOLEAN=ON \
	-DPROJECT_VERSION:STRING="%{name}-%{EVRD}" \
	-DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
	-DUSE_GNOME_KEYRING:BOOLEAN=OFF

%make


%install
%makeinstall_std -C build
desktop-file-install --delete-original \
  --set-key="Exec" --set-value="%{name}" \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name}

# We use %%doc macro to pull needed docs
rm -rf %{buildroot}%{_datadir}/doc/%{name}

# Useless stuff making rpmlint complain
rm -rf %{buildroot}%{_datadir}/%{name}/lua/%{name}/external/pygy_require/.gitignore
