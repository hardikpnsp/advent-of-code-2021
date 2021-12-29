import copy


def read_input():
    with open("input.txt") as f:
        algorithm = f.readline().strip()
        f.readline()
        image = []
        while line := f.readline():
            image.append(list(line.strip()))

    return algorithm, image


def get_outer_pixel(pass_number, algorithm):
    if algorithm[0] == ".":
        return "."
    else:
        # hardcoded based on my input
        if pass_number % 2 == 0:
            return "."
        else:
            return "#"


def enhance(image, algorithm, pass_number=0):
    # TODO: cleanup
    new_image = copy.deepcopy(image)
    for i in range(1, len(image) - 1):
        for j in range(1, len(image[0]) - 1):
            index_string = image[i - 1][j - 1:j + 2] + image[i][j - 1:j + 2] + image[i + 1][j - 1:j + 2]
            new_image[i][j] = algorithm[index_from_pixels(index_string)]

    outer_pixel = get_outer_pixel(pass_number, algorithm)

    # first row, first col
    index_string = list(outer_pixel * 3) + list(outer_pixel) + image[0][:2] + list(outer_pixel) + image[1][:2]
    new_image[0][0] = algorithm[index_from_pixels(index_string)]

    # first row, last col
    index_string = list(outer_pixel * 3) + image[0][-2:] + list(outer_pixel) + image[1][-2:] + list(outer_pixel)
    new_image[0][-1] = algorithm[index_from_pixels(index_string)]

    # first row
    for j in range(1, len(image[0]) - 1):
        index_string = list(outer_pixel * 3) + image[0][j - 1:j + 2] + image[1][j - 1:j + 2]
        new_image[0][j] = algorithm[index_from_pixels(index_string)]

    # last row, first col
    index_string = list(outer_pixel) + image[-2][:2] + list(outer_pixel) + image[-1][:2] + list(outer_pixel * 3)
    new_image[-1][0] = algorithm[index_from_pixels(index_string)]

    # last row, last col
    index_string = image[-2][-2:] + list(outer_pixel) + image[-1][-2:] + list(outer_pixel) + list(outer_pixel * 3)
    new_image[-1][-1] = algorithm[index_from_pixels(index_string)]

    # last row
    for j in range(1, len(image[0]) - 1):
        index_string = image[-2][j - 1:j + 2] + image[-1][j - 1:j + 2] + list(outer_pixel * 3)
        new_image[-1][j] = algorithm[index_from_pixels(index_string)]

    # first column
    for i in range(1, len(image) - 1):
        index_string = list(outer_pixel) + image[i - 1][0:2] + list(outer_pixel) + image[i][0:2] + list(outer_pixel) + \
                       image[i + 1][0:2]
        new_image[i][0] = algorithm[index_from_pixels(index_string)]

    # last column
    for i in range(1, len(image) - 1):
        index_string = image[i - 1][-2:] + list(outer_pixel) + image[i][-2:] + list(outer_pixel) + image[i + 1][
                                                                                                   -2:] + list(
            outer_pixel)
        new_image[i][-1] = algorithm[index_from_pixels(index_string)]

    return new_image


def index_from_pixels(index_string):
    return int("".join(map(lambda x: '1' if x == '#' else '0', index_string)), base=2)


def pad_image(image):
    # pad 3 pixels on all sides
    padded_image = [list("." * (len(image[0]) + 6))] * 3
    for row in image:
        padded_image.append(list("...") + row + list("..."))
    padded_image.extend([list("." * (len(image[0]) + 6))] * 3)
    return padded_image


def print_image(new_image):
    rows = []
    for row in new_image:
        rows.append("".join(row))
    print("\n".join(rows))


def calculate_lit_pixels(new_image):
    count = 0
    for row in new_image:
        for pixel in row:
            if pixel == "#":
                count += 1

    return count


def main(num_of_pass=2):
    algorithm, image = read_input()
    part1(algorithm, image, num_of_pass)
    part1(algorithm, image, 50)


def part1(algorithm, image, num_of_pass):
    # Could have done it without padding 3 * pass rows up front, instead add 1 outer pixel per pass
    padded_image = image
    for _ in range(num_of_pass):
        padded_image = pad_image(padded_image)

    new_image = padded_image
    for i in range(num_of_pass):
        new_image = enhance(new_image, algorithm, pass_number=i)

    print_image(new_image)
    print(f"Part 1: {calculate_lit_pixels(new_image)}")


if __name__ == "__main__":
    main()
