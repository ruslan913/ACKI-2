import os

def inPutBit(input_file, read_bit, bit_len, garbage_bit):
    if bit_len == 0:
        sib_bit = input_file.read(1)
        read_bit = int.from_bytes(sib_bit, "little")
        if sib_bit == b"":
            garbage_bit += 1
            read_bit = 255
            if garbage_bit >14:
                print("Ruslan is stuped")
                exit(1)
        bit_len = 8

    t = read_bit & 1
    read_bit >>= 1
    bit_len -= 1
    return t, read_bit, bit_len, garbage_bit
def Decode():
    read_bit = 0
    bit_len = 0
    garbage_bit = 0

    with open("out.txt", "rb") as file_in:

        chuck = ord(file_in.read(1))

        rasp_slovar = {}
        for i in range(chuck):
            key_hat = file_in.read(1).decode('ascii')

            val_hat = int.from_bytes(file_in.read(4), "little")

            rasp_slovar[key_hat] = val_hat

        slovar_mas = [0, 1]

        for i in rasp_slovar:
            slovar_mas.append(rasp_slovar[i] + slovar_mas[-1])

        with open("out_final.txt", "wb+") as file_out:
            low_v = 0
            high_v = (1 << 16) - 1
            delete = slovar_mas[-1]
            diff = high_v - low_v + 1
            first_q = int(int(high_v + 1) / 4)
            half_q = first_q * 2
            third_q = first_q * 3
            val = 0

            for i in range(16):
                k, read_bit, bit_len, garbage_bit = inPutBit(file_in, read_bit, bit_len, garbage_bit)
                val += val + k
            while True:
                freq = int(((val - low_v + 1) * delete - 1) / diff)
                j = 1
                while slovar_mas[j] <= freq:
                    j += 1
                high_v = int(low_v + slovar_mas[j] * diff / delete - 1)
                low_v = int(low_v + slovar_mas[j - 1] * diff / delete)

                while True:
                    if high_v < half_q:
                        pass
                    elif low_v >= half_q:
                        low_v -= half_q
                        high_v -= half_q
                        val -= half_q
                    elif low_v >= first_q and high_v < third_q:
                        low_v -= first_q
                        high_v -= first_q
                        val -= first_q
                    else:
                        break
                    low_v += low_v
                    high_v += high_v + 1
                    k, read_bit, bit_len, garbage_bit = inPutBit(file_in, read_bit, bit_len, garbage_bit)
                    val += val + k
                if j == 1:
                    break
                file_out.write(list(rasp_slovar.keys())[j - 2].encode('ascii'))
                diff = high_v - low_v + 1

def InForSym(sin, irgum):
    j = 0
    for i in sin:
        if irgum == i:
            return j + 2
        j += 1
    print("Ruslan want to sleep")

def outPutBit(bit, outputfile, write_bit, bit_len):
    write_bit >>= 1
    if bit & 1:
        write_bit |= 0x80
    bit_len -= 1

    if bit_len == 0:
        bit_len = 8
        outputfile.write(write_bit.to_bytes(1, "little"))

    return write_bit, bit_len

def bitPlusFollow(bit, bittofollow, outputfile, write_bit, bit_len):
    write_bit, bit_len = outPutBit(bit, outputfile, write_bit, bit_len)
    for _ in range(bittofollow):
        write_bit, bit_len = outPutBit(~bit, outputfile, write_bit, bit_len)
    return write_bit, bit_len

def indexForSymbol(sin, irgum):
    j = 0
    for i in sin:
        if irgum == i:
           return j + 2
        j += 1
    print("Developer is Idiot")

def Coder():
    counter = 0
    write_bit = 0
    bit_len = 8

    sum_slovar = 0
    with open('in.txt', 'r') as fp:
        test_sum = 0
        chunk = fp.read(1)
        slovar = {}
        while chunk:
            test_sum += 1
            if slovar.get(chunk) == None:
                slovar.update({chunk: 1})
            else:
                    #
                slovar[chunk] = slovar[chunk] + 1

            chunk = fp.read(1)


        for _, val in slovar.items():
            sum_slovar = sum_slovar + val
        if test_sum == sum_slovar:
            print("Ok")
        else:
            print("not Ok")

    sorted_slovar = dict(sorted(slovar.items(), key=lambda item: item[1], reverse=True))

    slovar_mas = [0, 1]
    for i in sorted_slovar:
        slovar_mas.append(sorted_slovar[i] + slovar_mas[-1])

    f = open("out.txt", "wb+")
    print(len(sorted_slovar))
    f.write(len(sorted_slovar).to_bytes(1, "little"))
    for i in sorted_slovar:
        f.write(i.encode("ascii"))
        f.write(sorted_slovar[i].to_bytes(4, "little"))
    print(sorted_slovar)

    with open('in.txt', 'r') as fp:
        low_v = 0
        high_v = (1 << 16)-1  # 2^16 интервал
        delete = slovar_mas[-1]
        diff = high_v - low_v + 1
        first_q = int(int(high_v + 1) / 4)
        half_q = first_q * 2
        third_q = first_q * 3
        bit_to_follow = 0

        chip = fp.read(1)
        while chip:
            j = indexForSymbol(sorted_slovar, chip)
            high_v = int(low_v + slovar_mas[j] * diff / delete - 1)
            low_v = int(low_v + slovar_mas[j - 1] * diff / delete)

            while True:
                if high_v < half_q:
                    write_bit, bit_len = bitPlusFollow(0, bit_to_follow, f, write_bit, bit_len)
                    bit_to_follow=0
                elif low_v >= half_q:
                    write_bit, bit_len = bitPlusFollow(1, bit_to_follow, f, write_bit, bit_len)
                    bit_to_follow=0
                    low_v -= half_q
                    high_v -= half_q
                elif low_v >= first_q and high_v < third_q:
                    bit_to_follow += 1
                    low_v -= first_q
                    high_v -= first_q
                else:
                    break
                low_v += low_v
                high_v += high_v + 1

            diff = high_v - low_v + 1
            chip = fp.read(1)

        high_v = int(low_v + slovar_mas[1] * diff / delete - 1)
        low_v = int(low_v + slovar_mas[0] * diff / delete)

        while True:
            if high_v < half_q:
                write_bit, bit_len = bitPlusFollow(0, bit_to_follow, f, write_bit, bit_len)
                bit_to_follow=0
            elif low_v >= half_q:
                write_bit, bit_len = bitPlusFollow(1, bit_to_follow, f, write_bit, bit_len)
                bit_to_follow=0
                low_v -= half_q
                high_v -= half_q
            elif low_v >= first_q and high_v < third_q:
                bit_to_follow += 1
                low_v -= first_q
                high_v -= first_q
            else:
                break
            low_v += low_v
            high_v += high_v + 1
        bit_to_follow += 1
        if low_v < first_q:
            write_bit, bit_len = bitPlusFollow(0, bit_to_follow, f, write_bit, bit_len)
            bit_to_follow = 0
        else:
            write_bit, bit_len = bitPlusFollow(1, bit_to_follow, f, write_bit, bit_len)
            bit_to_follow = 0

        write_bit >>= bit_len
        f.write(write_bit.to_bytes(1, "little"))
        print(counter)
        counter += 1

    f.close()

    sid = os.stat("in.txt").st_size
    sib = os.stat("out.txt").st_size

    print(f"szatie= {(sib/sid)*100}%")

if __name__ == "__main__":
    print("Выберите:\n1 - Кодировать\n2 - Декодировать")
    choice = int(input())
    if choice == 1:
        Coder()
    elif choice == 2:
        Decode()
    else:
        print("Вы ввели неверное число, попробуйте в следующий раз")
