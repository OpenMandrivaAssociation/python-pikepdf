%define debug_package %{nil}

%bcond_with test

%define module	pikepdf

Name:		python-%{module}
Version:	6.2.6
Release:	3
Summary:	Read and write PDFs with Python, powered by qpdf
Group:		Development/Python
License:	MPLv2.0
URL:		https://github.com/pikepdf/pikepdf
Source0:	https://pypi.io/packages/source/p/%{module}/%{module}-%{version}.tar.gz
#Patch1:		0001-Relax-some-requirements.patch

BuildRequires:	pkgconfig(libqpdf)
BuildRequires:	pkgconfig(python)
BuildRequires:	pybind11-devel
BuildRequires:	python3dist(lxml) >= 4
BuildRequires:	python3dist(pybind11)
BuildRequires:	python3dist(setuptools)
BuildRequires:	python3dist(setuptools-scm)
#BuildRequires:	python3dist(setuptools-scm[toml]) >= 4.1
BuildRequires:	python3dist(setuptools-scm-git-archive)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(traitlets)
BuildRequires:  python3dist(ipython-genutils)
BuildRequires:  python3dist(decorator)
BuildRequires:  python3dist(pickleshare)
BuildRequires:  python3dist(backcall)
BuildRequires: python-wheel
BuildRequires: python-pip

# Tests:
%if %{with test}
BuildRequires:	poppler
BuildRequires:	python3dist(attrs) >= 20.2
BuildRequires:	python3dist(hypothesis) >= 5
BuildRequires:	python3dist(hypothesis) < 6
BuildRequires:	python3dist(pillow) >= 7
BuildRequires:	python3dist(psutil) >= 5
BuildRequires:	python3dist(pytest) >= 6
BuildRequires:	python3dist(pytest) < 7
BuildRequires:	python3dist(pytest-runner)
BuildRequires:	python3dist(pytest-timeout) >= 1.4.2
BuildRequires:	python3dist(pytest-xdist) >= 1.28
BuildRequires:	python3dist(pytest-xdist) < 3
BuildRequires:	python3dist(python-xmp-toolkit) >= 2.0.1
%endif

%{?python_provide:%python_provide python3-%{module}}

%description
pikepdf is a Python library for reading and writing PDF files. pikepdf is
based on QPDF, a powerful PDF manipulation and repair library.


#package -n	python-%{module}-doc
#Summary:	pikepdf documentation
#Group:		Documentation
#BuildRequires:	python3dist(sphinx) >= 1.4
#BuildRequires:	python3dist(sphinx-rtd-theme)
#BuildRequires:	python3dist(pillow) >= 7
#BuildRequires:	python3dist(matplotlib)
#BuildRequires:	ipython
#
#description -n	python-%{module}-doc
#Documentation for pikepdf.

%prep
%autosetup -n %{module}-%{version} -p1

# Remove bundled egg-info
rm -rf src/%{module}.egg-info

# We don't build docs against the installed version, so force the version.
sed -i -e "s/release = .\+/release = '%{version}'/g" docs/conf.py

%build
%py_build

# generate html docs
#pushd docs
#PYTHONPATH=$(ls -d ${PWD}/../build/lib*) sphinx-build . ../html
#popd
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
%py_install

# ensure .so modules are executable for proper -debuginfo extraction
chmod a+rx %{buildroot}%{python_sitearch}/%{module}/*.so


%files
%license LICENSE.txt
%doc README.md
%{python_sitearch}/%{module}/
%{python_sitearch}/%{module}*.dist-info

#files -n python-%{module}-doc
#doc html
#license LICENSE.txt
