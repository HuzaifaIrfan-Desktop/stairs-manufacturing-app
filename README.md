# stairs_app
Wooden Stairs Computer Aided Manufacturing App - QT Based Desktop App, Drawings (DXF/PDF), Cut Lists (PDF) , and CNC CAM (G-Code )


## Conda Environment Setup

```sh
mamba create --name stairs_app_env --file environment.yml
```

[New ENV Setup](env.md)

```sh
conda activate stairs_app_env
```

## Run

```sh
python main.py
```

## Build

```sh
pyinstaller windows-app.spec
```
