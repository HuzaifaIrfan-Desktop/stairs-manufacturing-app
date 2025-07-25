<div align="center">
  <h1>Stairs App</h1>
  <p><h3 align="center">Wooden Stairs Computer Aided Manufacturing App - QT Based Desktop App, Drawings (DXF/PDF), Cut Lists (PDF) , and CNC CAM (G-Code) 🚀</h3></p>
</div>


•[stairs_app-v_0_1_1.zip](https://www.dropbox.com/scl/fi/xw6l0cs4n27cywsw9sdpo/stairs_app-v_0_1_1.zip?rlkey=g90mzfz23nyinukjzymnkp4fg&st=adue9u1o&dl=0)

<hr>

## Demo Video

[![Demo Video](https://img.youtube.com/vi/zCyjUjtQt80/0.jpg)](https://www.youtube.com/watch?v=zCyjUjtQt80)


![overview](overview.drawio.png)


## Conda Installation

- Install Miniforge and Add to Path
- https://conda-forge.org/download/


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

## Sign the EXE

```sh
signtool sign /a /fd SHA256 /td SHA256 /tr http://timestamp.digicert.com stairs_app.exe
```



## 🤝🏻 &nbsp;Connect with Me

<p align="center">
<a href="https://www.huzaifairfan.com"><img src="https://img.shields.io/badge/-huzaifairfan.com-1aa260?style=flat&logo=Google-Chrome&logoColor=white"/></a>
<a href="https://github.com/HuzaifaIrfan/"><img src="https://img.shields.io/badge/-Github-4078c0?style=flat&logo=Github&logoColor=white"/></a>
<a href="mailto:hi@huzaifairfan.com"><img src="https://img.shields.io/badge/-hi@huzaifairfan.com-c71610?style=flat&logo=Gmail&logoColor=white"/></a>
<a href="https://www.upwork.com/freelancers/huzaifairfan2001"><img src="https://img.shields.io/badge/-Upwork-14a800?style=flat&logo=Upwork&logoColor=white"/></a>
</p>

## License

Licensed under the MIT License, Copyright 2025 Huzaifa Irfan. [LICENSE](LICENSE)