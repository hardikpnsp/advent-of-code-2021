bits_array = []

with open('./input-2.txt') as f:
    while(line := f.readline()):
        bits_array.append(line.strip())

width = len(bits_array[0])


oxygen_generator_rating = bits_array
current_bit = 0
while(len(oxygen_generator_rating) > 1):
    ones = 0
    zeroes = 0

    for bits in oxygen_generator_rating:
        match bits[current_bit]:
            case '1':
                ones += 1
            case '0':
                zeroes += 1

    chosen_bit = '1' if ones >= zeroes else '0'
    oxygen_generator_rating = list(filter(lambda x: x[current_bit] == chosen_bit, oxygen_generator_rating))
    current_bit += 1

oxygen_generator_rating = int(oxygen_generator_rating[0], 2)

co2_scrubber_ratting = bits_array
current_bit = 0
while(len(co2_scrubber_ratting) > 1):
    ones = 0
    zeroes = 0

    for bits in co2_scrubber_ratting:
        match bits[current_bit]:
            case '1':
                ones += 1
            case '0':
                zeroes += 1

    chosen_bit = '1' if ones < zeroes else '0'
    co2_scrubber_ratting = list(filter(lambda x: x[current_bit] == chosen_bit, co2_scrubber_ratting))
    current_bit += 1

co2_scrubber_ratting = int(co2_scrubber_ratting[0], 2)

print(oxygen_generator_rating * co2_scrubber_ratting)

