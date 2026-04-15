# RGB LED

Ce dossier regroupe les modules RGB pour Pico.

<img src="https://europe1.discourse-cdn.com/arduino/original/4X/e/7/6/e76bc03f40852645e65379a0969876e46ddf2397.png" alt="Illustration RGB LED" width="220" align="left">

## Vue d'ensemble

- Meme materiel de base: LED RGB pilotee par PWM.
- Le code present actuellement est axe sur un fondu de couleurs continu.
- Si plusieurs variantes sont ajoutees plus tard, elles pourront etre regroupees ici.

## Variantes disponibles

- **RGB Fade Pico2W**: animation de fondu de couleurs en continu.

## Conseil rapide

Commencez par verifier le cablage des broches R, G, B, puis ajustez `COMMON_ANODE` et `STEP_DELAY_MS` selon votre montage.

