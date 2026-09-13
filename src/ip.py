
import re


def is_valid_ipv4(addr:str) -> bool:
    octet = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"

    ipv4_pattern = (
        rf"^{octet}\."
        rf"{octet}\."
        rf"{octet}\."
        rf"{octet}$"
    )

    return re.match(ipv4_pattern, addr) is not None


def is_valid_ipv6(addr:str) -> bool:
    hex_group = r"[0-9a-fA-F]{1,4}"

    # IPv4 part for IPv4-embedded IPv6 addresses
    ipv4_octet = r"(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])"
    ipv4 = (
        rf"{ipv4_octet}\."
        rf"{ipv4_octet}\."
        rf"{ipv4_octet}\."
        rf"{ipv4_octet}"
    )

    ipv6_pattern = (
        rf"^("
        rf"(?:{hex_group}:){{7}}{hex_group}"
        rf"|(?:{hex_group}:){{1,7}}:"
        rf"|(?:{hex_group}:){{1,6}}:{hex_group}"
        rf"|(?:{hex_group}:){{1,5}}(?::{hex_group}){{1,2}}"
        rf"|(?:{hex_group}:){{1,4}}(?::{hex_group}){{1,3}}"
        rf"|(?:{hex_group}:){{1,3}}(?::{hex_group}){{1,4}}"
        rf"|(?:{hex_group}:){{1,2}}(?::{hex_group}){{1,5}}"
        rf"|{hex_group}:((?::{hex_group}){{1,6}})"
        rf"|:((?::{hex_group}){{1,7}}|:)"
        rf")$"
    )

    if re.match(ipv6_pattern, addr):
        return True

    # IPv4-embedded IPv6
    ipv6_ipv4_pattern = (
        rf"^("
        rf"::ffff:{ipv4}"
        rf"|::ffff:0:{ipv4}"
        rf"|::(?:ffff:)?{ipv4}"
        rf")$"
    )

    return re.match(ipv6_ipv4_pattern, addr) is not None


def is_valid_ip(addr:str) -> bool:
    if ":" in addr:
        return is_valid_ipv6(addr)

    return is_valid_ipv4(addr)


def test_runner(test_data:list, test_title:str="", test_func=is_valid_ip):
    if test_title:
        test_title = f": {test_title}"
    print(f"Testing{test_title}")
    successfull = []
    failed = []
    for ip, expected in test_data:
        result = test_func(ip)
        if expected == result:
            successfull.append(ip)
        else:
            failed.append(ip)
            print(f"{ip} should be {expected}: {expected == result} (is {result})")

    print(f"Total Data: {len(test_data)}")
    print(f"Success: {len(successfull)}")
    print(f"Failed : {len(failed)}")


def test():
    test_ipv4 = [
        # Valid IPv4 addresses
        ("127.0.0.1", True),
        ("0.0.0.0", True),
        ("255.255.255.255", True),
        ("1.2.3.4", True),
        ("192.168.1.1", True),
        ("10.0.0.1", True),

        # Invalid: wrong number of octets
        ("1.2", False),
        ("1.2.3", False),
        ("1.2.3.4.5", False),
        ("", False),

        # Invalid: values outside 0-255
        ("256.0.0.1", False),
        ("1.256.3.4", False),
        ("1.2.3.256", False),
        ("999.999.999.999", False),

        # Invalid: non-numeric
        ("bernd.test", False),
        ("a.b.c.d", False),
        ("1.2.3.a", False),
        ("1.two.3.4", False),

        # Invalid: malformed
        ("1..3.4", False),
        (".1.2.3", False),
        ("1.2.3.", False),
        ("1.2.03.4", False),
        ("1.2.3.4 ", False),
    ]

    test_runner(test_ipv4, "IPv4", is_valid_ipv4)

    test_ipv6 = [
        # Valid full IPv6 addresses
        ("2001:0db8:85a3:0000:0000:8a2e:0370:7334", True),
        ("2001:db8:85a3:0:0:8a2e:370:7334", True),
        ("fe80:0000:0000:0000:0202:b3ff:fe1e:8329", True),

        # Valid compressed IPv6 addresses
        ("::1", True),
        ("::", True),
        ("2001:db8::1", True),
        ("2001:db8::", True),
        ("::ffff:192.168.1.1", True),

        # Valid IPv6 with hexadecimal charactersip_v
        ("FE80::1", True),
        ("abcd:ef01:2345:6789:abcd:ef01:2345:6789", True),

        # Invalid: too many groups
        ("1:2:3:4:5:6:7:8:9", False),
        ("1:2:3:4:5:6:7:8:9:10", False),

        # Invalid: malformed compression
        ("1:2:3:4:5:6:7:8:", False),
        (":1:2:3:4:5:6:7:8", False),
        ("1:2:3:4:5:6:7:8::", False),
        ("1::2::3", False),

        # Invalid: invalid hexadecimal characters
        ("gggg::1", False),
        ("2001:db8:zzzz::1", False),

        # Invalid: group too long
        ("12345::1", False),
        ("2001:db8:12345::1", False),

        # Invalid: random strings / IPv4
        ("127.0.0.1", False),
        ("bernd.test", False),
        ("", False),
    ]
    test_runner(test_ipv6, "IPv6", is_valid_ipv6)


if __name__ == "__main__":
    test()
