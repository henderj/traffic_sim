def mutate_array(array=[]):
    array.append(4)
    return array


def main():
    array = [0, 1, 2]
    mutate_array(array)
    print(array)


if __name__ == "__main__":
    main()
