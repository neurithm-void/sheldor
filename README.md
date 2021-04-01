# SHELDOR : The Conqueror

A text generator based on dialogs of Sheldon Copper, from The Big Bang Theory.

Each branch contains different experiments. 

## Experiment 1
Train Vanilla BLSTM model with input as a other charachter's dialog and out should be sheldon's dialog. (No context storing in text generation).

Checkpoints
- create a csv file containing dataset.
    - [] input will be any character dialog and output should be sheldon's dialog.
    - [] clean the dataset, remove all spacing char and unuseful symbols.
    - [] For encoding, use GLoVe 100b vectors, later initialize unk symbols vector by taking random mean. 
- [] create a preprocessing pipeline.


