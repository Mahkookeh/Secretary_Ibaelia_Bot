import PIL
import pytesseract
import re

# Set tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# Set image path
image_path = "..\\..\\test_images\\"


def parse_text(text):
    start = "puzzle in"
    end = r"\."
    result = re.search(r"%s\s?(.*)%s|%s\n*(.*)" % (start, end, start), text)
    if result.group(1):
        return result.group(1)
    else:
        return result.group(2)

def format_zeros(time):
    if len(time) == 1:
        return f"0{time}"
    return time

def format_time(time_text):
    if ":" in time_text:
        times = time_text.split(":")[::-1]
    elif "seconds" in time_text:
        times = [time_text[:time_text.index(" ")]]

    hours = "00:" if len(times) < 3 else f"{format_zeros(times[2])}:"
    minutes = "00:" if len(times) < 2 else f"{format_zeros(times[1])}:"
    seconds = f"{format_zeros(times[0])}"
    return f"{hours}{minutes}{seconds}"

def get_time_from_image(img):
    text = pytesseract.image_to_string(img)
    time_text = parse_text(text)
    formatted_time = format_time(time_text)
    return formatted_time



if __name__ == '__main__':
    time_array = []

    img = PIL.Image.open(f"{image_path}crossword1.png")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword2.png")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword3.jpg")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword4.jpg")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword5.jpg")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword6.png")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword7.jpg")
    time_array.append(get_time_from_image(img))

    img = PIL.Image.open(f"{image_path}crossword8.png")
    time_array.append(get_time_from_image(img))

    print(time_array)
    print(sorted(time_array))