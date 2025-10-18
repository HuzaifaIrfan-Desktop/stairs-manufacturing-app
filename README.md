# Stairs Manufacturing App
**`Wooden Stairs Computer Aided Manufacturing App - QT Based Desktop App, Drawings (DXF/PDF), Cut Lists (PDF) , and CNC CAM (G-Code) 🚀`**

<!-- •[Link](#)

<hr>

## 🎬 Demo

[![Demo](https://img.youtube.com/vi/video_id/0.jpg)](https://www.youtube.com/watch?v=video_id)

![overview](overview.drawio.png)

-->


# 📦 Release
- [v0.2.0](https://github.com/HuzaifaIrfan-CADCAM/stairs_app/releases)




<hr>


## 🎬 Demo

[▶️![Demo](https://img.youtube.com/vi/phJr-eCjHw4/hqdefault.jpg)](https://www.youtube.com/watch?v=phJr-eCjHw4)



![overview](docs/overview.drawio.png)

![code_structure](docs/code_structure.drawio.png)






# 🛠️ Development

## Target
- Linux/Windows Desktop (x86_64)

## Development Environment
- **OS**: Ubuntu 24.04 (x86_64)
- **IDE**: Visual Studio Code
- **Framework**: pyside6

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


## Build

```sh
pyinstaller windows-app.spec
```

## Sign the EXE

```sh
signtool sign /a /fd SHA256 /td SHA256 /tr http://timestamp.digicert.com stairs_app.exe
```


# 🚀 Usage

## Run

```sh
python main.py
```



# 📝 Documentation

# 📚 References



# 🤝🏻 Connect with Me

## Huzaifa Irfan

- 💬 Just want to say hi?
- 🚀 Have a project to discuss?
- 📧 Email me @: [hi@huzaifairfan.com](mailto:hi@huzaifairfan.com)
- 📞 Visit my Profile for other channels:

[![GitHub](https://img.shields.io/badge/Github-%23222.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/HuzaifaIrfan/)
[![Website](https://img.shields.io/badge/Website-%23222.svg?style=for-the-badge&logo=google-chrome&logoColor==%234285F4)](https://www.huzaifairfan.com)

# 📜 License

Licensed under the GPL3 License, Copyright 2025 Huzaifa Irfan. [LICENSE](LICENSE)
<hr />
Last Updated on 2025-07-28
