from typing import Union
import click
import io
from pathlib import Path
from PIL import Image


def to_binary(data: Union[str, int]):
    if type(data) == str:
        return ''.join([format(ord(i), '08b') for i in data])
    elif type(data) == int:
        return format(data, "08b")


@click.group()
def cli():
    pass


@cli.command()
@click.option('--image-path', help='Path to the image containing steganography data')
@click.option('--report-length', help='Length of encrypted report data', type=click.INT)
@click.option('--output-path', help='Path to save the hidden data as text file')
def extract(image_path: Path, report_length: int, output_path: Path):
    """Extract data hidden in an image

    Args:
        image_path (Path): Path to the image containing steganography data
        report_length (int): Length of encrypted report data
        output_path (Path): Path to save the hidden data as text file
    """
    im = Image.open(image_path)
    steg_bits = io.StringIO()
    index = 0
    for pixel in im.getdata():
        for c in pixel:
            if (index < report_length):
                bit_num = str(c % 2)
                steg_bits.write(bit_num)
                index += 1
            else:
                break
        else:
            continue
        break
    steg_bits.seek(0)
    bit_string = steg_bits.read()
    steg_bits.close()
    
    b64_data = int(bit_string, 2).to_bytes((len(bit_string) + 7) // 8, byteorder='big')
    with open(output_path, 'w') as of:
        of.write(b64_data.decode('ascii'))
    
    

if __name__ == "__main__":
    cli()
