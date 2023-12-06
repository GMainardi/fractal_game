import numpy as np
import itertools


class NewtonsMethod():

    def __init__(self, roots: list[complex]) -> None:

        self.roots = roots

        self.colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (0, 255, 255),
            (255, 0, 255),
            (192, 192, 192),
            (128, 128, 128),
            (128, 0, 0),
            (128, 128, 0),
            (0, 128, 0),
            (128, 0, 128),
            (0, 128, 128),
            (0, 0, 128),
            (128, 128, 0)
        ]

        def f(x):
            result = 1
            for root in self.roots:
                result *= (x - root)
            return result
        
        def df(x):
            result = 0
            for products in itertools.combinations(self.roots, len(self.roots)-1):
                p_r = 1
                for prod in products:
                    p_r *= (x-prod)
                result += p_r
            return result
        
        self.f_func = f
        self.diff_f_func = df
                    

    def resolves_newton(self, x):
        return x - self.f_func(x)/self.diff_f_func(x)
    
    def converges(self, z: complex, max_it: int = 15) -> bool:
        for _ in range(max_it):
            z = self.resolves_newton(z)

        return self.get_closest_root(z)

    def get_closest_root(self, z: complex) -> tuple[int, int, int]:

        closest = 0
        for idx, root in enumerate(self.roots[1:]):

            if abs(z-root) < abs(z-self.roots[closest]):
                closest = idx+1

        return self.colors[closest]
                
    
class HolomorphicDynamics:

    def __init__(self, func: NewtonsMethod, frame_size: tuple[int]) -> None:
        self.func = func
        self.frame_size = frame_size
    

    def color_points(self, window: tuple[float]) -> np.array:
        '''
        Color every pixel in `self.frame_size` based on `window` values applied on `self.func`, if that function converges

        `window`: x, y, w, h vaules that are shown on the window with `self.frame_size` pixels

        return: a matrix of `self.frame_size` shape filled with values based on `self.func` convergion
        '''


        x, y, w, h = window
        x_values = np.linspace(x, 
                               x + w, 
                               self.frame_size[1])

        y_values = np.linspace(y,
                               y + h,
                               self.frame_size[0])
        
        pixels = np.zeros((*self.frame_size, 3))
        for x_idx, real in enumerate(x_values):
            for y_idx, imag in enumerate(y_values):

                c = complex(real, imag)
                pixels[y_idx, x_idx, :] = self.func.converges(c)


        return pixels