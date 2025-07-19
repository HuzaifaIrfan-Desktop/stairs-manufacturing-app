


## New Conda Env Setup

```sh
conda create -n stairs_app_env python=3.12
```

```sh
conda activate stairs_app_env
```

### Install Libs


```sh
mamba install -c conda-forge cadquery pythonocc-core lxml cairosvg ezdxf pyside6 jupyterlab pydantic pydantic-settings 
```


```sh
mamba install -c conda-forge PyInstaller
```


## Export Conda Env Setup

```sh
mamba env export > environment.yml
```
