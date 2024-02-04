%global module pikepdf

%bcond_with	doc
%bcond_with	test

Summary:	Read and write PDFs with Python, powered by qpdf
Name:		python-%{module}
Version:	8.12.0
Release:	1
Group:		Development/Python
License:	MPLv2.0
URL:		https://github.com/pikepdf/pikepdf
Source0:	https://pypi.io/packages/source/p/%{module}/%{module}-%{version}.tar.gz

BuildRequires:	pkgconfig(libqpdf)
BuildRequires:	pkgconfig(python)
BuildRequires:	pybind11-devel
#BuildRequires:  python%{pyver}dist(backcall)
#BuildRequires:  python%{pyver}dist(decorator)
BuildRequires:  python%{pyver}dist(ipython-genutils)
BuildRequires:	python%{pyver}dist(lxml)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(pybind11)
BuildRequires:	python%{pyver}dist(pythran)
#BuildRequires:  python%{pyver}dist(pickleshare)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	python%{pyver}dist(scipy)
%if %{with doc}
BuildRequires:  python%{pyver}dist(sphinx)
%endif
#BuildRequires:  python%{pyver}dist(traitlets)
BuildRequires:	python%{pyver}dist(wheel)

# Tests:
%if %{with test}
BuildRequires:	poppler
BuildRequires:	python%{pyver}dist(attrs) >= 20.2
BuildRequires:	python%{pyver}dist(hypothesis) >= 5
BuildRequires:	python%{pyver}dist(hypothesis) < 6
BuildRequires:	python%{pyver}dist(pillow) >= 7
BuildRequires:	python%{pyver}dist(psutil) >= 5
BuildRequires:	python%{pyver}dist(pytest) >= 6
BuildRequires:	python%{pyver}dist(pytest) < 7
BuildRequires:	python%{pyver}dist(pytest-runner)
BuildRequires:	python%{pyver}dist(pytest-timeout) >= 1.4.2
BuildRequires:	python%{pyver}dist(pytest-xdist) >= 1.28
BuildRequires:	python%{pyver}dist(pytest-xdist) < 3
BuildRequires:	python%{pyver}dist(python-xmp-toolkit) >= 2.0.1
%endif

#{?python_provide:%python_provide python3-%{module}}

%description
pikepdf is a Python library for reading and writing PDF files. pikepdf is
based on QPDF, a powerful PDF manipulation and repair library.

%files
%license LICENSE.txt
%doc README.md
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}-%{version}*-info/

#----------------------------------------------------------------------------

%if %{with doc}
%package -n %{name}-doc
Summary:	pikepdf documentation
Group:		Documentation
BuildRequires:	python%{pyver}dist(sphinx) >= 1.4
BuildRequires:	python%{pyver}dist(sphinx-rtd-theme)
BuildRequires:	python%{pyver}dist(pillow) >= 7
BuildRequires:	python%{pyver}dist(matplotlib)
BuildRequires:	ipython

%description -n	%{name}-doc
Documentation for pikepdf.

%files -n %{name}-doc
%license LICENSE.txt
%doc html
%endif

#----------------------------------------------------------------------------

%prep
%autosetup -n %{module}-%{version} -p1

# Remove bundled egg-info
rm -rf src/%{module}*-info

# We don't build docs against the installed version, so force the version.
sed -i -e "s/release = .\+/release = '%{version}'/g" docs/conf.py

%build
%py_build

# generate html docs
%if %{with doc}
export PYTHONPATH="$PWD/build/lib.linux-%{_arch}-cpython-%{python3_version_nodots}"
pushd docs
sphinx-build . ../html
popd
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py_install

# ensure .so modules are executable for proper -debuginfo extraction
chmod a+rx %{buildroot}%{python_sitearch}/%{module}/*.so

