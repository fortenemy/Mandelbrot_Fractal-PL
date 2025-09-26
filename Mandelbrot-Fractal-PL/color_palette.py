#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SYSTEM KOLOROWANIA FRAKTALI
============================

Klasa odpowiedzialna za piękne, wielokolorowe renderowanie fraktali:
- Różne palety kolorów
- Płynne przejścia
- Dynamiczne efekty
- Optymalizacja kolorów

Zawiera algorytmy kolorowania takie jak:
- HSV rainbow
- Ocean waves
- Fire/magma
- Electric plasma
- Cosmic nebula

Autor: AI Assistant
Data: 2025
"""

import numpy as np
from typing import Tuple, List, Optional
from enum import Enum
import colorsys

class PaletteType(Enum):
    """Typy dostępnych palet kolorów"""
    RAINBOW = "Rainbow"
    OCEAN = "Ocean Waves"  
    FIRE = "Fire & Magma"
    ELECTRIC = "Electric Plasma"
    COSMIC = "Cosmic Nebula"
    VINTAGE = "Vintage Sepia"
    NEON = "Neon Dreams"
    ICE = "Ice Crystal"
    SUNSET = "Sunset Glow"
    MATRIX = "Matrix Code"

class ColorPalette:
    """Generator palet kolorów dla fraktali"""
    
    def __init__(self):
        """Inicjalizacja systemu kolorowania"""
        self.palettes = list(PaletteType)
        self.current_palette_index = 0
        self.current_palette = self.palettes[0]
        
        # Cache kolorów dla wydajności
        self.color_cache = {}
        self.cache_size = 1000
        
        # Parametry animacji
        self.animation_time = 0.0
        self.animation_speed = 0.02
        
        print(f"🎨 System kolorowania: {len(self.palettes)} palet dostępnych")
    
    @property
    def current_palette_name(self) -> str:
        """Nazwa aktualnej palety"""
        return self.current_palette.value
    
    def next_palette(self):
        """Przełącz na następną paletę"""
        self.current_palette_index = (self.current_palette_index + 1) % len(self.palettes)
        self.current_palette = self.palettes[self.current_palette_index]
        
        # Wyczyść cache przy zmianie palety
        self.color_cache.clear()
        
        print(f"🎨 Paleta: {self.current_palette_name}")
    
    def hsv_to_rgb(self, h: float, s: float, v: float) -> Tuple[int, int, int]:
        """
        Konwersja HSV na RGB
        
        Args:
            h: Hue (0-1)
            s: Saturation (0-1) 
            v: Value (0-1)
            
        Returns:
            RGB tuple (0-255)
        """
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def rainbow_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """
        Paleta tęczowa - klasyczne kolorowanie
        
        Args:
            t: Parametr koloru (0-1)
            intensity: Intensywność (0-1)
            
        Returns:
            RGB color tuple
        """
        # Animowana tęcza
        hue = (t * 6.0 + self.animation_time) % 1.0
        saturation = 0.8 + 0.2 * np.sin(t * np.pi * 4 + self.animation_time * 2)
        value = intensity * (0.5 + 0.5 * np.sin(t * np.pi * 2))
        
        return self.hsv_to_rgb(hue, saturation, value)
    
    def ocean_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """
        Paleta oceanu - błękity i zielenie
        
        Args:
            t: Parametr koloru (0-1)
            intensity: Intensywność (0-1)
            
        Returns:
            RGB color tuple
        """
        if t < 0.1:
            # Głęboki ocean - ciemne błękity
            blue = int(10 + t * 500 * intensity)
            green = int(5 + t * 300 * intensity)
            red = 0
        elif t < 0.6:
            # Średnie głębokości - błękity i turkusy
            wave = np.sin(t * np.pi * 8 + self.animation_time * 3)
            blue = int(50 + (t - 0.1) * 400 * intensity + wave * 30)
            green = int(30 + (t - 0.1) * 300 * intensity + wave * 40)
            red = int(wave * 20)
        else:
            # Płytkie wody - jasne turkusy
            foam = np.sin(t * np.pi * 16 + self.animation_time * 5)
            blue = int(150 + (t - 0.6) * 200 + foam * 50)
            green = int(200 + (t - 0.6) * 50 + foam * 30)
            red = int(100 + foam * 40)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def fire_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """
        Paleta ognia - czerwienie, pomarańcze, żółcie
        
        Args:
            t: Parametr koloru (0-1)
            intensity: Intensywność (0-1)
            
        Returns:
            RGB color tuple
        """
        # Animowane płomienie
        flicker = np.sin(t * np.pi * 12 + self.animation_time * 8) * 0.1
        adjusted_t = max(0, min(1, t + flicker))
        
        if adjusted_t < 0.2:
            # Ciemne czerwienie - żar
            red = int(20 + adjusted_t * 600 * intensity)
            green = int(adjusted_t * 100 * intensity)
            blue = 0
        elif adjusted_t < 0.5:
            # Jasne czerwienie do pomarańczy
            red = int(120 + (adjusted_t - 0.2) * 400 * intensity)
            green = int(20 + (adjusted_t - 0.2) * 600 * intensity)
            blue = int((adjusted_t - 0.2) * 100 * intensity)
        elif adjusted_t < 0.8:
            # Pomarańcz do żółci
            red = int(200 + (adjusted_t - 0.5) * 150 * intensity)
            green = int(120 + (adjusted_t - 0.5) * 400 * intensity)
            blue = int(30 + (adjusted_t - 0.5) * 200 * intensity)
        else:
            # Jasne żółcie i biele
            red = 255
            green = int(220 + (adjusted_t - 0.8) * 175 * intensity)
            blue = int(60 + (adjusted_t - 0.8) * 700 * intensity)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def electric_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """
        Paleta elektryczna - neonowe błękity i fiolety
        
        Args:
            t: Parametr koloru (0-1)
            intensity: Intensywność (0-1)
            
        Returns:
            RGB color tuple
        """
        # Pulsujące wyładowania
        pulse = np.sin(t * np.pi * 6 + self.animation_time * 10) * 0.3
        spark = np.sin(t * np.pi * 20 + self.animation_time * 15) * 0.1
        
        base_hue = 0.6 + t * 0.3 + pulse * 0.1  # Błękity do fioletów
        saturation = 0.9 + spark * 0.1
        value = intensity * (0.3 + 0.7 * t + pulse * 0.3)
        
        return self.hsv_to_rgb(base_hue % 1.0, min(1.0, saturation), min(1.0, value))
    
    def cosmic_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """
        Paleta kosmiczna - głębokie fiolety, różowe i złote
        
        Args:
            t: Parametr koloru (0-1)
            intensity: Intensywność (0-1)
            
        Returns:
            RGB color tuple
        """
        # Gwiezdna mgławica
        swirl = np.sin(t * np.pi * 3 + self.animation_time * 2) * 0.2
        twinkle = np.sin(t * np.pi * 25 + self.animation_time * 12) * 0.1
        
        if t < 0.3:
            # Głęboka przestrzeń - ciemne fiolety
            red = int(20 + t * 200 * intensity + twinkle * 50)
            green = int(5 + t * 50 * intensity)
            blue = int(40 + t * 400 * intensity + swirl * 60)
        elif t < 0.7:
            # Mgławica - różowe i fioletowe
            red = int(60 + (t - 0.3) * 400 * intensity + swirl * 80)
            green = int(20 + (t - 0.3) * 200 * intensity + twinkle * 40)
            blue = int(120 + (t - 0.3) * 300 * intensity)
        else:
            # Gwiazdy - jasne złote i białe
            red = int(200 + (t - 0.7) * 180 * intensity)
            green = int(150 + (t - 0.7) * 300 * intensity)
            blue = int(50 + (t - 0.7) * 400 * intensity + twinkle * 100)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def vintage_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """Paleta vintage - sepie i brązy"""
        base = t * intensity
        red = int(100 + base * 120)
        green = int(80 + base * 100) 
        blue = int(50 + base * 60)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def neon_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """Paleta neonowa - jasne, nasycone kolory"""
        glow = np.sin(t * np.pi * 8 + self.animation_time * 6) * 0.2
        hue = (t * 0.8 + self.animation_time * 0.1) % 1.0
        
        return self.hsv_to_rgb(hue, 1.0, min(1.0, intensity * (0.7 + 0.3 * t + glow)))
    
    def ice_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """Paleta lodowa - błękity i biele"""
        crystal = np.sin(t * np.pi * 15 + self.animation_time * 4) * 0.1
        
        blue_base = 150 + t * 100 * intensity + crystal * 30
        red_base = 100 + t * 120 * intensity + crystal * 50
        green_base = 130 + t * 110 * intensity + crystal * 40
        
        return (max(0, min(255, int(red_base))), 
                max(0, min(255, int(green_base))),
                max(0, min(255, int(blue_base))))
    
    def sunset_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """Paleta zachodu słońca"""
        if t < 0.4:
            # Pomarańcze
            red = int(255 * intensity)
            green = int(120 + t * 300 * intensity)
            blue = int(30 + t * 100 * intensity)
        else:
            # Różowe do fioletów
            red = int(200 + (1-t) * 100 * intensity)
            green = int(50 + t * 150 * intensity)  
            blue = int(80 + t * 300 * intensity)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def matrix_color(self, t: float, intensity: float = 1.0) -> Tuple[int, int, int]:
        """Paleta Matrix - zielenie"""
        digital = np.sin(t * np.pi * 30 + self.animation_time * 20) * 0.2
        
        green = int(50 + t * 200 * intensity + digital * 50)
        red = int(t * 50 * intensity)
        blue = int(t * 30 * intensity)
        
        return max(0, min(255, red)), max(0, min(255, green)), max(0, min(255, blue))
    
    def get_color(self, iterations: int, max_iterations: int) -> Tuple[int, int, int]:
        """
        Pobierz kolor dla danej liczby iteracji
        
        Args:
            iterations: Liczba iteracji
            max_iterations: Maksymalna liczba iteracji
            
        Returns:
            RGB color tuple
        """
        # Sprawdź cache
        cache_key = (iterations, max_iterations, self.current_palette_index, 
                    int(self.animation_time * 100))
        
        if cache_key in self.color_cache:
            return self.color_cache[cache_key]
        
        # Oblicz parametr koloru
        if iterations >= max_iterations:
            # Punkt należy do zbioru Mandelbrota
            color = (0, 0, 0)  # Czarny
        else:
            # Normalizuj iteracje do zakresu 0-1
            t = iterations / max_iterations
            intensity = min(1.0, np.sqrt(t) * 1.2)
            
            # Wybierz funkcję kolorowania
            color_functions = {
                PaletteType.RAINBOW: self.rainbow_color,
                PaletteType.OCEAN: self.ocean_color,
                PaletteType.FIRE: self.fire_color,
                PaletteType.ELECTRIC: self.electric_color,
                PaletteType.COSMIC: self.cosmic_color,
                PaletteType.VINTAGE: self.vintage_color,
                PaletteType.NEON: self.neon_color,
                PaletteType.ICE: self.ice_color,
                PaletteType.SUNSET: self.sunset_color,
                PaletteType.MATRIX: self.matrix_color
            }
            
            color_func = color_functions.get(self.current_palette, self.rainbow_color)
            color = color_func(t, intensity)
        
        # Dodaj do cache (z limitem rozmiaru)
        if len(self.color_cache) < self.cache_size:
            self.color_cache[cache_key] = color
        
        return color
    
    def apply_colors(self, fractal_data: np.ndarray) -> np.ndarray:
        """
        Zastosuj kolory do danych fraktala
        
        Args:
            fractal_data: Tablica 2D z liczbą iteracji
            
        Returns:
            Tablica 3D RGB (height, width, 3)
        """
        height, width = fractal_data.shape
        colored_data = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Aktualizuj czas animacji
        self.animation_time += self.animation_speed
        if self.animation_time > 2 * np.pi:
            self.animation_time = 0.0
        
        # Znajdź maksymalną liczbę iteracji w danych
        max_iter = np.max(fractal_data)
        
        # Vectorized coloring dla wydajności
        unique_values = np.unique(fractal_data)
        color_map = {}
        
        for value in unique_values:
            color_map[value] = self.get_color(int(value), int(max_iter))
        
        # Zastosuj kolory
        for i in range(height):
            for j in range(width):
                iterations = fractal_data[i, j]
                colored_data[i, j] = color_map[iterations]
        
        return colored_data
    
    def get_palette_info(self) -> dict:
        """
        Informacje o aktualnej palecie
        
        Returns:
            Słownik z informacjami
        """
        return {
            'current_palette': self.current_palette_name,
            'palette_index': self.current_palette_index,
            'total_palettes': len(self.palettes),
            'animation_time': self.animation_time,
            'cache_size': len(self.color_cache)
        }
