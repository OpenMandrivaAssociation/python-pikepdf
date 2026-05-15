# nanobind baked in build options dont produce debuginfo
%define _debugsource_template %{nil}
%define module pikepdf

%bcond doc 0
%bcond test 0

Summary:	Read and write PDFs with Python, powered by qpdf
Name:		python-pikepdf
Version:	10.6.0
Release:	1
Group:		Development/Python
License:	MPL-2.0
URL:		https://github.com/pikepdf/pikepdf
Source0:	%{URL}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildSystem:	python
BuildRequires:	cmake
BuildRequires:	clang-tools
BuildRequires:	pkgconfig(libqpdf)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(lxml)
BuildRequires:	python%{pyver}dist(nanobind)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pythran)
BuildRequires:	python%{pyver}dist(scikit-build-core)
BuildRequires:	python%{pyver}dist(scipy)
BuildRequires:	python%{pyver}dist(wheel)
%if %{with doc}
BuildRequires:	python%{pyver}dist(myst-parser)
BuildRequires:  python%{pyver}dist(sphinx)
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)
%endif
%if %{with test}
BuildRequires:	poppler
BuildRequires:	python%{pyver}dist(attrs) >= 20.2
BuildRequires:	python%{pyver}dist(hypothesis) >= 6.36
BuildRequires:	python%{pyver}dist(numpy) >= 1.21.0
BuildRequires:	python%{pyver}dist(pillow) >= 10.0.1
BuildRequires:	python%{pyver}dist(psutil) >= 5
BuildRequires:	python%{pyver}dist(pytest) >= 6.2.5
BuildRequires:	python%{pyver}dist(pytest-timeout) >= 2.1.0
BuildRequires:	python%{pyver}dist(pytest-xdist) >= 2.5.0
BuildRequires:	python%{pyver}dist(python-xmp-toolkit) >= 2.0.1
%endif

%description
pikepdf is a Python library for reading and writing PDF files. pikepdf is
based on QPDF, a powerful PDF manipulation and repair library.

%if %{with doc}
%package -n %{name}-doc
Summary:	pikepdf documentation
Group:		Documentation

%description -n	%{name}-doc
Documentation for pikepdf.
%endif

%if %{with doc}
%prep -a
# We don't build docs against the installed version, so force the version.
sed -i -e "s/release = .\+/release = '%{version}'/g" docs/conf.py
%endif

%build -p
export LDFLAGS="%{ldflags} -lpython%{pyver}"

# generate html docs
%if %{with doc}
%build -a
export PYTHONPATH="$PWD/build/lib.linux-%{_arch}-cpython-%{python3_version_nodots}"
pushd docs
sphinx-build . ../html
popd
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install -a
# ensure .so modules are executable for proper -debuginfo extraction
chmod a+rx %{buildroot}%{python_sitearch}/%{module}/*.so

%files
%license LICENSE.txt
%doc README.md
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}-%{version}*-info/

%if %{with doc}
%files -n %{name}-doc
%license LICENSE.txt
%doc html
%endif
