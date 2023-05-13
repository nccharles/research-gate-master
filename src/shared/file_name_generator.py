__author__ = "Sylvie"
__copyright__ = "Copyright 2023, AUCA Research Gate"

import random
import string
from typing import Callable


class FileNameGenerator:
    @staticmethod
    def generate_file_name(base_string_length: int, extension: str = None, generator_function: Callable[[int], str] = None):
        if not generator_function:
            generator_function: Callable[[int], str] = FileNameGenerator.random_generator_function
        generated_base_name: str = generator_function(base_string_length)
        return generated_base_name + "." + extension if extension else generated_base_name

    @staticmethod
    def random_generator_function(string_length: int):
        if not isinstance(string_length, int) or not string_length > 0:
            raise ValueError("Invalid string length value {0}".format(string_length))
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(string_length)])
