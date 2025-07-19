


## New Conda Env Setup

```sh
conda create -n stairs_app_env python=3.12
```
```sh
conda activate stairs_app_env
```

### Install Libs

```sh
conda install -c conda-forge pyside6 pythonocc-core cadquery pydantic pydantic-settings
```

```sh
conda install -c conda-forge PyInstaller
```

```sh
conda install lxml cairosvg ezdxf
```

```sh
conda install pymupdf
```

### Not available in conda forge win-64
```sh
pip install pymupdf
```

## Export Conda Env Setup

```sh
conda env export > environment.yml
```
