# bikeGAN

this is the fork of [bicycleGAN](https://junyanz.github.io/BicycleGAN/) which is used to train and run GANs for [frankenGAN](http://geometry.cs.ucl.ac.uk/projects/2018/frankengan). the interactive system which uses these networks is [chordatlas](https://github.com/twak/chordatlas).

## running

requirements: 
* nvidia GPU (CUDA 8+)
* pytorch 1.4
* visdom
* dominate

the entry point is `test_interactive.py` which listens to the `./input` folders for new inputs, and writes them to `./output` (these folders should exist). it will download the [pre-trained model weights](http://geometry.cs.ucl.ac.uk/projects/2018/frankengan/data/franken_nets/) the first time your run it. Once it is running, set [chordatlas](https://github.com/twak/chordatlas)'s bikeGAN file location (in the settings menu) to the bikeGAN root directory (the one containing this file).

alternatively, use the [docker container](https://hub.docker.com/r/twak/bikegan/) with [nvidia-docker](https://github.com/NVIDIA/nvidia-docker):

```nvidia-docker run -v $(pwd)/input:/home/user/bikegan/input -v $(pwd)/output:/home/user/bikegan/output -it --rm twak/bikegan```

## cite

if you use this project, please cite [frankenGAN](https://arxiv.org/abs/1806.07179)

```
@misc{frankenGAN,
  Author = {Tom Kelly and Paul Guerrero and Anthony Steed and Peter Wonka and Niloy J. Mitra},
  Title = {FrankenGAN: Guided Detail Synthesis for Building Mass-Models Using Style-Synchonized GANs},
  Year = {2018},
  Eprint = {arXiv:1806.07179},
}
```

