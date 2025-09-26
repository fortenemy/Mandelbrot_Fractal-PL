#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FRAKTAL MANDELBROTA - Interaktywna Aplikacja
============================================

Aplikacja pozwala na eksplorację fraktala Mandelbrota z możliwością:
- Nieskończonego powiększania (zoom)
- Poruszania się po fraktalu
- Wielokolorowego renderowania
- Płynnej animacji

Sterowanie:
- Mysz: Kliknij i przeciągnij aby się poruszać
- Scroll: Powiększanie/pomniejszanie
- Spacja: Reset widoku
- ESC: Wyjście z aplikacji

Autor: AI Assistant
Data: 2025
"""

import pygame
import sys
import threading
from fractal_engine import MandelbrotEngine
from color_palette import ColorPalette

class FractalApp:
    """Główna klasa aplikacji fraktala"""
    
    def __init__(self, width=1200, height=800):
        """Inicjalizacja aplikacji"""
        # Inicjalizacja Pygame
        pygame.init()
        
        # Ustawienia okna
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("🌈 Fraktal Mandelbrota - Nieskończona Eksploracja")
        
        # Ikona aplikacji (opcjonalna)
        self.setup_icon()
        
        # Silnik fraktala
        self.fractal_engine = MandelbrotEngine(width, height)
        self.color_palette = ColorPalette()
        
        # Stan aplikacji
        self.clock = pygame.time.Clock()
        self.running = True
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.rendering = False
        self.current_surface = None
        
        # Wątek renderowania
        self.render_thread = None
        self.render_lock = threading.Lock()
        
        # Informacje o wydajności
        self.fps = 0
        self.zoom_level = 1.0
        self.render_time = 0
        
        # Font dla UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
    def setup_icon(self):
        """Ustawienie ikony aplikacji"""
        try:
            # Tworzymy prostą ikonę 32x32
            icon_surface = pygame.Surface((32, 32))
            pygame.draw.circle(icon_surface, (255, 100, 200), (16, 16), 15)
            pygame.draw.circle(icon_surface, (100, 200, 255), (16, 16), 8)
            pygame.display.set_icon(icon_surface)
        except:
            pass  # Ikona opcjonalna
    
    def handle_events(self):
        """Obsługa wydarzeń"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.fractal_engine.reset_view()
                    self.zoom_level = 1.0
                    self.start_render()
                elif event.key == pygame.K_c:
                    # Zmiana palety kolorów
                    self.color_palette.next_palette()
                    self.start_render()
                elif event.key == pygame.K_s:
                    # Zapisz screenshot
                    self.save_screenshot()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # Zwiększ jakość renderowania
                    self.fractal_engine.increase_iterations()
                    self.start_render()
                elif event.key == pygame.K_MINUS:
                    # Zmniejsz jakość renderowania
                    self.fractal_engine.decrease_iterations()
                    self.start_render()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk
                    self.dragging = True
                    self.last_mouse_pos = event.pos
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.fractal_engine.pan(-dx, -dy)
                    self.last_mouse_pos = event.pos
                    self.start_render()
            
            elif event.type == pygame.MOUSEWHEEL:
                # Zoom z kółkiem myszy
                mouse_x, mouse_y = pygame.mouse.get_pos()
                zoom_factor = 1.2 if event.y > 0 else 1/1.2
                
                self.fractal_engine.zoom_at_point(
                    mouse_x, mouse_y, zoom_factor
                )
                self.zoom_level *= zoom_factor
                self.start_render()
            
            elif event.type == pygame.VIDEORESIZE:
                # Zmiana rozmiaru okna
                self.width, self.height = event.w, event.h
                self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                self.fractal_engine.resize(self.width, self.height)
                self.start_render()
    
    def start_render(self):
        """Rozpocznij renderowanie w osobnym wątku"""
        if self.rendering:
            return
        
        self.rendering = True
        self.render_thread = threading.Thread(target=self.render_fractal)
        self.render_thread.start()
    
    def render_fractal(self):
        """Renderowanie fraktala w osobnym wątku"""
        import time
        start_time = time.time()
        
        try:
            # Generowanie fraktala
            fractal_data = self.fractal_engine.generate()
            
            # Kolorowanie
            colored_data = self.color_palette.apply_colors(fractal_data)
            
            # Konwersja na surface Pygame
            with self.render_lock:
                self.current_surface = pygame.surfarray.make_surface(
                    colored_data.swapaxes(0, 1)
                )
                
            self.render_time = time.time() - start_time
            
        except Exception as e:
            print(f"Błąd renderowania: {e}")
        
        finally:
            self.rendering = False
    
    def draw_ui(self):
        """Rysowanie interfejsu użytkownika"""
        # Tło dla informacji
        info_rect = pygame.Rect(10, 10, 300, 120)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), info_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), info_rect, 2)
        
        # Informacje tekstowe
        y_offset = 20
        texts = [
            f"FPS: {self.fps:.1f}",
            f"Zoom: {self.zoom_level:.2e}x",
            f"Czas render: {self.render_time:.2f}s",
            f"Iteracje: {self.fractal_engine.max_iter}",
            f"Paleta: {self.color_palette.current_palette_name}"
        ]
        
        for text in texts:
            surface = self.small_font.render(text, True, (255, 255, 255))
            self.screen.blit(surface, (20, y_offset))
            y_offset += 20
        
        # Instrukcje sterowania
        controls_y = self.height - 180
        controls_rect = pygame.Rect(10, controls_y, 380, 160)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), controls_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), controls_rect, 2)
        
        controls = [
            "*  Przeciągnij: Poruszanie",
            "*  Scroll: Zoom in/out",
            "*  =/+: Zwiększ jakość renderowania", 
            "*  -: Zmniejsz jakość renderowania",
            "*  Spacja: Reset widoku",
            "*  C: Zmiana kolorów",
            "*  S: Screenshot"
        ]
        
        y_offset = controls_y + 10
        for control in controls:
            surface = self.small_font.render(control, True, (255, 255, 255))
            self.screen.blit(surface, (20, y_offset))
            y_offset += 20
        
        # Status renderowania
        if self.rendering:
            status_text = self.font.render("🔄 Renderowanie...", True, (255, 255, 0))
            text_rect = status_text.get_rect(center=(self.width//2, 30))
            pygame.draw.rect(self.screen, (0, 0, 0, 180), text_rect.inflate(20, 10))
            self.screen.blit(status_text, text_rect)
    
    def save_screenshot(self):
        """Zapisz screenshot fraktala"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fractal_screenshot_{timestamp}.png"
        pygame.image.save(self.screen, filename)
        print(f"Screenshot zapisany: {filename}")
    
    def run(self):
        """Główna pętla aplikacji"""
        print("🌈 Uruchamianie aplikacji Fraktal Mandelbrota...")
        print("⚡ Używaj myszy do nawigacji, scroll do zoomu!")
        
        # Pierwsze renderowanie
        self.start_render()
        
        while self.running:
            # Wydarzenia
            self.handle_events()
            
            # Czyszczenie ekranu
            self.screen.fill((10, 10, 20))
            
            # Rysowanie fraktala
            with self.render_lock:
                if self.current_surface:
                    self.screen.blit(self.current_surface, (0, 0))
            
            # Interface użytkownika
            self.draw_ui()
            
            # Aktualizacja ekranu
            pygame.display.flip()
            self.fps = self.clock.tick(60)
        
        # Oczekiwanie na zakończenie renderowania
        if self.render_thread and self.render_thread.is_alive():
            self.render_thread.join(timeout=1.0)
        
        pygame.quit()
        print("👋 Aplikacja zamknięta. Dziękujemy za używanie!")

def main():
    """Funkcja główna"""
    try:
        app = FractalApp()
        app.run()
    except Exception as e:
        print(f"❌ Błąd aplikacji: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
