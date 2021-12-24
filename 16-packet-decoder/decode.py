"""Packet

First 3 bits -> Version
Next 3 bits -> Type ID


Type ID:
-------
4 -> literal value:
    pad with leading zero till length is multiple of 4 bits
    break into groups of 4 bits
        each group is prefixed by 1: except the last group which is prefixed by 0

    Basically if 4 -> scan every group of 5 bits till there is a group which starts with 0

not 4 -> operator:
    it contains one or more packets

    length type ID: bit right after version and Type ID
    --------------
    0 -> next 15 bits are number representing total length in bits of the subpacket
    1: -> next 11 bits are number representing total subpackets immediately contained by this packet
"""

from functools import reduce

class Packet:
    def __init__(self, packet_binary) -> None:
        self.subpackets = []
        self.version = 0
        self.type_id = 0
        self.literal = 0
        self.binary = 0
        self.length_type_id = 0

        self.parse_packet(packet_binary)

    def parse_packet(self, packet_binary):
        self.binary = packet_binary
        self.version = self.parse_version(self.binary)
        self.type_id = self.parse_type_id(self.binary)

        if self.type_id == 4:
            # current packet is a literal, populate literal
            # group of 5 bits from 7th bit
            self.literal = self.parse_literal(self.binary[6:])
        else:
            # current packet has sub packets, populate subpackets
            self.length_type_id = self.parse_len_type_id(self.binary)
            if self.length_type_id == 0:
                # next 15 bits define len till which subpackets exists
                subpackets_len = int(self.binary[7:22], base=2)
                current_len = 0
                offset = 22
                while current_len < subpackets_len:
                    l = self.find_subpacket_len(self.binary[current_len + offset:])
                    p = Packet(self.binary[current_len + offset: current_len + offset + l])
                    self.subpackets.append(p)
                    current_len += l
            else:
                # next 11 btis define how many subpackets are there
                number_of_subpackets = int(self.binary[7:18], base=2)
                current_len = 0
                offset = 18
                for _ in range(number_of_subpackets):
                    l = self.find_subpacket_len(self.binary[current_len + offset:])
                    p = Packet(self.binary[current_len + offset : current_len + offset + l])
                    self.subpackets.append(p)
                    current_len += l

    def literal_len(self, literal_binary):
        i = 5
        while (i <= len(literal_binary)):
            group = literal_binary[i-5:i]
            if group.startswith("0"):
                return i
            i += 5

    def find_subpacket_len(self, packet_binary):
        type_id = self.parse_type_id(packet_binary)

        if type_id == 4:
            # current packet is a literal, populate literal
            # group of 5 bits from 7th bit
            return 6 + self.literal_len(packet_binary[6:])
        else:
            # current packet has sub packets, populate subpackets
            self.length_type_id = self.parse_len_type_id(packet_binary)
            if self.length_type_id == 0:
                # next 15 bits define len till which subpackets exists
                subpackets_len = int(packet_binary[7:22], base=2)
                return 22 + subpackets_len
            else:
                # next 11 btis define how many subpackets are there
                number_of_subpackets = int(packet_binary[7:18], base=2)
                current_len = 0
                offset = 18
                for _ in range(number_of_subpackets):
                    l = self.find_subpacket_len(packet_binary[current_len + offset:])
                    current_len += l
                return current_len + offset

    def parse_len_type_id(self, packet_binary):
        return int(packet_binary[6])

    def parse_type_id(self, packet_binary):
        return int(packet_binary[3:6], base=2)

    def parse_version(self, packet_binary):
        return int(packet_binary[0:3], base=2)

    def parse_literal(self, literal_binary):
        i = 5
        data = ""
        while (i <= len(literal_binary)):
            group = literal_binary[i-5:i]
            data += group[1:]
            if group.startswith("0"):
                break
            i += 5
        return int(data, base=2)

    def value(self):
        if self.type_id == 0:
            return sum(map(lambda x: x.value(), self.subpackets))
        elif self.type_id == 1:
            subpackets_values = map(lambda x: x.value(), self.subpackets)
            return reduce(lambda x, y: x * y, subpackets_values)
        elif self.type_id == 2:
            return min(map(lambda x: x.value(), self.subpackets))
        elif self.type_id == 3:
            return max(map(lambda x: x.value(), self.subpackets))
        elif self.type_id == 4:
            return self.literal
        elif self.type_id == 5:
            subpackets_values = list(map(lambda x: x.value(), self.subpackets))
            if subpackets_values[0] > subpackets_values[1]:
                return 1
            else:
                return 0
        elif self.type_id == 6:
            subpackets_values = list(map(lambda x: x.value(), self.subpackets))
            if subpackets_values[0] < subpackets_values[1]:
                return 1
            else:
                return 0
        elif self.type_id == 7:
            subpackets_values = list(map(lambda x: x.value(), self.subpackets))
            if subpackets_values[0] == subpackets_values[1]:
                return 1
            else:
                return 0






def print_packet(packet, indent):
    print(" "*indent + f"Binary: {packet.binary} -> Version: {packet.version} -> TypeID: {packet.type_id} -> Literal: {packet.literal}")
    for p in packet.subpackets:
        print_packet(p, indent+2)

def version_sum(packet):
    total = packet.version
    for p in packet.subpackets:
        total += version_sum(p)
    return total

if __name__ == "__main__":
    packet_hex = "A059141803C0008447E897180401F82F1E60D80021D11A3DC3F300470015786935BED80A5DB5002F69B4298A60FE73BE41968F48080328D00427BCD339CC7F431253838CCEFF4A943803D251B924EC283F16D400C9CDB3180213D2D542EC01092D77381A98DA89801D241705C80180960E93469801400F0A6CEA7617318732B08C67DA48C27551C00F972830052800B08550A277416401A5C913D0043D2CD125AC4B1DB50E0802059552912E9676931530046C0141007E3D4698E20008744D89509677DBF5759F38CDC594401093FC67BACDCE66B3C87380553E7127B88ECACAD96D98F8AC9E570C015C00B8E4E33AD33632938CEB4CD8C67890C01083B800E5CBDAB2BDDF65814C01299D7E34842E85801224D52DF9824D52DF981C4630047401400042E144698B2200C4328731CA6F9CBCA5FBB798021259B7B3BBC912803879CD67F6F5F78BB9CD6A77D42F1223005B8037600042E25C158FE0008747E8F50B276116C9A2730046801F29BC854A6BF4C65F64EB58DF77C018009D640086C318870A0C01D88105A0B9803310E2045C8CF3F4E7D7880484D0040001098B51DA0980021F17A3047899585004E79CE4ABD503005E610271ED4018899234B64F64588C0129EEDFD2EFBA75E0084CC659AF3457317069A509B97FB3531003254D080557A00CC8401F8791DA13080391EA39C739EFEE5394920C01098C735D51B004A7A92F6A0953D497B504F200F2BC01792FE9D64BFA739584774847CE26006A801AC05DE180184053E280104049D10111CA006300E962005A801E2007B80182007200792E00420051E400EF980192DC8471E259245100967FF7E6F2CF25DBFA8593108D342939595454802D79550C0068A72F0DC52A7D68003E99C863D5BC7A411EA37C229A86EBBC0CB802B331FDBED13BAB92080310265296AFA1EDE8AA64A0C02C9D49966195609C0594223005B80152977996D69EE7BD9CE4C1803978A7392ACE71DA448914C527FFE140"
    packet_binary = "".join([format(int(h, 16), "#06b")[2:] for h in packet_hex])

    packet = Packet(packet_binary)
    print_packet(packet, 0)

    version_sum = version_sum(packet)
    print(version_sum)

    print(packet.value())

"""
 4                        1                       5                             6
___                     ____                     ___                          ____
1000 1010 0000 0000 01 [00 1010 1 000 0000 0001 [1010 1000 0000 0000 0010 11 [11 0100 0111 1 000]]]
   ____ ______________      ___   _____________     ____ ___________________      ___ VVVVVV XXX
    2         1              2         1             2             11              4    15

"""
