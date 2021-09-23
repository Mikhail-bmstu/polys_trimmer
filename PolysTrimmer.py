# imports
import re
import os
from time import process_time
from tqdm import tqdm

# global counters for stats file
p_A_cnt = 0
p_T_cnt = 0
p_A_Er_cnt = 0
p_T_Er_cnt = 0
mid_len = 0
read_cnt = 0


def file_corrector(task_file_path, asn_file_path):
    # patterns to edit rna/dna sequences
    poly_A = r'^(.*?)(AAAA*)\n'  # FGLKFDD(AAAAAA) -> FGLKFDD
    poly_T = r'^(TTTT*)(.*\n)'  # (TTTTTT)FDSKLDFLSDK -> FDSKLDFLSDK
    poly_A_Er = r'^(.*?)(AAA*[TCG]?AA*[TCG]A*[TCG]?A*)\n'  # FGLKFDD(AAAAGAAGAAAGA) -> FGLKFDD
    poly_T_Er = r'^([ACG]?[ACG]?T*[ACG]T*[ACG]?TTTT*)(.*\n)'  # (CTTTCTCTT)FGKJGDKGJ -> FGKJGDKGJ

    global p_A_cnt
    global p_T_cnt
    global p_A_Er_cnt
    global p_T_Er_cnt
    global mid_len
    global read_cnt

    with open(task_file_path, 'r', encoding="utf8") as task_file:
        with open(asn_file_path, 'w', encoding="utf8") as ans_file:
            lines = [line for line in task_file]
            for i in range(1, len(lines), 4):  # 1 read - 4 lines
                mid_len += len(lines[i])
                read_cnt += 1
                # search patterns
                # Poly A
                if re.search(poly_A_Er, lines[i]):  # poly A with error
                    match = re.search(poly_A_Er, lines[i])
                    poly_A_d = match.end(1) - match.start(1)
                    lines[i] = match.group(1) + '\n'
                    lines[i + 2] = lines[i + 2][:poly_A_d] + '\n'
                    p_A_Er_cnt += 1
                elif re.search(poly_A, lines[i]):  # poly A
                    match = re.search(poly_A, lines[i])
                    poly_A_d = match.end(1) - match.start(1)
                    lines[i] = match.group(1) + '\n'
                    lines[i + 2] = lines[i + 2][:poly_A_d] + '\n'
                    p_A_cnt += 1

                # Poly T
                if re.search(poly_T_Er, lines[i]):  # poly T with error
                    match = re.search(poly_T_Er, lines[i])
                    poly_T_d = match.end(1)
                    lines[i] = match.group(2)
                    lines[i + 2] = lines[i + 2][poly_T_d:]
                    p_T_Er_cnt += 1
                elif re.search(poly_T, lines[i]):  # poly T
                    match = re.search(poly_T, lines[i])
                    poly_T_d = match.end(1)
                    lines[i] = match.group(2)
                    lines[i + 2] = lines[i + 2][poly_T_d:]
                    p_T_cnt += 1

            ans_file.writelines(lines)  # edited lines


def file_ext(path_f):
    _, ext = os.path.splitext(path_f)
    return ext


def is_exists_dir(dir):
    return os.path.exists(dir)


def make_dir(dir):
    if not is_exists_dir(dir):
        print('Creating directory ' + dir)
        os.makedirs(dir)


def dir_walker(task_dir, ans_dir, prefix, stat_dir):
    t0 = process_time()  # timer

    make_dir(ans_dir)

    files = [
        f for f in os.listdir(task_dir)
        if file_ext(os.path.join(task_dir, f)) == ".fastq"
    ]
    for i in tqdm(range(len(files))):
        task_file_path = os.path.join(task_dir, files[i])
        asn_file_path = os.path.join(ans_dir, files[i])
        if prefix:
            asn_file_path = os.path.join(ans_dir, prefix + str(i + 1) + ".fastq")

        file_corrector(task_file_path, asn_file_path)

    # write result to stats file
    make_dir(stat_dir)
    with open(os.path.join(stat_dir, "stat_file.txt"), 'w', encoding="utf8") as stat_file:
        stat_file.write("Total: " + str(p_A_cnt + p_T_cnt + p_A_Er_cnt + p_T_Er_cnt) + "\n")
        stat_file.write("Poly A: " + str(p_A_cnt) + "\n")
        stat_file.write("Poly T: " + str(p_T_cnt) + "\n")
        stat_file.write("Poly A with errors: " + str(p_A_Er_cnt) + "\n")
        stat_file.write("Poly T with errors: " + str(p_T_Er_cnt) + "\n")
        stat_file.write("Poly A errors(%): " + str(round(p_A_Er_cnt * 100 / (p_A_cnt + p_A_Er_cnt), 2)) + "\n")
        stat_file.write("Poly T errors(%): " + str(round(p_T_Er_cnt * 100 / (p_T_cnt + p_T_Er_cnt), 2)) + "\n")
        stat_file.write("Middle read length: " + str(mid_len / read_cnt) + "\n")
        stat_file.write("Total read(lines): " + str(read_cnt) + "\n")

        print("Data is written to the statistic file, good luck ;)")

    t1 = process_time() - t0
    print(f"Corrected {len(files)} files in {t1 - t0} seconds")


def main():
    task_path = input("Enter the path of the files directory -> ")
    while not is_exists_dir(task_path):
        print("This directory doesn't exist!!!\nEnter the correct path...")
        task_path = input("Enter the path of the files directory -> ")

    ans_path = input("Enter the path of the directory where files will be saved -> ")

    while task_path == ans_path:
        print("Identical directories entered\nEnter the correct directories...")
        task_path = input("Enter the path of the files directory -> ")
        while not is_exists_dir(task_path):
            print("This directory doesn't exist!!!\nEnter the correct path...")
            task_path = input("Enter the path of the files directory -> ")

        ans_path = input("Enter the path of the directory where files will be saved -> ")

    prefix = "file"
    stat_path = ans_path

    if input("Use custom parameters? [y]es / [n]o (тыкать букву в [], т.е y/n): ") == 'y':
        if input("Use prefix? [y]es / [n]o: ") == 'y':
            prefix = input("Enter prefix for files -> ")
        if input("Change statistic file directory(default it's result directory)? [y]es / [n]o: ") == 'y':
            stat_path = input("Enter the path of the statistics file directory -> ")
    else:
        print("Statistics file directory is result files directory\nStatistics file name is sats_file")

    dir_walker(task_path, ans_path, prefix, stat_path)
    print("Check files in", ans_path, "and stats in", stat_path)


if __name__ == '__main__':
    main()
