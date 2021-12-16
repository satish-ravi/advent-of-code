import sys
from dataclasses import dataclass


@dataclass
class Packet:
    type_id: int
    version: int


@dataclass
class LiteralPacket(Packet):
    literal: int


@dataclass
class OperatorPacket0(Packet):
    num_bits: int
    packets: list[Packet]


@dataclass
class OperatorPacket1(Packet):
    num_subpackets: int
    packets: list[Packet]


inp = sys.stdin.read().split("\n")[0]


def get_binary(hex_str):
    result = ""
    for ch in hex_str:
        bin_str = bin(int(ch, 16))[2:]
        result += "0" * (4 - len(bin_str)) + bin_str
    return result


def parse_packet(packet_bin, num_packets=None, level=0):
    packets = []
    current = 0
    while (
        packet_bin[current:]
        and len(packet_bin[current:]) > 7
        and int(packet_bin[current:], 2) != 0
    ):
        version = int(packet_bin[current : current + 3], 2)
        type_id = int(packet_bin[current + 3 : current + 6], 2)
        current += 6
        if type_id == 4:
            lit_str = ""
            ended = False
            while not ended:
                ended = packet_bin[current] == "0"
                lit_str += packet_bin[current + 1 : current + 5]
                current += 5
            packets.append(LiteralPacket(type_id, version, int(lit_str, 2)))
        elif packet_bin[current] == "0":
            num_bits = int(packet_bin[current + 1 : current + 16], 2)
            subpackets, _ = parse_packet(
                packet_bin[current + 16 : current + 16 + num_bits], None, level + 1
            )
            current += 16 + num_bits
            packets.append(OperatorPacket0(type_id, version, num_bits, subpackets))
        else:
            num_subpackets = int(packet_bin[current + 1 : current + 12], 2)
            subpackets, total_length = parse_packet(
                packet_bin[current + 12 :], num_subpackets, level + 1
            )
            current += 12 + total_length
            packets.append(
                OperatorPacket1(type_id, version, num_subpackets, subpackets)
            )
        if num_packets is not None:
            num_packets -= 1
            if num_packets == 0:
                break
    return packets, current


def sum_versions(packets: list[Packet]) -> int:
    result = 0
    for packet in packets:
        if type(packet) == LiteralPacket:
            result += packet.version
        else:
            assert type(packet) in [OperatorPacket0, OperatorPacket1]
            result += packet.version + sum_versions(packet.packets)
    return result


def compute(packet: Packet) -> int:
    if packet.type_id == 4:
        assert type(packet) == LiteralPacket
        return packet.literal
    else:
        assert type(packet) in [OperatorPacket0, OperatorPacket1]
        if packet.type_id == 0:
            return sum(compute(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 1:
            result = 1
            for sub_packet in packet.packets:
                result *= compute(sub_packet)
            return result
        elif packet.type_id == 2:
            return min(compute(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 3:
            return max(compute(sub_packet) for sub_packet in packet.packets)
        elif packet.type_id == 5:
            assert len(packet.packets) == 2
            return 1 if compute(packet.packets[0]) > compute(packet.packets[1]) else 0
        elif packet.type_id == 6:
            assert len(packet.packets) == 2
            return 1 if compute(packet.packets[0]) < compute(packet.packets[1]) else 0
        elif packet.type_id == 7:
            assert len(packet.packets) == 2
            return 1 if compute(packet.packets[0]) == compute(packet.packets[1]) else 0
        else:
            raise Exception("should not reach here")


packets, _ = parse_packet(get_binary(inp), 1)
print("part1:", sum_versions(packets))
print("part2:", compute(packets[0]))
