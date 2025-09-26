#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SILNIK FRAKTALA MANDELBROTA
===========================

Klasa odpowiedzialna za generowanie fraktala Mandelbrota z możliwością:
- Nieskończonego powiększania
- Optymalizacji wydajności
- Dynamicznej zmiany jakości
- Płynnej nawigacji

Matematyka:
Fraktal Mandelbrota to zbiór punktów c w płaszczyźnie zespolonej,
dla których funkcja f(z) = z² + c nie diverguje dla z₀ = 0.

Autor: AI Assistant  
Data: 2025
"""

import numpy as np
import numba
from typing import Tuple, Optional

# Kompilacja JIT dla maksymalnej wydajności
@numba.jit(nopython=True, parallel=True, fastmath=True)
def mandelbrot_calculation(height: int, width: int, 
                          x_min: float, x_max: float,
                          y_min: float, y_max: float,
                          max_iter: int) -> np.ndarray:
    """
    Szybkie obliczenie fraktala Mandelbrota z optymalizacją Numba
    
    Args:
        height, width: Wymiary obrazu
        x_min, x_max, y_min, y_max: Zakres płaszczyzny zespolonej
        max_iter: Maksymalna liczba iteracji
        
    Returns:
        Tablica 2D z liczbą iteracji dla każdego punktu
    """
    result = np.zeros((height, width), dtype=np.int32)
    
    # Obliczenia równoległe dla każdego piksela
    for i in numba.prange(height):
        for j in numba.prange(width):
            # Mapowanie pikseli na płaszczyznę zespoloną
            x = x_min + (x_max - x_min) * j / (width - 1)
            y = y_min + (y_max - y_min) * i / (height - 1)
            
            c = complex(x, y)
            z = complex(0, 0)
            
            # Iteracje Mandelbrota z optymalizacjami
            for n in range(max_iter):
                if abs(z) > 2.0:  # Warunek dywergencji
                    result[i, j] = n
                    break
                    
                # Główne równanie z² + c
                z = z * z + c
                
                # Dodatkowa optymalizacja dla sprawdzania okresowości
                if n > 20 and abs(z) < 1e-10:
                    result[i, j] = max_iter
                    break
            else:
                result[i, j] = max_iter
                
    return result

@numba.jit(nopython=True, fastmath=True)
def smooth_coloring(iterations: int, z: complex, max_iter: int) -> float:
    """
    Płynne kolorowanie fraktala dla lepszego wyglądu
    
    Args:
        iterations: Liczba iteracji
        z: Ostatnia wartość z
        max_iter: Maksymalna liczba iteracji
        
    Returns:
        Płynna wartość koloru
    """
    if iterations < max_iter:
        # Algorytm płynnego kolorowania
        smooth = iterations + 1 - np.log2(np.log2(abs(z)))
        return smooth
    return iterations

class MandelbrotEngine:
    """Silnik generowania fraktala Mandelbrota"""
    
    def __init__(self, width: int, height: int):
        """
        Inicjalizacja silnika fraktala
        
        Args:
            width, height: Wymiary obrazu w pikselach
        """
        self.width = width
        self.height = height
        
        # Parametry matematyczne
        self.x_center = -0.5  # Środek w osi X
        self.y_center = 0.0   # Środek w osi Y  
        self.zoom = 1.0       # Poziom powiększenia
        self.aspect_ratio = width / height
        
        # Jakość renderowania
        self.max_iter = 100   # Maksymalne iteracje
        self.min_iter = 50    # Minimalne iteracje
        self.max_max_iter = 2000  # Maksymalne dozwolone iteracje
        
        # Cache dla optymalizacji
        self.last_params = None
        self.cached_result = None
        
        # Statystyki
        self.render_count = 0
        self.total_pixels = width * height
        
        print(f"🔧 Silnik Mandelbrota: {width}x{height}, jakość: {self.max_iter} iteracji")
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Oblicz granice obszaru renderowania
        
        Returns:
            Tuple (x_min, x_max, y_min, y_max)
        """
        # Szerokość i wysokość obszaru w płaszczyźnie zespolonej
        view_width = 3.0 / self.zoom
        view_height = view_width / self.aspect_ratio
        
        x_min = self.x_center - view_width / 2
        x_max = self.x_center + view_width / 2
        y_min = self.y_center - view_height / 2
        y_max = self.y_center + view_height / 2
        
        return x_min, x_max, y_min, y_max
    
    def adaptive_iterations(self, zoom: float) -> int:
        """
        Dynamicznie dostosuj liczbę iteracji do poziomu zoomu
        
        Args:
            zoom: Poziom powiększenia
            
        Returns:
            Optymalną liczbę iteracji
        """
        # Więcej iteracji dla większego zoomu
        iter_count = int(self.min_iter + np.log10(zoom + 1) * 30)
        return min(iter_count, self.max_max_iter)
    
    def generate(self) -> np.ndarray:
        """
        Generuj fraktal Mandelbrota
        
        Returns:
            Tablica 2D z wartościami iteracji
        """
        # Aktualne parametry
        current_params = (self.x_center, self.y_center, self.zoom, 
                         self.width, self.height, self.max_iter)
        
        # Sprawdź cache
        if current_params == self.last_params and self.cached_result is not None:
            return self.cached_result
        
        # Oblicz granice
        x_min, x_max, y_min, y_max = self.get_bounds()
        
        # Adaptacyjne iteracje
        adaptive_iter = self.adaptive_iterations(self.zoom)
        actual_iter = min(self.max_iter, adaptive_iter)
        
        print(f"🎯 Renderowanie: zoom={self.zoom:.2e}, iteracje={actual_iter}, "
              f"obszar=({x_min:.6f}, {y_min:.6f}) do ({x_max:.6f}, {y_max:.6f})")
        
        # Główne obliczenia
        result = mandelbrot_calculation(
            self.height, self.width,
            x_min, x_max, y_min, y_max,
            actual_iter
        )
        
        # Cache wyników
        self.last_params = current_params
        self.cached_result = result.copy()
        
        self.render_count += 1
        
        # Statystyki wydajności
        pixels_in_set = np.sum(result == actual_iter)
        pixels_outside = self.total_pixels - pixels_in_set
        
        if self.render_count % 5 == 0:  # Co 5 renderowań
            print(f"📊 Render #{self.render_count}: "
                  f"{pixels_in_set} pikseli w zbiorze, "
                  f"{pixels_outside} na zewnątrz")
        
        return result
    
    def zoom_at_point(self, screen_x: int, screen_y: int, zoom_factor: float):
        """
        Powiększ/pomniejsz fraktal w określonym punkcie
        
        Args:
            screen_x, screen_y: Współrzędne ekranowe punktu
            zoom_factor: Współczynnik powiększenia (>1 = zoom in, <1 = zoom out)
        """
        # Konwersja współrzędnych ekranowych na matematyczne
        x_min, x_max, y_min, y_max = self.get_bounds()
        
        math_x = x_min + (x_max - x_min) * screen_x / self.width
        math_y = y_min + (y_max - y_min) * screen_y / self.height
        
        # Przemieść środek do punktu kliknięcia przed zoomem
        self.x_center = math_x
        self.y_center = math_y
        
        # Zastosuj zoom
        old_zoom = self.zoom
        self.zoom *= zoom_factor
        
        # Zabezpieczenie przed zbyt dużym zoomem (limit numeryczny)
        max_zoom = 1e15
        if self.zoom > max_zoom:
            self.zoom = max_zoom
            print(f"⚠️  Osiągnięto maksymalny zoom: {max_zoom:.2e}")
        
        if self.zoom < 0.1:
            self.zoom = 0.1
            
        # Logowanie zoomu co większe zmiany
        if abs(np.log10(self.zoom) - np.log10(old_zoom)) > 1:
            print(f"🔍 Zoom: {old_zoom:.2e} → {self.zoom:.2e} "
                  f"w punkcie ({math_x:.6f}, {math_y:.6f})")
    
    def pan(self, dx: int, dy: int):
        """
        Przesuń widok fraktala
        
        Args:
            dx, dy: Przesunięcie w pikselach
        """
        x_min, x_max, y_min, y_max = self.get_bounds()
        
        # Konwersja pikseli na jednostki matematyczne
        pixel_width = (x_max - x_min) / self.width
        pixel_height = (y_max - y_min) / self.height
        
        self.x_center += dx * pixel_width
        self.y_center += dy * pixel_height
    
    def reset_view(self):
        """Reset widoku do domyślnych wartości"""
        print("🔄 Reset widoku do domyślnego")
        self.x_center = -0.5
        self.y_center = 0.0  
        self.zoom = 1.0
        self.max_iter = 100
        
        # Wyczyść cache
        self.last_params = None
        self.cached_result = None
    
    def resize(self, width: int, height: int):
        """
        Zmień rozmiar renderowania
        
        Args:
            width, height: Nowe wymiary
        """
        old_aspect = self.aspect_ratio
        
        self.width = width
        self.height = height
        self.aspect_ratio = width / height
        self.total_pixels = width * height
        
        # Wyczyść cache przy zmianie rozmiaru
        self.last_params = None
        self.cached_result = None
        
        print(f"📐 Zmiana rozmiaru: {width}x{height}, "
              f"ratio: {old_aspect:.3f} → {self.aspect_ratio:.3f}")
    
    def increase_iterations(self, factor: int = 50):
        """Zwiększ jakość renderowania"""
        self.max_iter = min(self.max_iter + factor, self.max_max_iter)
        print(f"⬆️  Jakość: {self.max_iter} iteracji")
        
        # Wyczyść cache
        self.last_params = None
        self.cached_result = None
    
    def decrease_iterations(self, factor: int = 50):
        """Zmniejsz jakość renderowania"""
        self.max_iter = max(self.max_iter - factor, self.min_iter)
        print(f"⬇️  Jakość: {self.max_iter} iteracji")
        
        # Wyczyść cache
        self.last_params = None
        self.cached_result = None
    
    def get_info(self) -> dict:
        """
        Pobierz informacje o aktualnym stanie silnika
        
        Returns:
            Słownik z informacjami
        """
        x_min, x_max, y_min, y_max = self.get_bounds()
        
        return {
            'center': (self.x_center, self.y_center),
            'zoom': self.zoom,
            'bounds': (x_min, x_max, y_min, y_max),
            'iterations': self.max_iter,
            'dimensions': (self.width, self.height),
            'renders': self.render_count,
            'total_pixels': self.total_pixels
        }
