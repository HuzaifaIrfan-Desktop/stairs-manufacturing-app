# stairs_app
Wooden Stairs Computer Aided Manufacturing App - QT Based Desktop App, Drawings (DXF/PDF), Cut Lists (PDF) , and CNC CAM (G-Code )


## Conda Environment Setup
### Windows
```sh
mamba create --name stairs_app_env --file windows-environment.yml
```
### Linux
```sh
mamba create --name stairs_app_env --file linux-environment.yml
```

[New ENV Setup](env.md)

```sh
conda activate stairs_app_env
```

## Build

```sh
pyinstaller windows-app.spec
```

## Run

```sh
python main.py
```